#!/usr/bin/python
# -*- coding: UTF-8 -*-#
#
# Author: Abelardo Pardo (abelardo.pardo@uc3m.es)
#
#
#

msgs = {
    '__doc__': """
    Script to execute the production rules in the current directory. The
    invocation of the script must be:

    script [options] [dir dir ...]

    The script executes the production rules in the given directories in the
    order they appear in the command line. If no directory is given, then the
    current directory is processed.

    The script accepts the following options:

      -d num: Debugging level. Used to set the severity level in a
              logging object. Possible values are:

              CRITICAL  	50
              ERROR 	        40
              WARNING 	        30
              INFO 	        20
              DEBUG 	        10
              NOTSET 	         0

      -s name value: Executes the application by first storing in the
       environment the assignment name = value. This means that, unless
       overwritten by definitions in the properties file, this assignment will
       be visible to all the rules executed.
    """,
    'file_not_found': 'File {0} not found',
    'cannot_open_fiel': 'Cannot open file {0}',
    'line_in_no_section': 'Line {ln} of {pfile} is outside a section',
    'incorrect_assignment': 'Incorrect assignment in line {ln} of {pfile}',
    'severe_parse_error': 'Severe error while parsing line {ln} of {pfile}',
    'not_enouth_params': 'Not enough params for {0}',
    'name_of_executable': 'Name of the executable to use in this rule',
    'rule_debug_level': 'Level of debug message',
    'rule_src_dir': 'Directory containing the source files.',
    'rule_dst_dir': 'Directory where the new files will be created.',
    'xslt_style_file': 'Style to be applied to the given source files.',
    'output_format': 'Extension to use when creating the new files.',
    'xslt_extra_arguments':
    'Extra arguments passed directly to the style processor.',
    'files_to_process': 'Space separated list of files to process.',
    'xslt_merge_styles':
    'Space separated list of styles to combine with the given style',
    'xslt_profile_lang': 'Language to use to profile the source documents',
    'xslt_multilingual':
    'True/False if the documents to process are multilingual.\n\
      Incompatible with profile_lang'
    }
