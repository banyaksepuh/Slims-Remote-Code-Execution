# 🔐 SLims Auto Upload File via Remote Code Execution

**Automated tool for SLims RCE**

---

## 🧠 Overview

Tool ini digunakan untuk melakukan automated assessment terhadap aplikasi SLiMS (Senayan Library Management System) dengan fokus pada deteksi kerentanan pada komponen phpThumb.
Scanner akan mencoba mengirim payload ke endpoint PHPUnit yang diketahui rentan, lalu memvalidasi response untuk memastikan apakah target benar-benar dapat dieksekusi.

Tool ini dirancang untuk:
- Security assessment
- Vulnerability validation
- Research terhadap misconfiguration pada deployment SLiMS

> ⚠️ Tool ini dibuat hanya untuk **educational purposes** dan **authorized security testing**

---

## 🔍 Detection & Execution Flow
1. Target Normalization

Membersihkan input domain & Mendukung fallback:
- https://
- http://

2. Multi-Path Discovery

Tool akan mencoba berbagai kemungkinan path instalasi SLiMS:
- /slims7_cendana
- /cendana
- /perpustakaan
- /pustaka
- /digilib
- /slims
- /library
- /v7, /v8, /v9
- /senayan
- /admin
- Root (/)
menemukan lokasi instalasi SLiMS yang tidak standar

3. Vulnerability Check (RCE Test)

Target endpoint:
- /lib/watermark/phpThumb.php

Tool akan mengirim parameter khusus untuk menguji eksekusi command:
- blur|9 ;echo PYRE_VERIFIED;

Jika response mengandung string tersebut target dianggap vulnerable terhadap command execution

4. Payload Execution (Controlled)

Jika vulnerability terkonfirmasi:
Tool mencoba melakukan aksi lanjutan (misalnya validasi write capability)
Menggunakan teknik berbasis parameter injection pada phpThumb

5. Strict Validation

Hasil hanya dianggap valid jika:
Status code 200
Response mengandung signature tertentu (validation key)

---

## ⚙️ Features
- 🔍 Multi-threaded scanning
- ⚡ Multi-path auto discovery
- 🔐 RCE-based validation
- 🧪 Real-time progress tracking
- 🚀 Output logging otomatis

## 🛠️ Requirements

- Python 3.x
- requests
- tqdm

Install dependencies:
```bash
pip install -r requirements.txt
```
---
USAGE
---
📌 Basic Command with list
```bash
$ python scan.py -l list.txt
```
⚡ Advanced Usage with threads
```bash
$ python scan.py -l targets.txt -t 10
```
🧪 Output
```bash
[REAL JACKPOT] https://target.com/path/uploader.php
```
---
