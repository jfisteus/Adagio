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
import os, re, sys, glob

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

import adagio, directory, i18n, rules, xsltproc, testshuffle, dependency
import treecache

# Prefix to use for the options
module_prefix = 'testexam'

# List of tuples (varname, default value, description string)
options = [
    ('styles',
     '%(home)s%(file_separator)sAdagio_Styles%(file_separator)sExam.xsl',
     i18n.get('xslt_style_file')),
    ('output_format', 'html', i18n.get('output_format')),
    ('extra_arguments', '', i18n.get('extra_arguments').format('Xsltproc')),
    ('produce', 'regular', i18n.get('exercise_produce'))
    ]

documentation = {
    'en' : """
    Rule to typeset a test exam from an XML file. The "files" are processed to
    render them as test exams with the following versions:

    - One per language in "languages"
    - One per version in produce:
      * regular: regular version, no solution, no pguide
      * solution: regular version with the solution
      * pguide: regular version including solution AND professor guide
    """}

def Execute(rule, dirObj):
    """
    Execute the rule in the given directory
    """

    # Get the files to process, if empty, terminate
    toProcess = rules.getFilesToProcess(rule, dirObj)
    if toProcess == []:
        return

    # Every source file given is processed to know how many permutations will be
    # rawFiles contains the list of files produced that need to be processed
    rawFiles = doShuffle(toProcess, dirObj)

    # Prepare the style transformation
    styleFiles = dirObj.getProperty(rule, 'styles')
    styleTransform = xsltproc.createStyleTransform(styleFiles.split())
    if styleTransform == None:
        print i18n.get('no_style_file')
        return

    # Create the dictionary of stylesheet parameters
    styleParams = xsltproc.createParameterDict(rule, dirObj)

    # Create a list with the param dictionaries to use in the different versions
    # to be created.
    paramDict = []
    produceValues = set(dirObj.getProperty(rule, 'produce').split())
    if 'regular' in produceValues:
        # Create the regular version, no additional parameters needed
        paramDict.append(({}, ''))
    if 'solution' in produceValues:
        paramDict.append(({'solutions.include.guide': "'yes'",
                           'adagio.testquestions.include.solutions': "'yes'"},
                          '_solution'))
    if 'pguide' in produceValues:
        paramDict.append(({'solutions.include.guide': "'yes'",
                           'adagio.testquestions.include.solutions': "'yes'",
                           'professorguide.include.guide': "'yes'",
                           'adagio.testquestions.include.id': "'yes'",
                           'adagio.testquestions.include.history': "'yes'"},
                          '_pguide'))

    # Apply all these transformations.
    xsltproc.doTransformations(styleFiles.split(), styleTransform, styleParams,
                               rawFiles, rule, dirObj, paramDict)

    return

def clean(rule, dirObj):
    """
    Clean the files produced by this rule
    """

    adagio.logInfo(rule, dirObj, 'Cleaning')

    # Get the files to process
    toProcess = rules.getFilesToProcess(rule, dirObj)
    if toProcess == []:
        return

    rawFiles = []
    for fname in toProcess:
        # Get the result files
        resultFiles = doGetShuffledFiles(fname)

        # Accumulate the list
        rawFiles.extend(resultFiles)

    suffixes = []
    produceValues = set(dirObj.getProperty(rule, 'produce').split())
    if 'regular' in produceValues:
        # Delete the regular version
        suffixes.append('')
    if 'solution' in produceValues:
        # Delete the solution
        suffixes.append('_solution')
    if 'pguide' in produceValues:
        # Delete the professor guide
        suffixes.append('_pguide')

    xsltproc.doClean(rule, dirObj, rawFiles, suffixes)

    # Clean also the produced files
    map(lambda x: rules.remove(x), rawFiles)

    return

def doShuffle(toProcess, dirObj):
    # Every source file given is processed to know how many permutations will be
    # produced.
    rawFiles = []
    for fname in toProcess:
        # Get the result files
        resultFiles = doGetShuffledFiles(fname)

        # Accumulate the list
        rawFiles.extend(resultFiles)

        # Update the dependencies (apply update to all elements in resultFiles)
        try:
            sources = set([fname])
            sources.update(dirObj.option_files)
            map(lambda x: dependency.update(x, sources), resultFiles)
        except etree.XMLSyntaxError, e:
            print i18n.get('severe_parse_error').format(fName)
            print e
            sys.exit(1)

        # If all the permutation files are up to date, no need to process
        if reduce(lambda x, y: x and y,
                  [dependency.isUpToDate(x) for x in resultFiles]):
            print i18n.get('testexam_no_shuffle_required').format(fname)
            continue

        print i18n.get('testexam_shuffling').format(fname)
        permutations = testshuffle.main(fname, adagio.userLog)

        if permutations == 0:
            print i18n.get('testexam_no_permutations').format(fname)
            sys.exit(1)
    return rawFiles

def doGetShuffledFiles(fname):
    """
    Function that given an XML file, checks the presence of productnumber
    elements in the section info and returns the names of the files which will
    contain the permutations.
    """
    
    sourceTree = treecache.findOrAddTree(fname, True)
    root = sourceTree.getroot()

    # Get the number of 'productnumber' elements. If none, set it to 1
    sectionInfo = root.find('sectioninfo')
    n = 1
    if sectionInfo != None:
        pnumbers = sectionInfo.findall('productnumber')
        if pnumbers != None:
            n = len(pnumbers)

    # Create the raw files that will be produced
    (h, t) = os.path.splitext(fname)
    return map(lambda x: h + '_' + str(x) + t, range(1, n + 1))
