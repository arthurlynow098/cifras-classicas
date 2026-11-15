<p align="center"><sub>Cifras Clássicas</sub></p>

---

<p align="center">
  <img src="assets/banner.png" alt="Cifras Clássicas" width="100%">
</p>

<p align="center">
  César, Vigenère e XOR, e a análise de frequência que quebra cada uma em português
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-F59E0B?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Criptografia" src="https://img.shields.io/badge/criptografia-cl%C3%A1ssica-242424?style=for-the-badge">
  <a href="https://github.com/arthurlynow098/cifras-classicas/actions/workflows/testes.yml"><img alt="Testes" src="https://img.shields.io/github/actions/workflow/status/arthurlynow098/cifras-classicas/testes.yml?style=for-the-badge&label=testes&color=242424"></a>
  <img alt="Licença MIT" src="https://img.shields.io/badge/licen%C3%A7a-MIT-242424?style=for-the-badge">
</p>

## Sobre o projeto

Todo curso de segurança começa falando da cifra de César e eu sempre achei aquilo meio bobo, até entender o ponto. Ninguém usa César hoje, mas **o motivo de ela ter caído** é a base de toda a criptografia moderna. Se a cifra deixa o padrão da língua passar, a matemática quebra ela, não importa quão secreta seja a chave.

Esse projeto implementa César, Vigenère e XOR e, mais importante, **quebra** César e Vigenère sem saber a chave, usando análise de frequência do português. É o meu laboratório de criptoanálise, no espírito dos desafios do Cryptopals.

## Como funciona

```mermaid
flowchart LR
    A[texto cifrado] --> B[testa tamanhos de chave de 1 a 12]
    B --> C[separa em colunas e calcula o índice de coincidência]
    C --> D[tamanho com IC parecido com português]
    D --> E[cada coluna vira uma César]
    E --> F[qui-quadrado em cada coluna]
    F --> G[chave e texto original]
```

## Tecnologias

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&amp;logo=python&amp;logoColor=white">
  <img alt="Criptoanálise" src="https://img.shields.io/badge/Criptoan%C3%A1lise-2B2B2B?style=flat-square">
</p>

## Executando o código

Só precisa de Python 3.10 ou mais novo. O texto aceita uma frase direta, um caminho de arquivo ou `-` para ler da entrada padrão.

```bash
git clone https://github.com/arthurlynow098/cifras-classicas.git
cd cifras-classicas

python -m cifras cesar "Ave Cesar" 3
python -m cifras vigenere exemplos/texto.txt lince > cifrado.txt

python -m cifras analisar cifrado.txt
python -m cifras quebrar-vigenere cifrado.txt
python -m cifras quebrar-cesar outro.txt --top 5
```

Testes

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

Os testes cifram o texto de exemplo com uma chave e conferem que o programa recupera a mesma chave sozinho.

## Exemplo

O texto de `exemplos/texto.txt` cifrado com Vigenère e a chave `lince` começa assim

```text
L kektewtteqqn cgzuccrsi n jyxiakhllr je xcvvs emzrs. Za tgrpznkw cwzcrza ...
```

```text
$ python -m cifras analisar cifrado.txt

  índice de coincidência  0.0431
  (português fica perto de 0.072, texto aleatório perto de 0.038)

  tamanhos de chave mais prováveis
    10  0.0809
    5   0.0803
    2   0.0433

$ python -m cifras quebrar-vigenere cifrado.txt

  chave provável  lince

A criptografia acompanha a humanidade ha muito tempo. Os generais romanos ...
```

## Estudei por aqui

Segui essas aulas e materiais para entender e aplicar tudo que está aqui.

| Material | O que tirei dele |
|---|---|
| [TryHackMe, Introduction to Cryptography](https://tryhackme.com/room/cryptographyintro) | Cifras clássicas e a transição para a criptografia moderna |
| [Cryptopals](https://cryptopals.com/) | Desafios práticos de criptoanálise, de onde veio a ideia de pontuar o texto |
| [OverTheWire Bandit](https://overthewire.org/wargames/bandit/) | Prática de terminal, onde aparecem ROT13 e codificações |
| [Curso em Vídeo, Python Mundo 1](https://www.youtube.com/playlist?list=PLHz_AreHm4dlKP6QQCekuIPky1CiwmdI6) | Base de Python que usei em todos os projetos |

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).

<p align="center"><sub>A gravura do banner é o escaravelho da prancha de besouros de Georgiy Jacobson, em domínio público no <a href="https://commons.wikimedia.org/wiki/File%3AGeorgiy_Jacobson_-_Beetles_Russia_and_Western_Europe_-_plate_30.jpg">Wikimedia Commons</a>.</sub></p>
