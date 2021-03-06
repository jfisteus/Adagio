#!/usr/bin/env python
# -*- coding: UTF-8 -*-#
#
# Copyright (C) 2010 Carlos III University of Madrid
# This file is part of Adagio: Agile Distributed Authoring Integrated Toolkit

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor
# Boston, MA  02110-1301, USA.
#
# Author: Abelardo Pardo (abelardo.pardo@uc3m.es)
#
import os, re, sys

import adagio, directory, i18n, rules, filecopy

# Prefix to use for the options
module_prefix = 'export'

# List of tuples (varname, default value, description string)
options = [
    ('dst_dir', '', i18n.get('rule_dst_dir'))
    ]

documentation = {
    'en' : """
    This rule copies the "files" in "src_dir" to "dst_dir" if ALL the following
    conditions are satisfied:

    - "enable_begin" is empty or the current time is greater than "enable_begin"
    - "enable_end" is empty or the current time is less than "enable_end"
    - "enable_open" has the value 1
    - "adagio.enabled_profiles" is empty or contains rule.enable_profile

    The default values of these variables are:
    - enable_open : '1'
    - enable_begin : ''
    - enable_end : ''
    - enable_profile : ''

    The dates are parsed following the format stored in "data_format"

    So, in principle, if an export section is defined without touching these
    variables, it is performing the export.

    These conditions apply also to the "clean" rule.
    """}

def Execute(rule, dirObj):
    """
    Execute the rule in the given directory
    """

    # Get the files to process, if empty, terminate
    toProcess = rules.getFilesToProcess(rule, dirObj)
    if toProcess == []:
        return

    # Check if dstDir is empty, in which case, there is nothing to do
    dstDir = dirObj.getProperty(rule, 'dst_dir')
    if dstDir == '':
        print i18n.get('export_no_dst')
        return

    # If we are here, the export may proceed!
    srcDir = dirObj.getProperty(rule, 'src_dir')
    filecopy.doCopy(rule, dirObj, toProcess, srcDir, dstDir)

    return

def clean(rule, dirObj):
    """
    Clean the files produced by this rule. The rule is executed under the same
    conditions explained in the documentation variable.
    """

    adagio.logInfo(rule, dirObj, 'Cleaning')

    # Get the files to process
    toProcess = rules.getFilesToProcess(rule, dirObj)
    if toProcess == []:
        return

    # Check the condition
    dstDir = dirObj.getProperty(rule, 'dst_dir')
    if dstDir == '':
        return

    # If we are here, the export may proceed!
    filecopy.doClean(rule, dirObj, toProcess,
                 dirObj.getProperty(rule, 'src_dir'), dstDir)

    return

