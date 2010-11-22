#!/usr/bin/python
# -*- coding: UTF-8 -*-#
#
# Author: Abelardo Pardo (abelardo.pardo@uc3m.es)
#
#
#
import os, logging, sys, getopt, datetime, locale, ConfigParser

import Ada, I18n, Properties, Directory
# import Ada, Directory, I18n, Xsltproc

# Global settings for logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('adado')

def main():
    """
    The manual page for this method is inside the localization package. Check
    the proper [ĺang].py file.
    """

    # Fix the output encoding when redirecting stdout
    if sys.stdout.encoding is None:
        (lang, enc) = locale.getdefaultlocale()
        if enc is not None:
            (e, d, sr, sw) = codecs.lookup(enc)
            # sw will encode Unicode data to the locale-specific character set.
            sys.stdout = sw(sys.stdout)

    #######################################################################
    #
    # Initialization of all the required variables
    #
    #######################################################################
    Ada.initialize()

    #######################################################################
    #
    # OPTIONS
    #
    #######################################################################
    targets = []
    optionsToSet = []

    # Swallow the options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:s:t:hx",
                                   ["dir="])
    except getopt.GetoptError, e:
        print e.msg
        print I18n.get('__doc__')
        sys.exit(2)

    # Parse the options
    for optstr, value in opts:
        # Debug option
        if optstr == "-d":
            # An integer is required
            try:
                numValue = int(value)
            except ValueError, e:
                logger.error(I18n.get('incorrect_debug_option'))
                sys.exit(3)
            Ada.config_defaults['debug_level'] = value

        # Dump the manual page
        elif optstr == "-h" or optstr == "-x":
            print I18n.get('__doc__')
            sys.exit(3)

        # Set a value in the environment
        elif optstr == "-s":
            sname_value = value.split()
            # If incorrect number of arguments, stop processing
            if len(sname_value) != 3:
                print I18n.get('incorrect_arg_num').format('-s option')
                print I18n.get('__doc__')
                sys.exit(3)
            optionsToSet.append(' '.join(sname_value))
        # Set the targets
        elif optstr == "-t":
            # Extend the list of targets to process
            targets.extend(value.split())

    # Invoke a function that traverses the options and checks that they have the
    # right type (integers, floats, date/time, et.
    pass # TO BE IMPLEMENTED

    # The rest of the arguments are the targets
    targets = args

    # Print Reamining arguments. If none, just stick the current dir
    logger.debug('Targets: ' + ' '.join(targets))

    #######################################################################
    #
    # MAIN PROCESSING
    #
    #######################################################################

    # Create the directory
    dirObject = Directory.getDirectoryObject(os.getcwd(),
                                             sorted(optionsToSet))
        
    # Execute its targets
    dirObject.Execute(targets)

# Execution as script
if __name__ == "__main__":
    main()
