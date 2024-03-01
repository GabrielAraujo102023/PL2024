import sys
import re

# Atualizar o texto para retirar tudo até logo a seguir ao comando
def update_text(t, i):
    return t[i:]

# Regex que apanham tudo até ao desejado
on = r'(on)'
off = r'(off)'
equals = r'(=)'
digit = r'(-|\+)?(\d+)' #Apanha vários digitos que podem ter um sinal atrás

#Apanha texto do stdin
text = sys.stdin.read()

n = 0
matched = re.search(on, text)
text = update_text(text, matched.end())
while matched:
    digit_matched = re.search(digit, text)
    equals_matched = re.search(equals, text)
    off_matched = re.search(off, text)

    # Vê quem tem o match.end mais pequeno, ou seja, qual é o comando mais próximo do inicio da frase
    ends = {'digit': digit_matched.end() if digit_matched else sys.maxsize,
            'equals': equals_matched.end() if equals_matched else sys.maxsize,
            'off': off_matched.end() if off_matched else sys.maxsize}
    closest_character = min(ends, key=ends.get)
    if ends[closest_character] == sys.maxsize:
        break
    if closest_character == 'digit':
        #Vê se o número é negativo
        sign = 1 if digit_matched.group(1) is None or digit_matched.group(1) == '+' else -1
        n += int(digit_matched.group(2)) * sign
        text = update_text(text, ends[closest_character])
    elif closest_character == 'equals':
        print(n)
        text = update_text(text, ends[closest_character])
    elif closest_character == 'off':
        text = update_text(text, off_matched.end())
        matched = re.search(on, text)
        continue
    else:
        break
print(f'Fim. Soma final -> {n}')