import sys
import re

def update_text(t, i):
    return t[i:]

on = r'.*?\s*?.*?(on)'
off = r'.*?\s*?.*?(off)'
equals = r'\s*?.*?.*?(=)'
digit = r'.*?\s*?.*?(-|\+)?(\d+)'
text = sys.stdin.read()
n = 0
matched = re.match(on, text)
text = update_text(text, matched.end())
while matched:
    digit_matched = re.match(digit, text)
    equals_matched = re.match(equals, text)
    off_matched = re.match(off, text)

    ends = {'digit': digit_matched.end() if digit_matched else sys.maxsize,
            'equals': equals_matched.end() if equals_matched else sys.maxsize,
            'off': off_matched.end() if off_matched else sys.maxsize}
    closest_character = min(ends, key=ends.get)
    if ends[closest_character] == sys.maxsize:
        break
    if closest_character == 'digit':
        sign = 1 if digit_matched.group(1) is None or digit_matched.group(1) == '+' else -1
        n += int(digit_matched.group(2)) * sign
        text = update_text(text, ends[closest_character])
    elif closest_character == 'equals':
        print(n)
        text = update_text(text, ends[closest_character])
    elif closest_character == 'off':
        text = update_text(text, off_matched.end())
        matched = re.match(on, text)
        continue
    else:
        break
print(f'Fim. Soma final -> {n}')