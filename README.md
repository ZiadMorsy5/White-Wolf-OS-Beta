# 🐺 White Wolf OS Beta

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JS-E34F26.svg?logo=html5&logoColor=white)
![Framework](https://img.shields.io/badge/Framework-Eel-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Beta-success.svg)

> **A lightweight, highly customizable, and user-friendly operating system prototype.**

## 📌 About The Project | عن المشروع

**White Wolf OS Beta** is a customized operating system prototype designed to simplify system management. It utilizes Python as a powerful backend engine to interact directly with hardware, and web technologies (HTML/CSS/JS) to provide a modern, responsive Graphical User Interface (GUI). It successfully consolidates essential system tools without the heavy overhead of a traditional kernel.

مشروع **White Wolf OS** هو نموذج أولي لنظام تشغيل مخصص وخفيف الوزن، يهدف إلى تبسيط بيئة العمل وإدارة موارد الجهاز بكفاءة عالية. يعتمد النظام على معمارية مبتكرة تستخدم لغة (Python) كمحرك خلفي للتعامل المباشر مع العتاد، وتقنيات الويب (HTML/CSS/JS) لتوفير واجهة رسومية عصرية، مما يقدم تجربة مستخدم سلسة ومستقرة.

---

## ✨ Key Features | الميزات الأساسية

* 📁 **File System Management:** A fully functional "Explorer" to navigate local drives. Supports standard file operations (Create, Read, Update, Delete) and features a blazing-fast built-in media player with a custom Windows 11-style context menu.
* ⚙️ **Process Management:** A dedicated "Task Manager" that fetches live, real-time data of active processes, displaying Process Names, PIDs, and Memory consumption percentages.
* 🧠 **Memory Management:** Real-time RAM tracking module with dynamic progress bars, breaking down metrics into Total RAM, Used RAM, and Free RAM.
* 💻 **I/O Devices Management:** Dynamically reads and displays Computer Node Name, OS version, CPU architecture, connected logical storage drives, and live battery status.

---

## 🛠️ Tech Stack | التقنيات المستخدمة

* **Backend Engine:** Python 3
* **GUI / Frontend:** HTML5, CSS3 (Glassmorphism UI), JavaScript
* **Bridge & Integration:** [Eel](https://github.com/python-eel/Eel)
* **System Utilities:** `psutil`, `py-cpuinfo`, `wmi` (for Windows)

---

## 🚀 Installation & Setup | طريقة التشغيل

To run **White Wolf OS Beta** on your local machine, follow these simple steps:

**1. Clone the repository:**
```bash
git clone [https://github.com/ZiadMorsy5/WhiteWolf-OS.git](https://github.com/ZiadMorsy5/WhiteWolf-OS.git)
cd WhiteWolf-OS
