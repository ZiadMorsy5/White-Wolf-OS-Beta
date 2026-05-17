import webview
import os
import sys
import psutil
import subprocess
import platform
import shutil
import http.server
import socketserver
import threading
import urllib.parse

# ========================================================
# 🚀 سيرفر البث الداخلي (لتشغيل الميديا فوراً داخل المحاكي)
# ========================================================
class MediaStreamHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # فك تشفير المسار القادم من المتصفح (مثال: C:/video.mp4)
        clean_path = urllib.parse.unquote(path)
        if clean_path.startswith('/'):
            clean_path = clean_path[1:]
        return clean_path

    def log_message(self, format, *args):
        pass # إخفاء سجلات السيرفر لمنع زحمة التيرمينال

def start_media_server():
    """تشغيل السيرفر في الخلفية على بورت 54321"""
    try:
        server = socketserver.TCPServer(("127.0.0.1", 54321), MediaStreamHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
    except:
        pass # إذا كان البورت يعمل مسبقاً، تجاهل الخطأ

# تشغيل السيرفر فور فتح البرنامج
start_media_server()
# ========================================================

class WhiteWolfAPI:
    def get_drives(self):
        """جلب الأقراص المتاحة (سريعة جداً)"""
        try:
            return [part.device.replace('\\', '') for part in psutil.disk_partitions(all=False) if 'cdrom' not in part.opts and part.fstype != '']
        except:
            return ['C:']

    def get_files(self, path):
        try:
            path = os.path.normpath(path)
            if len(path) == 2 and path[1] == ':': 
                path += '\\'
            
            if not os.path.exists(path):
                return {'error': f'المسار غير موجود: {path}'}

            files = []
            for f in os.listdir(path):
                full_path = os.path.join(path, f)
                safe_path = full_path.replace('\\', '/')
                files.append({
                    'name': f, 
                    'is_dir': os.path.isdir(full_path), 
                    'path': safe_path
                })
            
            files.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
            return files
            
        except PermissionError:
            return {'error': 'ليس لديك صلاحية للدخول لهذا المجلد (Access Denied)'}
        except Exception as e: 
            return {'error': str(e)}

    def open_real_file(self, path):
        """فتح الملفات (مثل PDF و EXE) بالمشغل الافتراضي للويندوز"""
        try:
            os.startfile(path) if platform.system() == 'Windows' else subprocess.run(['open', path])
            return True
        except: return False

    def run_cmd(self, command):
        """مترجم أوامر التيرمينال الذكي (Bash to Windows + Mock Commands)"""
        try:
            command = command.strip()
            if not command: return ""
            
            # تقسيم الأمر لمعرفة الأداة
            parts = command.split()
            base_cmd = parts[0].lower()
            args = " ".join(parts[1:])

            # ==========================================
            # 1. الأوامر الوهمية (Mock Commands) للبروتوتايب
            # ==========================================
            if base_cmd == "sudo":
                return f"[sudo] password for wolf:\nAccess Granted. Executing '{args}' with root privileges..." if args else "usage: sudo <command>"
            
            elif base_cmd == "useradd":
                return f"User '{args}' has been created and added to the system successfully." if args else "Usage: useradd <username>"
            
            elif base_cmd == "userdel":
                return f"User '{args}' has been removed from the system." if args else "Usage: userdel <username>"
            
            elif base_cmd == "passwd":
                target_user = args if args else "wolf"
                return f"Changing password for user {target_user}...\nPassword updated successfully."
            
            elif base_cmd == "chmod":
                return f"Permissions updated successfully for '{args}'." if args else "Usage: chmod <permissions> <file>"
            
            elif base_cmd in ["nano", "vim"]:
                return f"GUI Environment Active: Interactive editor '{base_cmd}' is restricted. Please use the visual Text Editor from the Desktop."
            
            elif base_cmd == "bash":
                return "bash: already running White Wolf OS bash environment. (Version 1.0.0)"

            # ==========================================
            # 2. الأوامر الحقيقية (Real Commands)
            # ==========================================
            elif base_cmd == "ls":
                cmd_to_run = f"dir /b {args}" if not args or "-l" not in args else f"dir {args.replace('-l', '')}"
            elif base_cmd == "pwd":
                cmd_to_run = "cd"
            elif base_cmd == "clear":
                return "CLEAR_TERMINAL_SIGNAL"
            elif base_cmd == "touch":
                cmd_to_run = f"type nul > {args}" if args else "touch: missing file operand"
            elif base_cmd == "cat":
                cmd_to_run = f"type {args}" if args else "cat: missing file operand"
            elif base_cmd == "rm" and "-rf" in args:
                target = args.replace("-rf", "").strip()
                cmd_to_run = f"rmdir /s /q {target}" if target else "rm: missing operand"
            elif base_cmd == "ifconfig":
                cmd_to_run = "ipconfig"
            else:
                cmd_to_run = command

            # تنفيذ الأوامر الحقيقية في الخلفية
            res = subprocess.run(cmd_to_run, shell=True, capture_output=True, text=True, timeout=10)
            output = res.stdout if res.stdout else res.stderr
            return output if output else "Done."
            
        except Exception as e:
            return f"Error: {str(e)}"

    def delete_item(self, path):
        try:
            if os.path.isdir(path): shutil.rmtree(path)
            else: os.remove(path)
            return "success"
        except Exception as e: return str(e)

    def rename_item(self, old_path, new_name):
        try:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            os.rename(old_path, new_path)
            return "success"
        except Exception as e: return str(e)

    def create_item(self, path, name, is_folder):
        try:
            full_path = os.path.join(path, name)
            if is_folder: os.makedirs(full_path, exist_ok=True)
            else: open(full_path, 'w').close()
            return "success"
        except Exception as e: return str(e)

    def paste_item(self, src_path, dest_dir, action):
        try:
            dest_path = os.path.join(dest_dir, os.path.basename(src_path))
            if action == 'copy':
                if os.path.isdir(src_path): shutil.copytree(src_path, dest_path)
                else: shutil.copy2(src_path, dest_path)
            elif action == 'cut':
                shutil.move(src_path, dest_path)
            return "success"
        except Exception as e: return str(e)

    def get_processes(self):
        """بيانات مدير المهام"""
        try:
            procs = []
            for p in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try: procs.append({'pid': p.info['pid'], 'name': p.info['name'], 'mem': round(p.info['memory_percent'] or 0, 2)})
                except: pass
            procs = sorted(procs, key=lambda x: x['mem'], reverse=True)[:50]
            sys_info = {'cpu': psutil.cpu_percent(), 'ram': psutil.virtual_memory().percent}
            return {'procs': procs, 'sys': sys_info}
        except Exception as e: return {'error': str(e)}

    def get_memory_details(self):
        """تفاصيل استهلاك الذاكرة للإعدادات"""
        try:
            mem = psutil.virtual_memory()
            return {
                'total': round(mem.total / (1024**3), 2),
                'used': round(mem.used / (1024**3), 2),
                'free': round(mem.available / (1024**3), 2),
                'percent': mem.percent
            }
        except Exception as e: return {'error': str(e)}

    def get_io_devices(self):
        """تفاصيل الجهاز والنظام للإعدادات"""
        try:
            devices = {
                'os': platform.system() + " " + platform.release(),
                'processor': platform.processor(),
                'machine': platform.machine(),
                'node': platform.node(),
                'disks': self.get_drives()
            }
            if hasattr(psutil, 'sensors_battery'):
                battery = psutil.sensors_battery()
                if battery:
                    devices['battery'] = f"{battery.percent}% ({'Charging' if battery.power_plugged else 'Discharged'})"
            return devices
        except Exception as e: return {'error': str(e)}

if __name__ == '__main__':
    api = WhiteWolfAPI()
    
    # الكود السحري لتحديد مسار ملف HTML سواء كنت بتشغله ككود أو كبرنامج exe
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
    html_file = os.path.join(base_dir, 'index.html')
    
    # فتح النافذة بالمسار الصحيح والمضمون
    window = webview.create_window('White Wolf OS - Pro Edition', html_file, js_api=api, width=1280, height=800, background_color='#1e272e')
    webview.start()
