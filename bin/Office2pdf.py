#!/usr/bin/python
# -*- coding: UTF-8 -*-#
#
# Author: Abelardo Pardo (abelardo.pardo@uc3m.es)
#
#
#
import os, re, sys

import Ada, Directory, I18n, AdaRule

# Prefix to use for the options
module_prefix = 'office2pdf'

# List of tuples (varname, default value, description string)
options = [
    ('exec', 'soffice', I18n.get('name_of_executable')),
    ('extra_arguments', '', I18n.get('extra_arguments').format('OpenOffice'))
    ]

documentation = {
    'en' : """
    This target invokes OpenOffice to obtain a PDF version of the given
    files. It assumes that there is a Macro already installed with name
    SaveAsPDF.
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

    # Loop over all source files to process
    executable = directory.getWithDefault(target, 'exec')
    extraArgs = directory.getWithDefault(target, 'extra_arguments')
    command = [executable, '-nologo', '-invisible', '-headless']
    command.extend(extraArgs.split())
    dstDir = directory.getWithDefault(target, 'src_dir')
    for datafile in toProcess:
        Ada.logDebug(target, directory, ' EXEC ' + datafile)

        # If file not found, terminate
        if not os.path.isfile(datafile):
            print I18n.get('file_not_found').format(datafile)
            sys.exit(1)

        # Derive the destination file name
        dstFileName = os.path.splitext(os.path.basename(datafile))[0] + \
            '.pdf'
        dstFile = os.path.abspath(os.path.join(dstDir, dstFileName))

        # Perform the execution
        command.append('macro:///Tools.MSToPDF.ConvertMSToPDF(' + datafile + ')')
        AdaRule.doExecution(target, directory, command, datafile, None,
                            stdout = Ada.userLog)
        command.pop(-1)

    # End of loop over all src files

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

    # Loop over all the source files
    dstDir = directory.getWithDefault(target, 'src_dir')
    for datafile in toProcess:

        # If file not found, terminate
        if not os.path.isfile(datafile):
            print I18n.get('file_not_found').format(datafile)
            sys.exit(1)

        # Derive the destination file name
        dstFile = os.path.splitext(os.path.basename(datafile))[0] + \
            '.pdf'
        dstFile = os.path.abspath(os.path.join(dstDir, dstFile))

        if not os.path.exists(dstFile):
            continue

        AdaRule.remove(dstFile)

# Execution as script
if __name__ == "__main__":
    Execute(module_prefix, Directory.getDirectoryObject('.'))