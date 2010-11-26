#!/usr/bin/python
# -*- coding: UTF-8 -*-#
#
# Author: Abelardo Pardo (abelardo.pardo@uc3m.es)
#
#
#
import os, re, sys, subprocess

import Ada, Directory, I18n, Dependency, AdaRule

# Prefix to use for the options
module_prefix = 'inkscape'

# List of tuples (varname, default value, description string)
options = [
    ('exec', 'inkscape', I18n.get('name_of_executable')),
    ('output_format', 'png', I18n.get('output_format')),
    ('extra_arguments', '', I18n.get('extra_arguments').format('Inkscape'))
    ]

documentation = {
    'en' : """
    Uses inkscape to transform the "files" into the format given in
    "output_format". Available formats are:
    - png
    - eps
    - ps
    - pdf

    The values in "extra_arguments" are given directly to inkscape
    """}

has_executable = AdaRule.which(next(b for (a, b, c) in options if a == 'exec'))

def Execute(target, directory, pad = ''):
    """
    Execute the rule in the given directory
    """

    global module_prefix
    global documentation
    global has_executable

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

    # Print msg when beginning to execute target in dir
    print pad + 'BB', target

    # Get formats and check if they are empty
    formats = directory.getWithDefault(target, 'output_format').split()
    if formats == []:
        print I18n.get('no_var_value').format('output_format')
        print pad + 'EE', target
        return

    # Loop over all source files to process
    executable = directory.getWithDefault(target, 'exec')
    extraArgs = directory.getWithDefault(target, 'extra_arguments')
    dstDir = directory.getWithDefault(target, 'dst_dir')
    for datafile in toProcess:
        Ada.logDebug(target, directory, ' EXEC ' + datafile)

        # If file not found, terminate
        if not os.path.isfile(datafile):
            print I18n.get('file_not_found').format(datafile)
            sys.exit(1)

        # Loop over formats
        for format in formats:
            # Derive the destination file name
            dstFile = os.path.splitext(os.path.basename(datafile))[0] + \
                '.' + format
            dstFile = os.path.abspath(os.path.join(dstDir, dstFile))

            # Check for dependencies!
            Dependency.update(dstFile, set([datafile] + directory.option_files))

            # If the destination file is up to date, skip the execution
            if Dependency.isUpToDate(dstFile):
                print I18n.get('file_uptodate').format(os.path.basename(dstFile))
                continue

            # Proceed with the execution of xslt
            print I18n.get('producing').format(os.path.basename(dstFile))

            command = [executable, '--export-' + format + '=' + dstFile]
            command.extend(extraArgs.split())
            command.append(datafile)

            Ada.logDebug(target, directory, 'Popen: ' + ' '.join(command))
            try:
                pr = subprocess.Popen(command, stdout = Ada.userLog)
                pr.wait()
            except:
                print I18n.get('severe_exec_error').format(executable)
                print I18n.get('exec_line').format(' '.join(command))
                sys.exit(1)

            # Update the dependencies of the newly created file
            Dependency.update(dstFile)

    print pad + 'EE', target
    return

def clean(target, directory, pad):
    """
    Clean the files produced by this rule
    """

    Ada.logInfo(target, directory, 'Cleaning')

    # Get formats and check if they are empty
    formats = directory.getWithDefault(target, 'output_format').split()
    if formats == []:
        Ada.logDebug(target, directory, 
                     I18n.get('no_var_value').format('output_format'))
        return

    # Get the files to process
    toProcess = AdaRule.getFilesToProcess(target, directory)
    if toProcess == []:
        return

    # Print msg when beginning to execute target in dir
    print pad + 'BB', target + '.clean'

    # Loop over all the source files
    dstDir = directory.getWithDefault(target, 'dst_dir')
    for datafile in toProcess:

        # If file not found, terminate
        if not os.path.isfile(datafile):
            print I18n.get('file_not_found').format(datafile)
            sys.exit(1)

        # Loop over formats
        for format in formats:
            # Derive the destination file name
            dstFile = os.path.splitext(os.path.basename(datafile))[0] + \
                '.' + format
            dstFile = os.path.abspath(os.path.join(dstDir, dstFile))

            if not os.path.exists(dstFile):
                continue

            print I18n.get('removing').format(os.path.basename(dstFile))
            os.remove(dstFile)

# Execution as script
if __name__ == "__main__":
    Execute(module_prefix, Directory.getDirectoryObject('.'))