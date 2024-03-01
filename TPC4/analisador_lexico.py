import sys
import re

regex_patterns = [('RESERVED', r'(SELECT|FROM|WHERE)'),
                  ('NUMBER', r'\d+'),
                  ('COMMA', r','),
                  ('NEWLINE', r'\n'),
                  ('SKIP', r'\s+'),
                  ('GREATEROREQUAL', r'>='),
                  ('ID', r'\w+'),
                  ('UNKNOWN', r'.')]

pattern = "|".join(f"(?P<{name}>{pattern})" for name, pattern in regex_patterns)

for line in sys.stdin:
    match = re.findall(pattern, line)
    if match:
        for m in match:
            for i in range(1, len(m)):
                if m[i] != '':
                    if m[i] != '\n':
                        print(f'{m[i]} -> {regex_patterns[i - 1][0]}')
                    else:
                        print(regex_patterns[i - 1][0])