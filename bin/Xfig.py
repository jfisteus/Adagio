#!/usr/bin/python
# -*- coding: UTF-8 -*-#
#
# Copyright (C) 2010 Carlos III University of Madrid
# This file is part of the ADA: Agile Distributed Authoring Toolkit

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
import os, sys, glob

import Ada, Directory, I18n, Dependency, AdaRule

# Prefix to use for the options
module_prefix = 'xfig'

# List of tuples (varname, default value, description string)
options = [
    ('exec', 'fig2dev', I18n.get('name_of_executable')),
    ('output_format', 'png', I18n.get('output_format')),
    ('extra_arguments', '', I18n.get('extra_arguments').format('Fig2dev'))
    ]

documentation = {
    'en' : """
    Executes fig2dev to translate *.fig figures to the given "output_format" of
    all the "files".
    """}

has_executable = AdaRule.which(next(b for (a, b, c) in options if a == 'exec'))

def Execute(target, directory):
    """
    Execute the rule in the given directory
    """

    global has_executable

    # If the executable is not present, notify and terminate
    if not has_executable:
        print I18n.get('no_executable').format(options['exec'])
        if directory.options.get(target, 'partial') == '0':
            sys.exit(1)
        return

    # Get the files to process, if empty, terminate
    toProcess = AdaRule.getFilesToProcess(target, directory)
    if toProcess == []:
        return

    # Prepare the command to execute
    executable = directory.getWithDefault(target, 'exec')
    dstDir = directory.getWithDefault(target, 'dst_dir')
    outputFormat = directory.getWithDefault(target, 'output_format')
    if outputFormat == '':
        print I18n.get('empty_output_format').format(target)
        sys.exit(1)

    # Loop over all source files to process
    for datafile in toProcess:
        Ada.logDebug(target, directory, ' EXEC ' + datafile)

        # If file not found, terminate
        if not os.path.isfile(datafile):
            print I18n.get('file_not_found').format(datafile)
            sys.exit(1)

        # Derive the destination file name
        dstFile = os.path.splitext(os.path.basename(datafile))[0] + \
            '.' + outputFormat
        dstFile = os.path.abspath(os.path.join(dstDir, dstFile))
                                                   
        # Add the input file to the command
        command = [executable, '-L', outputFormat]
        command.extend(directory.getWithDefault(target, 
                                                'extra_arguments').split())
        command.extend([datafile, dstFile])
        
        # Perform the execution
        AdaRule.doExecution(target, directory, command, datafile, dstFile, 
                            Ada.userLog, Ada.userLog)

    return

def clean(target, directory):
    """
    Clean the files produced by this rule
    """
    
    Ada.logInfo(target, directory, 'Cleaning')

    # Get the files to process
    toProcess = AdaRule.getFilesToProcess(target, directory)
    if toProcess == []:
        return

    dstDir = directory.getWithDefault(target, 'dst_dir')
    outputFormat = directory.getWithDefault(target, 'output_format')
    if outputFormat == '':
        print I18n.get('empty_output_format').format(target)
        sys.exit(1)

    # Loop over all source files to process
    for datafile in toProcess:

        # If file not found, terminate
        if not os.path.isfile(datafile):
            print I18n.get('file_not_found').format(datafile)
            sys.exit(1)

        # Derive the destination file name
        dstFile = os.path.splitext(os.path.basename(datafile))[0] + \
            '.' + outputFormat
        dstFile = os.path.abspath(os.path.join(dstDir, dstFile))
                                                   
        if not os.path.exists(dstFile):
            continue

        AdaRule.remove(dstFile)

    return

# Execution as script
if __name__ == "__main__":
    Execute(module_prefix, Directory.getDirectoryObject('.'))