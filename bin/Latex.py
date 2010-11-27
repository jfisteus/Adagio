#!/usr/bin/python
# -*- coding: UTF-8 -*-#
#
# Author: Abelardo Pardo (abelardo.pardo@uc3m.es)
#
#
#
import os, re, sys, glob

import Ada, Directory, I18n, Dependency, AdaRule

# Prefix to use for the options
module_prefix = 'Latex'

# List of tuples (varname, default value, description string)
options = [
    ('exec', 'latex', I18n.get('name_of_executable')),
    ('output_format', 'pdf', I18n.get('output_format')),
    ('extra_arguments', '', I18n.get('extra_arguments').format('LaTeX'))
    ]

documentation = {
    'en' : """
    Executes LaTeX with the given extra arguments over "files".
    """}

has_executable = AdaRule.which(next(b for (a, b, c) in options if a == 'exec'))

def Execute(target, directory, pad = ''):
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
        return

    # Print msg when beginning to execute target in dir
    print pad + 'BB', target

    # Prepare the command to execute
    commandPrefix = [directory.getWithDefault(target, 'exec'), 
                     '-output-format=' + directory.getWithDefault(target, 
                                                                  'dst_dir')
                     '-output-directory=' + \
                         directory.getWithDefault(target, 'output_format'),
                     directory.getWithDefault(target, 'extra_arguments')]
    
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
        command = commandPrefix + [datafile]
        
        # Perform the execution
        AdaRule.doExecution(target, directory, command, datafile, dstFile, 
                            Ada.userLog)

    print pad + 'EE', target
    return

def clean(target, directory, pad):
    """
    Clean the files produced by this rule
    """
    
    Ada.logInfo(target, directory, 'Cleaning')

    # Get the files to process
    toProcess = AdaRule.getFilesToProcess(target, directory)
    if toProcess == []:
        return

    # Print msg when beginning to execute target in dir
    print pad + 'BB', target + '.clean'

    # Loop over all source files to process
    dstDir = directory.getWithDefault(target, 'dst_dir')
    outputFormat = directory.getWithDefault(target, 'output_format')
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

        print I18n.get('removing').format(os.path.basename(dstFile))
        os.remove(dstFile)

    print pad + 'EE', target + '.clean'
    return

# Execution as script
if __name__ == "__main__":
    Execute(module_prefix, Directory.getDirectoryObject('.'))