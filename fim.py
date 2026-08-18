import argparse
from datetime import datetime
import hashlib
import json
import os
import sys

BASELINE_PATH = os.path.join("data", "baseline.json")

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

    abs_directory = os.path.abspath(directory)

    for root, _, files in os.walk(abs_directory):
        for filename in files:
            if filename == ".gitkeep":
                continue
            filepath = os.path.join(root, filename)
            file_hash = calculate_sha256(filepath)
            if file_hash is not None:
                results[filepath] = file_hash

    return results

def generate_baseline(directory):
    if not os.path.isdir(directory):
        print(f"[!] Erro: Diretorio '{directory}' nao existe.")
        return False

    print(f"[*] Gerando baseline para: {os.path.abspath(directory)}")
    file_hashes = scan_directory(directory)

    if not file_hashes:
        print("[!] Nenhum arquivo valido encontrado para gerar a baseline.")
        return False

    os.makedirs(os.path.dirname(BASELINE_PATH), exist_ok=True)

    baseline_data = {
        "created_at": datetime.now().isoformat(),
        "target_directory": os.path.abspath(directory),
        "total_files": len(file_hashes),
        "files": file_hashes,
    }

    try:
        with open(BASELINE_PATH, "w", encoding="utf-8") as f:
            json.dump(baseline_data, f, indent=4)

        print(f"[+] Baseline gerada com sucesso!")
        print(f"[+] Total de arquivos catalogados : {len(file_hashes)}")
        print(f"[+] Arquivo salvo em              : {BASELINE_PATH}\n")
        return True
    except OSError as e:
        print(f"[!] Erro ao salvar baseline: {e}")
        return False


def audit_directory(directory):
    if not os.path.isfile(BASELINE_PATH):
        print(f"[!] Erro: Arquivo de baseline '{BASELINE_PATH}' nao encontrado.")
        print("[!] Execute primeiro com o modo '--mode baseline' para registrar o estado inicial.")
        return False

    try:
        with open(BASELINE_PATH, "r", encoding="utf-8") as f:
            baseline_data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[!] Erro ao carregar arquivo de baseline: {e}")
        return False

    baseline_files = baseline_data.get("files", {})
    current_files = scan_directory(directory)

    print(f"[*] Baseline criada em : {baseline_data.get('created_at', 'Data desconhecida')}")
    print(f"[*] Total monitorado   : {len(baseline_files)} arquivos na baseline")
    print(f"[*] Estado atual       : {len(current_files)} arquivos encontrados")
    print("-" * 65)

    modified_files = []
    created_files = []
    deleted_files = []
    intact_count = 0

    for filepath, stored_hash in baseline_files.items():
        if filepath in current_files:
            if current_files[filepath] == stored_hash:
                intact_count += 1
            else:
                modified_files.append((filepath, stored_hash, current_files[filepath]))
        else:
            deleted_files.append(filepath)

    for filepath in current_files:
        if filepath not in baseline_files:
            created_files.append(filepath)

    if modified_files:
        print(f"\n[ALERTA] ARQUIVOS MODIFICADOS ({len(modified_files)}):")
        for path, old_h, new_h in modified_files:
            print(f"  [!] {path}")
            print(f"      Hash Original: {old_h[:16]}...")
            print(f"      Hash Atual   : {new_h[:16]}...")

    if created_files:
        print(f"\n[AVISO] ARQUIVOS CRIADOS / NAO AUTORIZADOS ({len(created_files)}):")
        for path in created_files:
            print(f"  [+] {path} (SHA-256: {current_files[path][:16]}...)")

    if deleted_files:
        print(f"\n[ALERTA] ARQUIVOS DELETADOS ({len(deleted_files)}):")
        for path in deleted_files:
            print(f"  [-] {path}")

    print("\n" + "=" * 65)
    print("  RESUMO DA AUDITORIA FORENSE")
    print("=" * 65)
    print(f"  Integramos/Sem alteracao: {intact_count}")
    print(f"  Modificados             : {len(modified_files)}")
    print(f"  Criados/Novos           : {len(created_files)}")
    print(f"  Deletados               : {len(deleted_files)}")

    if not modified_files and not created_files and not deleted_files:
        print("\n[OK] SUCESSO: Todos os arquivos estao 100% integros e inalterados.")
    else:
        print("\n[!] ATENCAO: Foram detectadas divergencias no diretorio monitorado.")

    return True

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
        generate_baseline(args.dir)

    elif args.mode == "audit":
        audit_directory(args.dir)

if __name__ == "__main__":
    main()