#!/usr/bin/python
# -*- coding: UTF-8 -*-#
#
# Author: Abelardo Pardo (abelardo.pardo@uc3m.es)
#
#
#
import os, re, sys, datetime

import Ada, Directory, I18n, Dependency, AdaRule, Copy

# Prefix to use for the options
module_prefix = 'export'

# List of tuples (varname, default value, description string)
options = [
    ('dst_dir', '', I18n.get('rule_dst_dir')),
    ('date_format', 'yyyy/MM/dd HH:mm:ss', I18n.get('date_format')),
    ('begin', '', I18n.get('export_begin')),
    ('end', '', I18n.get('export_end')),
    ('open', '1', I18n.get('export_open')),
    ('profile_revisions', '', I18n.get('export_profile_revisions'))
    ]

documentation = {
    'en' : """
    This rule copies the "files" in "src_dir" to "dst_dir" if ALL the following
    conditions are satisfied:

    - "begin" is empty or the current time is greater than "begin"
    - "end" is empty or the current time is less than "end"
    - "open" has the value 1
    - "profile_revisions" is empty or contains %(profile_revision)s

    The default values of these variables are:
    - open : '1'
    - begin : ''
    - end : ''
    - profile_revisions : ''

    The dates are parsed following the format stored in "data_format"

    So, in principle, if an export section is defined without touching these
    variables, it is performing the export.

    These conditions apply also to the "clean" target.
    """}

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

    # Get the files to process, if empty, terminate
    toProcess = AdaRule.getFilesToProcess(target, directory)
    if toProcess == []:
        return

    # Print msg when beginning to execute target in dir
    print pad + 'BB', target

    # Check the condition
    dstDir = directory.getWithDefault(target, 'dst_dir')
    if not evaluateCondition(target, directory, dstDir, pad):
        print pad + 'EE', target
        return

    # If we are here, the export may proceed!
    Copy.doCopy(target, directory, toProcess, dstDir)

    print pad + 'EE', target
    return

def clean(target, directory, pad):
    """
    Clean the files produced by this rule. The target is executed under the same
    rules explained in the documentation.
    """

    Ada.logInfo(target, directory, 'Cleaning')

    # Get the files to process
    toProcess = AdaRule.getFilesToProcess(target, directory)
    if toProcess == []:
        return

    # Print msg when beginning to execute target in dir
    print pad + 'BB', target + '.clean'

    # Check the condition
    dstDir = directory.getWithDefault(target, 'dst_dir')
    if not evaluateCondition(target, directory, dstDir, pad):
        print pad + 'EE', target
        return

    # If we are here, the export may proceed!
    Copy.doClean(target, directory, toProcess, dstDir)

    print pad + 'EE', target + '.clean'
    return

def evaluateCondition(target, directory, dstDir, pad):
    """
    Evaluates the condition to allow the execution of any export target.
    """

    # If the dst_dir is empty, do not export
    if dstDir == '':
        print I18n.get('export_no_dst')
        return False

    # Check part 1 of the rule: open must be 1
    openData = directory.getWithDefault(target, 'open')
    openValue = openData == '1'
    if not openValue:
        print I18n.get('export_not_open').format(openData)
        return False

    # Get current date/time
    now = datetime.datetime.now()

    # Get the date_format
    dateFormat = directory.getWithDefault(target, 'date_format')

    # Check part 2 of the rule: begin date is before current date
    beginDate = directory.getWithDefault(target, 'begin')
    if beginDate != '':
        if checkDateFormat(beginDate, dateFormat) < now:
            print I18n.get('export_closed_begin').format(beginDate)
            return False

    # Check part 3 of the rule: end date is after current date
    endDate = directory.getWithDefault(target, 'end')
    if endDate != '':
        if now < checkDateFormat(endDate, dateFormat):
            print I18n.get('export_closed_end').format(endDate)
            return False

    # Check part 4 of the rule: profile_revision must be in profile_revisions
    revisionsData = directory.getWithDefault(target, 'profile_revisions')
    if revisionsData != '':
        thisRevision = directory.options.get(Ada.module_prefix,
                                             'profile_revision')
        if not (thisRevision in set(revisionData.split())):
            print I18n.get('export_not_revision').format(thisRevision)
            return False

    return True

def checkDateFormat(d, f):
    """
    Check if the date d is compliant with the format f. If not, terminate with a
    message.

    Returns the datetime object with the date
    """
    try:
       result = datetime.datetime.strptime(d, f)
    except ValueError, e:
       print I18n.get('date_incorrect_format').format(d, f)
       sys.exit(1)

    return result

# Execution as script
if __name__ == "__main__":
    Execute(module_prefix, Directory.getDirectoryObject('.'))