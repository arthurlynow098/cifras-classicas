from pathlib import Path

import pytest

from cifras.analysis import break_caesar, break_vigenere, index_of_coincidence, letters
from cifras.ciphers import caesar, caesar_decrypt, strip_accents, vigenere, vigenere_decrypt, xor_bytes

TEXTO = (Path(__file__).resolve().parent.parent / "exemplos" / "texto.txt").read_text(encoding="utf-8")


def test_cesar_ida_e_volta():
    assert caesar("Ave Cesar", 3) == "Dyh Fhvdu"
    assert caesar_decrypt(caesar("Lince Lab 2026!", 11), 11) == "Lince Lab 2026!"


def test_acentos_sao_removidos():
    assert strip_accents("Ação, coração") == "Acao, coracao"


def test_vigenere_exemplo_classico():
    assert vigenere("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
    assert vigenere_decrypt("LXFOPVEFRNHR", "lemon") == "ATTACKATDAWN"


def test_vigenere_chave_sem_letra():
    with pytest.raises(ValueError):
        vigenere("abc", "123")


def test_xor_e_inverso_dele_mesmo():
    dado = b"mensagem secreta"
    assert xor_bytes(xor_bytes(dado, b"k3y"), b"k3y") == dado


def test_quebra_cesar_sem_saber_a_chave():
    cifrado = caesar(TEXTO, 17)
    chave, _, texto = break_caesar(cifrado)[0]
    assert chave == 17
    assert texto.startswith("A criptografia")


def test_indice_de_coincidencia_do_portugues():
    assert 0.065 < index_of_coincidence(TEXTO) < 0.085


def test_quebra_vigenere_sem_saber_a_chave():
    cifrado = vigenere(TEXTO, "lince")
    chave, texto = break_vigenere(cifrado)
    assert chave == "lince"
    assert letters(texto) == letters(TEXTO)
