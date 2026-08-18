# FILE INTEGRITY MONITOR (FIM)
Auditoria de Integridade e Analise Forense de Arquivos

---

## 1. INFORMACOES DO SISTEMA
- Linguagem: Python 3.x
- Modulos: hashlib, json, os, sys, argparse, datetime
- Algoritmo de Hash: SHA-256 (Leitura em Chunks de 4KB)
- Persistencia: data/baseline.json

---

## 2. VISAO GERAL
Sistema de monitoramento de integridade de arquivos (FIM) desenvolvido em Python para deteccao de alteracoes nao autorizadas, injecao de artefatos maliciosos e remocao de arquivos criticos atraves de assinaturas criptograficas SHA-256.

---

## 3. RECURSOS IMPLEMENTADOS
- Calculo de hash SHA-256 otimizado com leitura em blocos de 4096 bytes.
- Varredura recursiva de diretorios com normalizacao de caminhos absolutos.
- Geracao de Baseline (linha de base de integridade) com metadados em JSON.
- Motor de auditoria com classificacao em tres categorias de anomalias:
  * Arquivos Modificados (divergencia de hash SHA-256)
  * Arquivos Criados / Nao Autorizados (ausentes na baseline)
  * Arquivos Deletados (presentes na baseline, ausentes no disco)
- Relatorio forense detalhado com contagem e rastreamento de hashes.

---

## 4. INSTRUCOES DE USO

Clone o repositorio:
```bash
git clone [https://github.com/christzph/file-integrity-monitor.git](https://github.com/christzph/file-integrity-monitor.git)
cd file-integrity-monitor