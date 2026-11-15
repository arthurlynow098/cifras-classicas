from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analysis import break_caesar, break_vigenere, guess_key_length, index_of_coincidence
from .ciphers import caesar, caesar_decrypt, vigenere, vigenere_decrypt


def read_text(value: str) -> str:
    if value == "-":
        return sys.stdin.read()
    path = Path(value)
    return path.read_text(encoding="utf-8") if path.is_file() else value


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cifras", description="Cifras clássicas e criptoanálise por frequência.")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("cesar", "decifrar-cesar"):
        s = sub.add_parser(name)
        s.add_argument("texto", help="texto, caminho de arquivo ou - para stdin")
        s.add_argument("chave", type=int)
    for name in ("vigenere", "decifrar-vigenere"):
        s = sub.add_parser(name)
        s.add_argument("texto")
        s.add_argument("chave")
    s = sub.add_parser("quebrar-cesar", help="descobre a chave sem saber nada")
    s.add_argument("texto")
    s.add_argument("--top", type=int, default=3)
    s = sub.add_parser("quebrar-vigenere", help="descobre o tamanho da chave e depois a chave")
    s.add_argument("texto")
    s = sub.add_parser("analisar", help="mostra índice de coincidência e tamanhos prováveis de chave")
    s.add_argument("texto")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    text = read_text(args.texto)
    if args.cmd == "cesar":
        print(caesar(text, args.chave))
    elif args.cmd == "decifrar-cesar":
        print(caesar_decrypt(text, args.chave))
    elif args.cmd == "vigenere":
        print(vigenere(text, args.chave))
    elif args.cmd == "decifrar-vigenere":
        print(vigenere_decrypt(text, args.chave))
    elif args.cmd == "quebrar-cesar":
        print("\n  chave  chi²      começo do texto")
        for key, score, plain in break_caesar(text)[: args.top]:
            print(f"  {key:<6} {score:<9.1f} {plain[:60]!r}")
        print()
    elif args.cmd == "quebrar-vigenere":
        key, plain = break_vigenere(text)
        print(f"\n  chave provável  {key}\n\n{plain}\n")
    elif args.cmd == "analisar":
        print(f"\n  índice de coincidência  {index_of_coincidence(text):.4f}")
        print("  (português fica perto de 0.072, texto aleatório perto de 0.038)\n")
        print("  tamanhos de chave mais prováveis")
        for size, ic in guess_key_length(text)[:5]:
            print(f"    {size:<4}{ic:.4f}")
        print()
    return 0
