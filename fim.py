import hashlib
import os
import sys

def calculate_sha256(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def main():
    print("=" * 65)
    print("  FILE INTEGRITY MONITOR (FIM) - MODULO DE HASH")
    print("=" * 65)

    if len(sys.argv) < 2:
        print("\n[!] Uso: python3 fim.py <caminho_do_arquivo>")
        sys.exit(1)

    target_path = sys.argv[1]

    if os.path.isfile(target_path):
        file_hash = calculate_sha256(target_path)
        print(f"\n[+] Arquivo : {target_path}")
        print(f"[+] SHA-256 : {file_hash}\n")
    else:
        print(f"\n[!] Erro: '{target_path}' nao e um arquivo valido.")

if __name__ == "__main__":
    main()