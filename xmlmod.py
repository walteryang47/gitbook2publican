# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as xmlParser
from lxml import etree
from StringIO import StringIO
import os
import sys

xmlfile_path = os.path.abspath(sys.argv[1])

xml_doc = xmlParser.parse(xmlfile_path)
root_element = xml_doc.getroot()

print xmlfile_path


def writexml(xml_doc):
  contents = None
  with open(xmlfile_path, 'w') as f:
    xml_doc.write(f, encoding="UTF-8")
  with open(xmlfile_path, 'r') as f:
    contents = f.readlines()
  with open(xmlfile_path, 'w') as f:
    contents.insert(1, """\
<!DOCTYPE chapter PUBLIC "-//OASIS//DTD DocBook XML V4.5//EN" "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd" [
<!ENTITY % BOOK_ENTITIES SYSTEM "administrator-guide.ent">
%BOOK_ENTITIES;
]>

""")
    contents = "".join(contents)
    f.write(contents)



for elementr in root_element.iter('section'):
  for element in elementr:
    if element.tag == 'blockquote':
      for child in element:
        if child.tag == 'para':
          for childc in child:
            if childc.tag == 'emphasis' and childc.text == u'注意':
              print 'hehehe'
              element.remove(child)
              element.tag = 'note'
              writexml(xml_doc)
            elif childc.tag == 'emphasis' and childc.text == u'重要':
              print 'hehehe'
              element.remove(child)
              element.tag = 'important'
              writexml(xml_doc)
            elif childc.tag == 'emphasis' and childc.text == u'警告':
              print 'hehehe'
              element.remove(child)
              element.tag = 'warning'
              writexml(xml_doc)

