# -*- coding: UTF-8 -*-

import os
import sys
import codecs
from collections import OrderedDict

input_file = os.path.abspath(sys.argv[1])
output_dir = os.path.abspath(sys.argv[2])
output_dir_zh = output_dir + "/zh-CN"
index = 0
index_dict = {}
tree = OrderedDict()

if not os.path.exists(output_dir_zh):
    os.makedirs(output_dir_zh)
output_file = codecs.open(output_dir_zh + '/administrator-guide.xml', 'w', 'utf-8')


def output_prefix(output_file):
    output_file.write("<?xml version='1.0' encoding='utf-8' ?>\n")
    output_file.write("<!DOCTYPE section [\n")
    output_file.write("<!ENTITY % openstack SYSTEM \"administrator-guide.ent\">\n")
    output_file.write("%openstack;\n")
    output_file.write("]>\n")
    output_file.write("<book xmlns=\"http://docbook.org/ns/docbook\"\n")
    output_file.write("  xmlns:xi=\"http://www.w3.org/2001/XInclude\"\n")
    output_file.write("  xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n")
    output_file.write("  version=\"5.0\"\n")
    output_file.write("  xml:id=\"openstack-arch-design\">\n")
    output_file.write("  <title>oVirt administrator guide</title>\n")


def output_suffix(output_file):
    output_file.write("</book>")
    output_file.close()


def proccessSectionTree(output_file, line):
    if len(line.strip()) == 0:
        return
    if line.startswith("#"):
        return
    title = line[line.index("[") + 1:line.rindex("]")]
    title_path = line[line.rindex("(") + 1:line.rindex(")")]
    title_path = title_path[:-len(".md")]
    depth = (len(line) - len(line.lstrip()) + 1)/4
    index_dict[depth] = title + '|' + title_path
    target = tree
    search_depth = 0;
    while(search_depth < depth):
        target = target[index_dict[search_depth]]
        search_depth += 1
    target[index_dict[depth]] = OrderedDict()


def pandocGenerate(title_path, depth):
    command = "pandoc -s -f markdown -t docbook " + title_path.encode('utf-8') + ".md -o " + output_dir_zh.encode('utf-8') + "/" + title_path.encode('utf-8') + ".xml --template " + os.path.dirname(os.path.abspath(sys.argv[0]))
    if depth == 1:
        command += "/chapter.docbook"
    else:
        command += "/default.docbook"
    print command
    if not os.path.exists(title_path.encode('utf-8') + ".md"):
        if not os.path.exists(os.path.dirname(title_path.encode('utf-8'))):
            os.mkdir(os.path.dirname(title_path.encode('utf-8')))
        open(title_path.encode('utf-8') + ".md", 'w').close()
    os.system(command)


def proccessDockbook(tree, depth, p_title, p_title_path, output_file):
    if tree:
        if depth == 1:
            output_file.write("<?xml version='1.0' encoding='utf-8' ?>\n")
            output_file.write("<!DOCTYPE section [\n")
            output_file.write("<!ENTITY % openstack SYSTEM \"administrator-guide.ent\">\n")
            output_file.write("%openstack;\n")
            output_file.write("]>\n")
            output_file.write("<chapter xmlns=\"http://docbook.org/ns/docbook\"\n")
            output_file.write("  xmlns:xi=\"http://www.w3.org/2001/XInclude\"\n")
            output_file.write("  xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n")
            output_file.write("  version=\"5.0\"\n")
            output_file.write("  xml:id=\"" + p_title_path.replace('/', '_') + "\">\n")
            output_file.write("  <title>" + p_title + "</title>\n")
        if depth > 1:
            output_file.write("<section xmlns=\"http://docbook.org/ns/docbook\"\n")
            output_file.write("  xmlns:xi=\"http://www.w3.org/2001/XInclude\"\n")
            output_file.write("  xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n")
            output_file.write("  version=\"5.0\">\n")
            output_file.write("<title>" + p_title + "</title>\n")
        for key in tree:
            title, title_path = key.split('|')
            title_path_index = title_path
            if depth > 0:
                title_path_index = title_path[title_path.index('/') + 1:]
            output_file.write("  <xi:include href=\"" + title_path_index + ".xml\"/>\n")
            if not os.path.exists(os.path.dirname(output_dir_zh + '/' + title_path)):
                os.mkdir(os.path.dirname(output_dir_zh + '/' + title_path))
            new_file = codecs.open(output_dir_zh + '/' + title_path + ".xml", 'w', 'utf-8')
            proccessDockbook(tree[key], depth + 1, title, title_path, new_file)
            new_file.close()
        if depth > 1:
            output_file.write("</section>\n")
        if depth == 1:
            output_file.write("</chapter>\n")
    else:
        pandocGenerate(p_title_path, depth)


def proccessSUMMARYmd():
    output_prefix(output_file)
    with codecs.open(input_file, 'r', 'utf-8') as f:
        for line in f:
            proccessSectionTree(output_file, line)
    proccessDockbook(tree, 0, None, None, output_file)
    output_suffix(output_file)
    output_file.close()


def proccessMiscPublicanFiles():
    ent = open(output_dir_zh + '/administrator-guide.ent', 'w')
    ent.write("""\
<!ENTITY PRODUCT "Documents">
<!ENTITY BOOKID "administrator-guide">
<!ENTITY YEAR "2014">
<!ENTITY HOLDER "| Comapny name |">
<!ENTITY OVIRT " product name ">
<!ENTITY OVIRT_STORAGE " product Storage ">
<!ENTITY MANAGER "manager">
<!ENTITY NODE "node">
<!ENTITY DEFAULT_LOGICAL_NETWORK "management network">
""")
    ent.close()

proccessSUMMARYmd()
proccessMiscPublicanFiles()
