#!/usr/bin/python
# -*- coding: UTF-8 -*-#
#
# Copyright (C) 2008 Carlos III University of Madrid
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
import os, re, sys

import Ada, Directory, I18n, AdaRule

# Prefix to use for the options
module_prefix = 'convert'

# List of tuples (varname, default value, description string)
options = [
    ('exec', 'convert', I18n.get('name_of_executable')),
    ('output_format', 'png', I18n.get('output_format')),
    ('geometry', '', I18n.get('convert_geometry')),
    ('crop_option', '', I18n.get('convert_crop_option')),
    ('extra_arguments', '', I18n.get('extra_arguments').format('Convert'))
    ]

documentation = {
    'en' : """
    Uses the "convert" program scale images. The value of "geometry" is treated
    as a space separated list of geometries of the form hxw. Each file in
    "files" is then scaled for every value in geometry. Furthermore, the value
    in "crop_option" can be used to crop the image. "extra_arguments" are passed
    directly to convert. Convert is thus invoked as:

    convert -scale [geometry] [convert_option] [extra_args] 
            input.xxx output_geometry.xxx

    """}

has_executable = AdaRule.which(next(b for (a, b, c) in options if a == 'exec'))

def Execute(target, directory, pad = None):
    """
    Execute the rule in the given directory
    """

    global module_prefix
    global documentation

    Ada.logInfo(target, directory, 'Enter ' + directory.current_dir)

    # Detect and execute "special" targets
    if AdaRule.specialTargets(target, directory, documentation,
                                     module_prefix, clean, pad):
        return

    # If the executable is not present, notify and terminate
    if not has_executable:
        print I18n.get('no_executable').format(options['exec'])
        if directory.options.get(target, 'partial') == '0':
            sys.exit(1)
        return

    # Get the files to process, if empty, terminate
    toProcess = AdaRule.getFilesToProcess(target, directory)
    if toProcess == []:
        Ada.logDebug(target, directory, I18n.get('no_file_to_process'))
        return

    if pad == None:
	pad = ''

    # Print msg when beginning to execute target in dir
    print pad + 'BB', target

    # Get geometry
    geometries = directory.getWithDefault(target, 'geometry').split()
    if geometries == []:
        print I18n.get('no_var_value').format('geometry')
        print pad + 'EE', target
        return

    # Loop over all source files to process
    executable = directory.getWithDefault(target, 'exec')
    extraArgs = directory.getWithDefault(target, 'extra_arguments')
    convertCrop = directory.getWithDefault(target, 'crop_option')
    dstDir = directory.getWithDefault(target, 'dst_dir')
    for datafile in toProcess:
        Ada.logDebug(target, directory, ' EXEC ' + datafile)

        # If file not found, terminate
        if not os.path.isfile(datafile):
            print I18n.get('file_not_found').format(datafile)
            sys.exit(1)

        # Loop over formats
        for geometry in geometries:
            # Derive the destination file name
            (fn, ext) = os.path.splitext(os.path.basename(datafile))
            dstFile = fn + '_' + geometry + ext
            dstFile = os.path.abspath(os.path.join(dstDir, dstFile))

            # Creat the command to execute (slightly non-optimal, because the
            # following function might NOT execute the process due to
            # dependencies
            command = [executable, '-scale', geometry]
            command.extend(convertCrop.split())
            command.extend(extraArgs.split())
            command.append(datafile)
            command.append(dstFile)

            # Perform the execution
            AdaRule.doExecution(target, directory, command, datafile, dstFile, 
                                Ada.userLog)

    print pad + 'EE', target
    return

def clean(target, directory, pad = None):
    """
    Clean the files produced by this rule
    """

    Ada.logInfo(target, directory, 'Cleaning')

    # Get the files to process
    toProcess = AdaRule.getFilesToProcess(target, directory)
    if toProcess == []:
        return

    if pad == None:
	pad = ''

    # Print msg when beginning to execute target in dir
    print pad + 'BB', target + '.clean'

    # Get geometry
    geometries = directory.getWithDefault(target, 'geometry').split()
    if geometries == []:
        print I18n.get('no_var_value').format('geometry')
        print pad + 'EE', target
        return

    # Loop over all the source files
    dstDir = directory.getWithDefault(target, 'dst_dir')
    for datafile in toProcess:

        # If file not found, terminate
        if not os.path.isfile(datafile):
            print I18n.get('file_not_found').format(datafile)
            sys.exit(1)

        # Loop over formats
        for geometry in geometries:
            # Derive the destination file name
            (fn, ext) = os.path.splitext(os.path.basename(datafile))
            dstFile = fn + '_' + geometry + ext
            dstFile = os.path.abspath(os.path.join(dstDir, dstFile))

            if not os.path.exists(dstFile):
                continue

            AdaRule.remove(dstFile)

    print pad + 'EE', target + '.clean'
    return

# Execution as script
if __name__ == "__main__":
    Execute(module_prefix, Directory.getDirectoryObject('.'))
