import sys
from ply import lex
import re

def get_price(moedas):
    m = re.match(r'(\d+)e(\d+)c', moedas)
    if m:
        return int(m.group(1)) + (int(m.group(2)) / 100)

    m = re.search(r'(\d+)e', moedas)
    if m:
        return int(m.group(1))

    m = re.search(r'(\d+)c', moedas)
    if m:
        return float(m.group(1)) / 100

SALDO = 0
moedas = {'2e':2, '1e':1, '50c':0.5, '20c':0.2, '10c':0.1, '5c':0.05}
produtos = []
ids = []
with open(sys.argv[1], 'r') as f:
    for line in f:
        s = line.split(';')
        produtos.append({'id': s[0], 'nome': s[1], 'preco': s[2]})
        ids.append(s[0])

tokens = (
    'LISTAR',
    'SELECIONAR',
    'SAIR',
    'DOISEUROS',
    'UMEURO',
    'CINQUENTACENT',
    'VINTECENT',
    'DEZCENT',
    'CINCOCENT',
    'SALDO'
)

def t_SALDO(t):
    r'SALDO'
    global SALDO
    print(f'SALDO = {SALDO}')
    return t

def t_LISTAR(t):
    r'^LISTAR$'
    print('ID - PRODUTO - PREÇO')
    for produto in produtos:
        print(f'{produto["id"]} - {produto["nome"]} - {produto["preco"]}')
    return t

def t_SELECIONAR(t):
    r'SELECIONAR\s*\d+'
    m = re.match(r'SELECIONAR (\d+)', t.value)
    if m:
        product_id = m.group(1)
        if product_id in ids:
            global SALDO, moedas, produtos
            value = get_price(produtos[int(product_id)]['preco'])
            if SALDO >= value:
                SALDO -= value
            else:
                print('Saldo insuficiente')
        else:
            print('Produto não encontrado')
    else:
        print('Erro ao analisar a instrução SELECIONAR:', t.value)

def t_DOISEUROS(t):
    r'2e'
    global SALDO
    SALDO += 2
    return t

def t_UMEURO(t):
    r'1e'
    global SALDO
    SALDO += 1
    return t

def t_CINQUENTACENT(t):
    r'50c'
    global SALDO
    SALDO += 0.5
    return t

def t_VINTECENT(t):
    r'20c'
    global SALDO
    SALDO += 0.2
    return t

def t_DEZCENT(t):
    r'10c'
    global SALDO
    SALDO += 0.1
    return t

def t_CINCOCENT(t):
    r'5c'
    global SALDO
    SALDO += 0.05
    return t

def t_SAIR(t):
    r'SAIR'
    global SALDO
    print(f'TROCO = {SALDO}')
    sys.exit(0)

t_ignore = r' '

def t_error(t):
    print(f'Illegal character {t.value[0]}')
    t.lexer.skip(1)

lexer = lex.lex()

print('Máquina ligada.')
while True:
    lexer.input(input())
    tok = lexer.token()
    print(tok)
