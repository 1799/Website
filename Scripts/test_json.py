import sys
import json
import os


print(os.getcwd())
json_file = open('ultimate.json', 'r')
data = json.loads(json_file.read())
fopen = open(sys.argv[1] + '.txt')
fopen_json = open(sys.argv[1] + '.json', "w+")
fopen_json.truncate()
fopen_json.write('{\n')
lines = fopen.read().splitlines()
fopen = open(sys.argv[1] + '.txt')
last_line = lines[-1]
last_line_signal = ','
for line in fopen:
    line = line.rstrip()
    if(line ==last_line):
        last_line_signal = ''
    for i in range(len(data[line])):
        if(data[line][i].startswith('http://s3.amazonaws.com')):
            fopen_json.write('\t' + '"' + line + '": "'  + data[line][i] + '"' + last_line_signal +'\n')
fopen_json.write('}\n')
