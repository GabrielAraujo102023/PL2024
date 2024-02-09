import sys

modalidades = set()
total = 0
aptos = 0
ranges = {(start, start + 4): [] for start in range(0, 100, 5)}
first = True

for line in sys.stdin:
    if first: # Passar primeira linha
        first = False
        continue
    total += 1
    data = line.strip().split(',')
    modalidades.add(data[8])
    if data[12] == 'true':
        aptos += 1
    for (a, b) in ranges.keys():
        if a <= int(data[5]) <= b:
            ranges[(a,b)].append(data[3] + ' ' + data[4])


mod_file = open('./resultados/modalidades.txt', 'w')
for modalidade in sorted(modalidades):
    mod_file.write(modalidade + '\n')

apt_file = open('./resultados/percentagens.txt', 'w')
apt_file.write(f'Aptos: {(aptos * 100) / total}%\n')
apt_file.write(f'Não aptos: {((total - aptos) * 100) / total}%')

age_files = open('./resultados/idades.txt', 'w')
for ((a,b), nomes) in ranges.items():
    if len(nomes) > 0:
        age_files.write(f'[{a}, {b}]\n')
        for nome in nomes:
            age_files.write('\t' + nome + '\n')