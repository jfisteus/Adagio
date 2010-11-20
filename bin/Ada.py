#!/usr/bin/python
# -*- coding: UTF-8 -*-#
#
# Author: Abelardo Pardo (abelardo.pardo@uc3m.es)
#
#
#
import os, logging, sys, locale, ordereddict, re, datetime

import Directory, Properties, I18n

# Get language and locale for locale option
(lang, enc) = locale.getdefaultlocale()

# Prefix to use for the options
module_prefix = 'ada'

# Set the logger for this module
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(module_prefix)

################################################################################
#
# ConfigParser:
#
# Global variable in this module with name options
#
# SECTIONS
#
# Ada: variables affecting the overall set of operations.
# Xsltproc: apply xsltproc with options/style/xmlfile
#
################################################################################
config_defaults = {
    'debug_level':      '40',
    'version':          '10.03.1',
    'locale':           lang[0:2],
    'home':             os.path.abspath(os.getcwd()),
    'basedir':          os.path.abspath(os.getcwd()),
    'src_dir':          os.path.abspath(os.getcwd()),
    'dst_dir':          os.path.abspath(os.getcwd()),
    'files':            '',
    'property_file':    'Properties.txt',
    'project_file':     'Ada.properties',
    'file_separator':   os.path.sep,
    'current_datetime': str(datetime.datetime.now()),
    'profile_revision': ''
}

# List of tuples (varname, default value, description string)
options = [
    # Minimum version number required
    ('minimum_version', '', I18n.get('ada_minimum_version')),

    # Maximum version number required
    ('maximum_version', '', I18n.get('ada_maximum_version')),

    # Exact version required
    ('exact_version', '', I18n.get('ada_exact_version'))
    ]

documentation = {
    'en': """
     Documentation explaining the basic ada variables. To be written.
     """}

# Directory where ADA is installed
home = os.path.dirname(os.path.abspath(sys.argv[0]))
home = os.path.abspath(os.path.join(home, '..'))
if not os.path.isdir(home):
    logger.error('ERROR: ada.home is not a directory')
    print I18n.get('cannot_detect_ada_home')
    sys.exit(1)

def initialize():
    """
    Function that initializes all the required variables before doing anything
    else. This function is executed even before the options are parsed. It
    receives the ConfigParser object storing all the values.

    Returns a boolean stating if there had been problems
    """

    global home

    # Insert the definition of catalogs in the environment
    os.environ["XML_CATALOG_FILES"] = os.path.join(home, 'DTDs',
                                                   'catalog')

def Execute(target, directory):
    """
    Execute the rule in the given directory
    """

    global module_prefix
    global documentation

    logger.info(module_prefix + ':' + target + ':' + directory.current_dir)

    # If requesting dump, bypass execution
    if re.match('(.+)?dump', target):
        dumpOptions(directory)
        return

    if re.match('(.+)?help', target):
        msg = documentation[directory.options.get(module_prefix, 'locale')]
        if msg != None:
            print I18n.get('doc_preamble').format(module_prefix)
            print msg
        else:
            print I18n.get('no_doc_for_rule').format(module_prefix)
        return

    return

def dumpOptions(directory):
    """
    Dump the value of the options affecting the computations
    """

    global options
    global module_prefix

    print I18n.get('var_preamble').format(module_prefix)

    for sn in directory.options.sections():
        if sn.startswith(module_prefix):
            for (on, ov) in sorted(directory.options.items(sn)):
                print ' -', module_prefix + '.' + on, '=', ov


# Execution as script
if __name__ == "__main__":
    Execute(module_prefix, Directory.getDirectoryObject('.'))
