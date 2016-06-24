#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Juraj Michalek - Y Soft RnD - http://www.ysofters.com
# MIT License - see LICENSE.txt

import io
import os
import sys
import glob
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import xml.dom.minidom

def base_file_name(long_path):
    """Reduce file path to base file name without extension"""
    return long_path.split('/')[-1].split('.')[0]

def get_file_content(path):
    """Read content of file."""
    f = io.open(path, "r", encoding = 'utf-8')
    data = ""
    for line in f:
        data += line
    f.close()
    return data

def get_target_resource_path(prefix_path, language):
    """
        Return path with full language if it exist.
        Return shorter path in case of e.g. ro if it exists.
        Return path to english version.
    """
    long_path = prefix_path + "/" + language
    if os.path.exists(long_path):
        return long_path
    short_path = prefix_path + "/" + language.split('-')[0]
    if os.path.exists(short_path):
        return short_path
    return prefix_path + "/en-US"


def parse_resources_for_os(os_name, xliff_element):
    """Parse resources for specific OS and append it to XLIFF element."""

    meta_path = source_dir_name + "/" + os_name + "/metadata"
    source_files = glob.glob(meta_path  + "/en-US/*.txt")
    locale_keys = map(base_file_name, source_files)

    xliff_data = {}

    target_resource_path = get_target_resource_path(meta_path, target_language)

    for locale_key in locale_keys:
        name = locale_key
        value = get_file_content(meta_path + "/en-US/" + name + ".txt")
        target = get_file_content(target_resource_path + "/" + name + ".txt")

        # Do not include keys for empty resoruces
        if len(value) == 0:
            continue

        xliff_data[name] = {
            'source': value,
            'target': target
        }


    file_element = ET.SubElement(xliff_element, 'file')
    file_element.attrib['source-language'] = 'en-US'
    file_element.attrib['target-language'] = target_language
    file_element.attrib['datatype'] = 'plaintext'
    file_element.attrib['original'] = os_name

    bodyElement = ET.SubElement(file_element, 'body')
    comment_counter = 0
    for unit_id in xliff_data:
        trans_unit_element = ET.SubElement(bodyElement, 'trans-unit')
        trans_unit_element.attrib['id'] = unit_id
        trans_unit_source = ET.SubElement(trans_unit_element, 'source')
        trans_unit_source.text = xliff_data[unit_id]['source']

        trans_unit_target = ET.SubElement(trans_unit_element, 'target')
        if xliff_data[unit_id].has_key('target'):
            trans_unit_target.text = xliff_data[unit_id]['target']
        else:
            print "Target missing, adding untranslated for:", unit_id
            trans_unit_target.text = trans_unit_source.text

        if trans_unit_source.text != trans_unit_target.text:
            trans_unit_element.attrib['approved'] = 'yes'
            trans_unit_target.attrib['state'] = 'translated'
        else:
            trans_unit_element.attrib['approved'] = 'no'
            trans_unit_target.attrib['state'] = 'new'

if len(sys.argv) < 3:
    print "Specify parameters:"
    print " source directory with .txt files"
    print " result xliff files"
    print " target language code"
    sys.exit(1)

source_dir_name = sys.argv[1]
xliff_file_name = sys.argv[2]
target_language = sys.argv[3]

namespace="urn:oasis:names:tc:xliff:document:1.1"
ET.register_namespace('', namespace)
xliff_element = ET.Element('xliff', xmlns=namespace)
xliff_element.attrib['version'] = '1.1'


parse_resources_for_os('iOS', xliff_element)
parse_resources_for_os('Android', xliff_element)

xml = xml.dom.minidom.parseString(tostring(xliff_element, encoding='UTF-8', method='html'))

output = open(xliff_file_name, 'wb')
output.write(xml.toprettyxml(indent='  ', encoding='UTF-8'))
output.close()

