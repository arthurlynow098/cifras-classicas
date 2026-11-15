"""As cifras em si. Só letras de A a Z mudam, o resto (espaço, número,
pontuação) passa direto, igual nas versões clássicas feitas no papel."""
from __future__ import annotations

import unicodedata
from itertools import cycle

ALPHA = "abcdefghijklmnopqrstuvwxyz"


def strip_accents(text: str) -> str:
    """'Ação' vira 'Acao'. As cifras clássicas só conhecem 26 letras."""
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")


def _shift(ch: str, k: int) -> str:
    if ch.isascii() and ch.isalpha():
        base = ord("A") if ch.isupper() else ord("a")
        return chr((ord(ch) - base + k) % 26 + base)
    return ch


def caesar(text: str, key: int) -> str:
    return "".join(_shift(c, key) for c in strip_accents(text))


def caesar_decrypt(text: str, key: int) -> str:
    return caesar(text, -key)


def _vigenere(text: str, key: str, sign: int) -> str:
    key = [ALPHA.index(c) for c in strip_accents(key).lower() if c in ALPHA]
    if not key:
        raise ValueError("a chave precisa ter pelo menos uma letra")
    out, ks = [], cycle(key)
    for c in strip_accents(text):
        out.append(_shift(c, sign * next(ks)) if c.isascii() and c.isalpha() else c)
    return "".join(out)


def vigenere(text: str, key: str) -> str:
    return _vigenere(text, key, 1)


def vigenere_decrypt(text: str, key: str) -> str:
    return _vigenere(text, key, -1)


def xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR é a própria inversa, cifrar e decifrar são a mesma operação."""
    if not key:
        raise ValueError("chave vazia")
    return bytes(b ^ k for b, k in zip(data, cycle(key)))
