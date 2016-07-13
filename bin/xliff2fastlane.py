#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Juraj Michalek - Y Soft RnD - http://www.ysofters.com
# MIT License - see LICENSE.txt

import io
import os
import sys
import xml.etree.ElementTree as ET

def write_file_content(path, file_name, content):
    """Read content of file."""
    if not os.path.exists(path):
        os.makedirs(path)
    f = io.open(path + file_name, "w", encoding = 'utf-8')
    f.write(content)
    f.close()

def parse_xliff_for_os(target_dir_name, os_name, target_language, body_element):
    """Convert XLIFF for OS into files for Fastlane."""
    for trans_unit in body_element:
        trans_unit_id = trans_unit.attrib['id']
        trans_unit_target = ''
        for trans_unit_element in trans_unit:
            if trans_unit_element.tag.endswith('target'):
                trans_unit_target = u'' + trans_unit_element.text
                break
        resource_path = target_dir_name + '/' + os_name + '/metadata/' + target_language + '/'
        resource_file_name = trans_unit_id + '.txt'
        write_file_content(resource_path, resource_file_name, trans_unit_target)

if len(sys.argv) < 2:
    print "Specify parameters:"
    print " source xliff files"
    print " target directory"
    sys.exit(1)

xliff_file_name = sys.argv[1]
target_dir_name = sys.argv[2]

source_tree = ET.parse(xliff_file_name)
source_root = source_tree.getroot()
xliff_content = source_root.getchildren()

for xliff_data in xliff_content:
    parse_xliff_for_os(target_dir_name, xliff_data.attrib['original'], xliff_data.attrib['target-language'], xliff_data.getchildren()[0])


