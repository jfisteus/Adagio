#!/usr/bin/python
# -*- coding: UTF-8 -*-#
#
# Author: Abelardo Pardo (abelardo.pardo@uc3m.es)
#
#
#
import os, logging, sys, getopt, datetime

import Directory, Properties, AdaRule, I18n

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
    initialize()

    #######################################################################
    #
    # OPTIONS
    #
    #######################################################################
    targets = []
    directories = []
    givenDictionary = {}

    # Swallow the options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:s:t:",
                                   ["dir="])
    except getopt.GetoptError, e:
        print e.msg
        print I18n.get('__doc__')
        sys.exit(2)

    # Parse the options
    for optstr, value in opts:
        # Debug option
        if optstr == "-d":
            Directory.globalVariables['ada.debug.level'] = value
            logging.basicConfig(level=int(value))

        # Set a value in the environment
        elif optstr == "-s":
            name_value = value.split()
            # If not enough arguments, stop processing
            if len(name_value) != 2:
                print I18n.get('incorrect_arg_num').format('-s option')
                print I18n.get('__doc__')
                sys.exit(2)
            # This option is stored in level B of the dictionary
            givenDictionary[name_value[0]] = name_value[1]

        # Set the targets
        elif optstr == "-t":
            # Extend the list of targets to process
            targets.extend(value.split())

    # Print Reamining arguments. If none, just stick the current dir
    loggin.debug('Remaning args: ' + str(args))
    if args == []:
        directories = [os.getcwd()]
    else:
        directories = args

    #######################################################################
    #
    # MAIN PROCESSING
    #
    #######################################################################
    logging.info('Start ADA processing ' + str(targets))

    # Remember the initial directory
    initialDir = os.getcwd()

    # Create the initial list of directories to process
    directories = map(lambda x: (x, ''), directories)
    executionChain = {}
    index = 0
    while index < len(directories):
        # Get the first dir in the list to process
        currentDir, exportDst = directories[index]

        # Move to the next element
        index = index + 1;

        logging.info('Processing ' + currentDir + ' ' + exportDst)

        # Move to the actual dir
        logging.info('INFO: Switching to ' + currentDir)
        os.chdir(currentDir)

        if executionChain.has_key(currentDir):
            currentDirInfo = executionChain[currentDir]
            currentDirInfo.appendExportDst(exportDst)
        else:
            # Create the Directory object for the new dir
            currentDirInfo = Directory.Directory(currentDir, exportDst)

            # Store it in the execution Chain
            executionChain[currentDir] = currentDirInfo

            # Obtain the dirs to recur with dst given
            logging.info('INFO: Obtaining recursive dirs')
            recursiveDirs = currentDirInfo.getSubrecursiveDirs()

            # Append dirs to directories
            directories.extend([ (dirName, currentDir)
                                 for dirName in recursiveDirs
                                 if directories.count((dirName, currentDir)) == 0])

            # Obtain dirs to recur with no dst
            recursiveDirsNodst = currentDirInfo.getSubrecursiveDirsNodst();

            # Loop over the non repeated ones to
            # Append dirs to directories
            directories.extend([(dirName, '') for dirName in recursiveDirsNodst
                                if directories.count((dirName, '')) == 0])

    # Reverse the directories to have the right execution order
    directories.reverse()

    AdaRule.executeRuleChain(directories, executionChain, targets)

def isCorrectAdaVersion():
    """ Method to check if the curren ada version is within the potentially
    limited values specified in variables ada.minimum.version,
    ada.maximum.version and ada.exact.version"""

    # Get versions to allow execution depending on the version
    minVersion = Directory.get('ada.minimum_version')
    maxVersion = Directory.get('ada.maximum_version')
    exactVersion = Directory.get('ada.exact_version')

    # If no value is given in any variable, avanti
    if (minVersion == None) and (maxVersion == None) and (exactVersion == None):
        return True

    # Translate current version to integer
    currentValue = 0
    vParts = Directory.fixed_definitions['ada.version'].split('.')
    currentValue = 1000000 * vParts[0] + 10000 * vParts[1] + vParts[2]

    # Translate all three variables to numbers
    minValue = currentValue
    if (minVersion != None):
        vParts = minVersion.split('.')
        minValue = 1000000 * vParts[0] + 10000 * vParts[1] + vParts[2]

    maxValue = currentValue
    if (maxVersion != None):
        vParts = maxVersion.split('.')
        maxValue = 1000000 * vParts[0] + 10000 * vParts[1] + vParts[2]

    exactValue = currentValue
    if (exactVersion != None):
        vParts = exactVersion.split('.')
        exactValue = 1000000 * vParts[0] + 10000 * vParts[1] + vParts[2]

        # Check if an exact version is required
    if (exactValue == currentValue) and (minValue <= currentValue) and \
            (currentValue <= maxValue):
        return True

    return False

def initialize():
    """
    Function that initializes all the required variables before doing anything
    else. This function is executed even before the options are parsed.
    """

    # Nuke the adado.log file
    logFile = os.path.join(os.getcwd(), 'adado.log')
    if os.path.exists(logFile):
        os.remove(logFile)

    # Set the logging format
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s %(message)s',
                        filename=logFile,
                        filemode='w')

    logging.debug('Initialization starts')

    # Get the ADA_HOME from the execution environment
    ada_home = os.path.dirname(os.path.abspath(sys.argv[0]))
    ada_home = os.path.abspath(os.path.join(ada_home, '..'))
    if ada_home == '':
        logging.error('ERROR: Unable to set variable ADA_HOME')
        raise TypeError, 'Unable to set variable ADA_HOME'

    if not os.path.isdir(ada_home):
        logging.error('ERROR: ADA_HOME is not a directory')
        raise TypeError, 'ADA_HOME is not a directory'

    logging.debug('ADA_HOME = ' + ada_home)
    Directory.fixed_definitions['ada.home'] = ada_home

    # Insert the definition of catalogs in the environment
    os.environ["XML_CATALOG_FILES"] = os.path.join(ada_home, 'DTDs',
                                                   'catalog')
    # Load the rest of all the default options
    Properties.loadOptions()

    # Compare ADA versions to see if execution is allowed
    if not isCorrectAdaVersion():
        logging.error('ERROR: Incorrect Ada Version (' +
                      Directory.globalVariables['ada.current.version'] + ')')
        raise TypeError, 'Incorrect ADA Version (' + \
            Directory.globalVariables['ada.current.version'] + \
            ') Review variables ' + \
            'ada.exact.version, \nada.minimum.version and ada.maximum.version'

def infoMessage(message):
    logging.info(message)
    print message

# Execution as script
if __name__ == "__main__":
    main()
