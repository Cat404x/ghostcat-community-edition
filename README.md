# GhostCat Community 🐾

GhostCat Community is a lightweight, cross-platform Python CLI tool for basic LAN discovery.

It is built for educational purposes and authorized internal network auditing only.

---

## Features

• Cross-platform (Windows, macOS, Linux)  
• No external dependencies (standard library only)  
• TCP connect-based host detection  
• Default ports: 80, 443  
• Custom port support  
• JSON export support  
• Safe thread limit (max 25 workers)  
• Clean CLI interface  

---

## Installation

Clone the repository:

git clone https://github.com/Cat404x/ghostcat-community-edition.git  
cd ghostcat-community-edition  

No additional packages required.

---

## Usage

Scan a network:

python main.py -s 192.168.1.0/24  

Scan with custom ports:

python main.py -s 192.168.1.0/24 -p 22,80,443  

Export results:

python main.py -s 192.168.1.0/24 -e  

Show version:

python main.py --version  

---

## Legal Notice

This tool is intended for use only on networks you own or are explicitly authorized to audit.

The user is responsible for complying with all applicable laws and organizational policies.

---

## Version

Current version: v0.1.0
