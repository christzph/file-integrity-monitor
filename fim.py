import argparse
import hashlib
import os
import sys

def calculate_sha256(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as file:
            while chunk := file.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (PermissionError, FileNotFoundError, OSError):
        return None


def scan_directory(directory):
    results = {}

    if not os.path.isdir(directory):
        return results

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = calculate_sha256(filepath)
            if file_hash is not None:
                results[filepath] = file_hash

    return results


def main():
    parser = argparse.ArgumentParser(
        description="File Integrity Monitor (FIM) - Monitor de Integridade de Arquivos"
    )

    parser.add_argument(
        "-d",
        "--dir",
        required=True,
        help="Caminho do diretorio a ser monitorado",
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["scan", "baseline", "audit"],
        default="scan",
        help="Modo de operacao: scan (listar), baseline (gravar), audit (verificar)",
    )

    args = parser.parse_args()

    print("=" * 65)
    print("  FILE INTEGRITY MONITOR (FIM) - PARSER & VARREDURA")
    print("=" * 65)

    if args.mode == "scan":
        results = scan_directory(args.dir)
        print(f"\n[+] Total de arquivos mapeados: {len(results)}\n")
        for path, hash_val in results.items():
            print(f"  {hash_val[:16]}...  {path}")
        print()
    elif args.mode == "baseline":
        print(f"\n[!] Modo baseline ainda nao implementado para: {args.dir}\n")
    elif args.mode == "audit":
        print(f"\n[!] Modo audit ainda nao implementado para: {args.dir}\n")


if __name__ == "__main__":
    main()