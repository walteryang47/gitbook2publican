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

    author_group = open(output_dir_zh + '/Author_Group.xml', 'w')
    author_group.write("""\
<?xml version='1.0' encoding='utf-8' ?>
<!DOCTYPE section [
<!ENTITY % openstack SYSTEM "administrator-guide.ent">
%openstack;
]>
<authorgroup xmlns="http://docbook.org/ns/docbook"
  xmlns:xi="http://www.w3.org/2001/XInclude"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  version="5.0">
    <author>
      <firstname>firstname</firstname>
      <surname>surname</surname>
      <affiliation>
        <orgname>orgname</orgname>
        <orgdiv>orgdiv</orgdiv>
      </affiliation>
      <email>walteryang47@gmail.com</email>
    </author>
</authorgroup>
""")
    author_group.close()

    book_info = open(output_dir_zh + '/Book_Info.xml', 'w')
    book_info.write("""\
<?xml version='1.0' encoding='utf-8' ?>
<!DOCTYPE section [
<!ENTITY % openstack SYSTEM "administrator-guide.ent">
%openstack;
]>
<bookinfo xmlns="http://docbook.org/ns/docbook"
  xmlns:xi="http://www.w3.org/2001/XInclude"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  version="5.0"
  xml:id="book-Documents-administrator-guide-administrator_guide">
    <title>administrator-guide</title>
    <subtitle>EayunOS 系统管理员手册</subtitle>
    <productname>EayunOS</productname>
    <productnumber>4.1</productnumber>
    <edition>0</edition>
    <pubsnumber>0</pubsnumber>
    <abstract>
        <para>
                  本手册会详细介绍如何管理虚拟化解决方案。
        </para>
    </abstract>
    <corpauthor>
        <inlinemediaobject>
            <imageobject>
                <imagedata fileref="Common_Content/images/title_logo.svg" format="SVG" />
            </imageobject>
        </inlinemediaobject>
    </corpauthor>
    <xi:include href="Common_Content/Legal_Notice.xml"/>
    <xi:include href="Author_Group.xml"/>
</bookinfo>
""")
    book_info.close()

    revision_his = open(output_dir_zh + '/Revision_History.xml', 'w')
    revision_his.write("""\
<?xml version='1.0' encoding='utf-8' ?>
<!DOCTYPE section [
<!ENTITY % openstack SYSTEM "administrator-guide.ent">
%openstack;
]>
<appendix xmlns="http://docbook.org/ns/docbook"
  xmlns:xi="http://www.w3.org/2001/XInclude"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  version="5.0"
  xml:id="appe-Documents-administrator-guide-Revision_History">
    <title>修订历史</title>
    <simpara>
        <revhistory>
            <revision>
                <revnumber>0.0-0</revnumber>
                <date>Mon Jun 9 2014</date>
                <author>
                    <firstname>firstname</firstname>
                    <surname>surname</surname>
                    <email>user@mail.com</email>
                </author>
                <revdescription>
                    <simplelist>
                        <member>revdescription</member>
                    </simplelist>
                </revdescription>
            </revision>
        </revhistory>
    </simpara>
</appendix>
""")
    revision_his.close()

    publican = open(output_dir + '/publican.cfg', 'w')
    publican.write("""\
# Config::Simple 5.09
# Wed Feb 12 18:43:21 2014

brand: eayun
type: Book
xml_lang: "zh-CN"
""")
    publican.close()

    publican = open(output_dir_zh + '/Preface.xml', 'w')
    publican.write("""\
<?xml version='1.0' encoding='utf-8' ?>
<!DOCTYPE section [
<!ENTITY % openstack SYSTEM "administrator-guide.ent">
%openstack;
]>
<preface xmlns="http://docbook.org/ns/docbook"
  xmlns:xi="http://www.w3.org/2001/XInclude"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  version="5.0"
  xml:id="pref-Documents-administrator-guide-Preface">
    <title>Preface</title>
    <xi:include href="Common_Content/Conventions.xml"/>
    <xi:include href="Feedback.xml">
    <xi:fallback>
    <xi:include href="Common_Content/Feedback.xml"/>
    </xi:fallback>
    </xi:include>
</preface>
""")
    publican.close()

    publican = open(output_dir_zh + '/Chapter-using-guide.xml', 'w')
    publican.write("""\
<?xml version='1.0' encoding='utf-8' ?>
<!DOCTYPE section [
<!ENTITY % openstack SYSTEM "administrator-guide.ent">
%openstack;
]>
<chapter xmlns="http://docbook.org/ns/docbook"
  xmlns:xi="http://www.w3.org/2001/XInclude"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  version="5.0"
  xml:id="chap-Documents-administrator-guide-Chapter-using-guide">
    <title>手册使用向导</title>
    <para>
        This is a test paragraph
    </para>
    <section id="sect-Documents-administrator-guide-Chapter-using-guide-Section_1">
        <title>阅读管理员手册前的准备</title>
        <para>
            This is a test paragraph in a section
        </para>
    </section>

    <section id="sect-Documents-administrator-guide-Chapter-using-guide-Section_2">
        <title>本手册的层次结构</title>
        <para>
            This is a test paragraph in Section 2
            <orderedlist>
                <listitem>
                    <para>
                        This is a test listitem.
                    </para>
                </listitem>
            </orderedlist>
        </para>
    </section>

    <section id="sect-Documents-administrator-guide-Chapter-using-guide-Section_3">
        <title>流程实例</title>
        <para>
        </para>
           <section id="sect-Documents-administrator-guide-Chapter-using-guide-Section_3-1">
                <title>概览</title>
                <para>
                </para>
           </section>
           <section id="sect-Documents-administrator-guide-Chapter-using-guide-Section_3-2">
                <title>流程示例之创建iscsi数据中心</title>
                <para>
                </para>
           </section>
           <section id="sect-Documents-administrator-guide-Chapter-using-guide-Section_3-3">
                <title>流程示例之负载</title>
                <para>
                </para>
           </section>
           <section id="sect-Documents-administrator-guide-Chapter-using-guide-Section_3-4">
                <title>流程示例之供用户组使用的模板</title>
                <para>
                </para>
           </section>
    </section>
</chapter>
""")
    publican.close()

proccessSUMMARYmd()
proccessMiscPublicanFiles()
