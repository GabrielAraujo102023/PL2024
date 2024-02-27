import sys
import re

def process_text(text):
    r = ''
    bold_matched = re.match(r'(.*?)\*\*(.*?)\*\*', text)
    italics_matched = re.match(r'(.*?)\*([^*].*?)\*[^*]', text)
    link_matched = re.match(r'(.*?)[^!]\[(.*?)]\((.*?)\)', text)
    img_matched = re.match(r'(.*?)!\[(.*?)]\((.*?)\)', text)

    # Vê quem tem o match.end mais pequeno, ou seja, qual é o comando mais próximo do inicio da frase
    ends = {'bold': bold_matched.end() if bold_matched else sys.maxsize,
            'italics': italics_matched.end() if italics_matched else sys.maxsize,
            'link': link_matched.end() if link_matched else sys.maxsize,
            'img': img_matched.end() if img_matched else sys.maxsize}
    closest_match = min(ends, key=ends.get)
    if ends[closest_match] == sys.maxsize:
        r += text
    elif closest_match == 'bold':
        r += f'{bold_matched.group(1)}<b>{bold_matched.group(2)}</b>'
    elif closest_match == 'italics':
        r += f'{italics_matched.group(1)}<i>{italics_matched.group(2)}</i>'
    elif closest_match == 'link':
        r += f'{link_matched.group(1) + " "}<a href="{link_matched.group(3)}">{link_matched.group(2)}</a>'
    elif closest_match == 'img':
        r += f'{img_matched.group(1)}<img src="{img_matched.group(3)}">'
        r += f'<label>{img_matched.group(2)}</label>'
    return r


if len(sys.argv) == 2:
    html = """
    <!DOCTYPE html>
    <html lang="pt-PT">
    <head>
        <title>TPC2 - A102023</title>
        <meta charset="utf-8">
    </head>
    <body>
    """
    with open(sys.argv[1], 'r') as f:
        for line in f:
            h1_matched = re.match(r'^#[^#](.+)', line)
            if h1_matched:
                html += f'<h1>{h1_matched.group(1)}</h1>'
                continue

            h2_matched = re.match(r'^##([^#].+)', line)
            if h2_matched:
                html += f'<h2>{h2_matched.group(1)}</h2>'
                continue

            h3_matched = re.match(r'^###(.+)', line)
            if h3_matched:
                html += f'<h3>{h3_matched.group(1)}</h3>'
                continue

            list_matched = re.match(r'^1\.(.+)', line)
            if list_matched:
                html += '<ol>'
                html += '<li>'
                html += process_text(list_matched.group(1))
                html += '</li>'
                numb = 2
                while True:
                    item_matched = re.match(fr'^{numb}\.(.+)', line)
                    if item_matched:
                        html += '<li>'
                        html += process_text(item_matched.group(1))
                        html += '</li>'
                        numb += 1
                    else:
                        break
                html += '</ol>'
                continue
            html += '<p>'
            html += process_text(line)
            html += '</p>'

        html += '</body>'
        print(html)
        with open(sys.argv[1] + '.html', 'w') as hf:
            hf.write(html)
else:
    print('Argumentos: Path do ficheiro .md para traduzir para HTML')