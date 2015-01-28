import os
import sys
import codecs

input_file = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2]) + '/SUMMARY.md'

if not os.path.exists(os.path.dirname(output_file)):
    os.makedirs(os.path.dirname(output_file))

path_dict = {}


def proccessSectionTree(output_file, line):
    if len(line.strip()) == 0:
        return
    if line.startswith("#"):
        return
    print line
    title_path = line[line.rindex("(") + 1:line.rindex(")")]
    title_path = title_path[:-len(".md")]
    paths = title_path.split('/')
    for path in paths:
        path_dict[path] = path;


with codecs.open(input_file, 'r', 'utf-8') as f:
    for line in f:
        proccessSectionTree(output_file, line)

out_file = codecs.open(output_file, 'w', 'utf-8')
for key, value in path_dict.items():
    out_file.write(key + '|' + value + '\n')
out_file.close()
