"""Criptoanálise por frequência, o motivo de essas cifras serem só históricas.

Em português o A, o E e o O aparecem muito mais que o resto. A César só
desloca as letras, então o "formato" da frequência continua igual, só que
deslocado. Basta testar os 26 deslocamentos e ver qual encaixa melhor.
"""
from __future__ import annotations

from collections import Counter

from .ciphers import ALPHA, caesar_decrypt, strip_accents, vigenere_decrypt

# frequência aproximada das letras em textos em português, em %
PT_FREQ = {
    "a": 14.63, "b": 1.04, "c": 3.88, "d": 4.99, "e": 12.57, "f": 1.02, "g": 1.30, "h": 1.28,
    "i": 6.18, "j": 0.40, "k": 0.02, "l": 2.78, "m": 4.74, "n": 5.05, "o": 10.73, "p": 2.52,
    "q": 1.20, "r": 6.53, "s": 7.81, "t": 4.34, "u": 4.63, "v": 1.67, "w": 0.01, "x": 0.21,
    "y": 0.01, "z": 0.47,
}


def letters(text: str) -> str:
    return "".join(c for c in strip_accents(text).lower() if c in ALPHA)


def chi_squared(text: str) -> float:
    """Quanto a frequência do texto foge da do português. Menor é melhor."""
    only = letters(text)
    n = len(only)
    if n == 0:
        return float("inf")
    counts = Counter(only)
    return sum((counts.get(c, 0) - n * p / 100) ** 2 / (n * p / 100) for c, p in PT_FREQ.items())


def break_caesar(ciphertext: str) -> list[tuple[int, float, str]]:
    """Devolve os 26 candidatos ordenados do mais provável para o menos."""
    results = []
    for key in range(26):
        plain = caesar_decrypt(ciphertext, key)
        results.append((key, chi_squared(plain), plain))
    return sorted(results, key=lambda r: r[1])


def index_of_coincidence(text: str) -> float:
    """Chance de duas letras sorteadas do texto serem iguais.
    Português fica perto de 0.072, texto aleatório perto de 0.038."""
    only = letters(text)
    n = len(only)
    if n < 2:
        return 0.0
    return sum(v * (v - 1) for v in Counter(only).values()) / (n * (n - 1))


def guess_key_length(ciphertext: str, max_len: int = 12) -> list[tuple[int, float]]:
    """Separa o texto em colunas para cada tamanho de chave candidato.
    No tamanho certo cada coluna é uma César simples e o IC volta a parecer português."""
    only = letters(ciphertext)
    scores = []
    for size in range(1, max_len + 1):
        cols = [only[i::size] for i in range(size)]
        scores.append((size, sum(index_of_coincidence(c) for c in cols) / size))
    return sorted(scores, key=lambda s: -s[1])


def break_vigenere(ciphertext: str, max_len: int = 12) -> tuple[str, str]:
    only = letters(ciphertext)
    best_ic = guess_key_length(ciphertext, max_len)[0][1]
    # pega o MENOR tamanho com IC quase tão bom quanto o melhor, porque múltiplos
    # do tamanho certo (2x, 3x) também ficam com IC alto
    size = min(s for s, ic in guess_key_length(ciphertext, max_len) if ic >= best_ic * 0.9)
    key = ""
    for i in range(size):
        column = only[i::size]
        shift = break_caesar(column)[0][0]
        key += ALPHA[shift]
    return key, vigenere_decrypt(ciphertext, key)
