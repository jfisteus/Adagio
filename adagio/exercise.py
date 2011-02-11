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
import os, re, sys, glob

import directory, i18n, dependency, adarule, xsltproc

# Prefix to use for the options
module_prefix = 'exercise'

# List of tuples (varname, default value, description string)
options = [
    ('styles',
     '%(home)s%(file_separator)sADA_Styles%(file_separator)sExerciseSubmit.xsl',
     I18n.get('xslt_style_file')),
    ('submit_styles',
     '%(home)s%(file_separator)sADA_Styles%(file_separator)sAsapSubmit.xsl',
     I18n.get('xslt_style_file')),
    ('output_format', 'html', I18n.get('output_format')),
    ('extra_arguments', '', I18n.get('extra_arguments').format('Xsltproc')),
    ('produce', 'regular', I18n.get('exercise_produce'))
    ]

documentation = {
    'en' : """
    Rule to process XML files containing exercises. For each file, the following
    documents can (optionally be created):

    - Regular document for the students

    - Document with the solutions (elements with condition=solution)

    - Document with the professor guide (elements with condition =
      professorguide)

    - Document cotaining a form to submit answers (different stylesheet)

    The generation of these documents is controlled with the following
    convention.

    - The "files" in "src_dir" are processed as many times as specified by the
    "languages" variable and the created files are created in the "dst_dir".

    - All the created files will have the extension given in "output_format"

    - All files are processed as many times as specified by "language"
    """}

# Possible values of the 'produce' option for this rule
_produce_values = set(['regular', 'solution', ' pguide', ' submit'])

def Execute(target, directory):
    """
    Execute the rule in the given directory
    """

    # Get the files to process, if empty, terminate
    toProcess = AdaRule.getFilesToProcess(target, directory)
    if toProcess == []:
        return

    # Prepare the style transformation
    styleFiles = directory.getProperty(target, 'styles')
    styleTransform = Xsltproc.createStyleTransform(styleFiles.split())
    if styleTransform == None:
        print I18n.get('no_style_file')
        return

    # Create the dictionary of stylesheet parameters
    styleParams = Xsltproc.createParameterDict(target, directory)

    # Create a list with the param dictionaries to use in the different versions
    # to be created.
    paramDict = []
    produceValues = set(directory.getProperty(target, 'produce').split())
    if 'regular' in produceValues:
        # Create the regular version, no additional parameters needed
        paramDict.append(({}, ''))
    if 'solution' in produceValues:
        paramDict.append(({'solutions.include.guide': "'yes'"},
                          '_solution'))
    if 'pguide' in produceValues:
        paramDict.append(({'solutions.include.guide': "'yes'",
                          'professorguide.include.guide': "'yes'"},
                          '_pguide'))

    # Apply all these transformations.
    Xsltproc.doTransformations(styleFiles.split(), styleTransform, styleParams,
                               toProcess, target, directory, paramDict)

    # If 'submit' is also in the produce values, apply that transformation as
    # well (an optimization could be applied here such that if the same style is
    # given for the submit production, it could be folded in the previous
    # transformations...)

    if 'submit' in produceValues:

        # Prepare the style transformation
        styleFiles = directory.getProperty(target, 'submit_styles')
        styleTransform = Xsltproc.createStyleTransform(styleFiles.split())
        if styleTransform == None:
            print I18n.get('no_style_file')
            return

        # Create the dictionary of stylesheet parameters
        styleParams = Xsltproc.createParameterDict(target, directory)

        # Apply the transformation and produce '_submit' file
        Xsltproc.doTransformations(styleFiles.split(), styleTransform,
                                   styleParams, toProcess, target, directory,
                                   [({}, '_submit')])

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

    # Create a list with the suffixes to consider
    suffixes = []
    produceValues = set(directory.getProperty(target, 'produce').split())
    if 'regular' in produceValues:
        # Delete the regular version
        suffixes.append('')
    if 'solution' in produceValues:
        # Delete the solution
        suffixes.append('_solution')
    if 'pguide' in produceValues:
        # Delete the professor guide
        suffixes.append('_pguide')
    if 'submit' in produceValues:
        # Delete the submission file
        suffixes.append('_submit')

    Xsltproc.doClean(target, directory, toProcess, suffixes)

    return

# Execution as script
if __name__ == "__main__":
    Execute(module_prefix, Directory.getDirectoryObject('.'))
