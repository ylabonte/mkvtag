#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tag one or more mkv files.

This python module uses the mkvtoolnix (https://mkvtoolnix.download/) cli tool
`mkvpropedit`. So you need to have this installed first.
"""
from optparse import OptionParser
from subprocess import call
from glob import glob
from os import path
from sys import exit
from re import compile, IGNORECASE


"""
Function definitions
"""


def store_tag(option, opt, value, parser):
    """Split option argument at '='.

    Expects option argument of type "<key>=<value>" to transfer and store it as
    dictionary (`parser.values[option.dest][<key>] = <value>`).
    """
    (key, val) = value.split('=')
    parser.values.ensure_value('tags', {})
    parser.values.tags[key] = val


def setTitleByPattern(pattern, repl, filename, abspath):
    """Set file title using regular expression substitution."""
    try:
        test = compile(pattern, IGNORECASE)
        if test.search(filename):
            title = test.sub(repl, filename)
            if title:
                cmdArgs.append('--set "title=%s"' % title)
            else:
                print('Skipping \'%s\', because the pattern match ' +
                      'is not compatible with the replacement string ' +
                      '(`-R/--repl`): \'%s\'' %
                      (abspath, repl))
        else:
            print('Skipping \'%s\', because it‘s basename does not ' +
                  'match the specified pattern (`-P/--pattern`): \'%s\'' %
                  (abspath, pattern))
    except Exception:
        print('Skipping \'%s\', because of a problem with pattern or ' +
              'replacement string.')


"""
Initialize option parser
"""


parser = OptionParser(version='0.1.0',
                      usage='./%prog [options] <filename> ...',
                      add_help_option=True,
                      description="""This tool is meant to ease MKV tagging.
It's primary purpose is to set the filename (without extension) as video title.
Use common filename patterns to edit multiple files at once.""",
                      epilog="""Author:
Yannic Labonte <yannic.labonte@gmail.com>"""
                      )

parser.add_option('-q', '--quiet',
                  action='store_false', dest='verbose',
                  help='Be quiet and do your work.',
                  )
parser.add_option('-v', '--verbose',
                  action='store_true', dest='verbose',
                  help='Verbose output.',
                  )
parser.add_option('-n', '--dry-run',
                  action='store_true', dest='dryRun',
                  help='Do not actually touch anything.'
                  )
parser.add_option('-t', '--tag',
                  action='callback', dest='tags', type='string',
                  callback=store_tag,
                  metavar='<tag>=<value>',
                  help='Set custom tag.',
                  )
parser.add_option('-T', '--filename2title',
                  action='store_true', dest='filename2title',
                  help='Set filename (without extension) as title.',
                  )
parser.add_option('-s', '--use-pattern',
                  action='store_true', dest='usePattern',
                  help='Use the pattern to parse filename and set title.'
                  )
parser.add_option('-P', '--pattern',
                  action='store', dest='pattern', type='string',
                  default=r'(?P<series>.*) - ' +
                          r'S0*(?P<season>\d+)E0*(?P<episode>\d+) - ' +
                          r'(?P<title>.*)\.mkv',
                  metavar='<subst-pattern>',
                  help='Substitution pattern.',
                  )
parser.add_option('-R', '--repl',
                  action='store', dest='repl', type='string',
                  default=r'\g<episode>. \g<title> ' +
                          r'(\g<series> - Season \g<season>)',
                  metavar='<subst-repl>',
                  help='Substitution replacement string (`repl` argument).',
                  )
parser.add_option('-E', '--executable',
                  action='store', dest='bin', type='string',
                  default='mkvpropedit',
                  metavar='<path-to-executable>',
                  help='name or path of `mkvpropedit` (default: mkvpropedit).',
                  )


"""
Start processing
"""


(opts, args) = parser.parse_args()
if not args:
    parser.print_help()
    exit(1)


commandArgs = []
if opts.tags:
    for tag in opts.tags:
        commandArgs.append('--set "%s=%s"' % (tag, opts.tags[tag]))


for givenPath in args:
    resolvedPaths = glob(givenPath)
    for filepath in resolvedPaths:
        cmdArgs = commandArgs.copy()
        abspath = path.abspath(filepath)
        filename = path.basename(filepath)
        filenameParts = filename.split('.')
        ext = filenameParts.pop()

        if not path.isfile(abspath) or ext != 'mkv':
            if opts.verbose:
                print('Skipping \'%s\', because it‘s not a MKV.' % abspath)
            continue

        if opts.filename2title:
            title = '.'.join(filenameParts)
            cmdArgs.append('--set "title=%s"' % title)
        elif opts.usePattern:
            setTitleByPattern(opts.pattern, opts.repl, filename, abspath)

        command = '%s "%s" --edit info %s' % (
                  opts.bin, abspath, ' '.join(cmdArgs))

        if opts.verbose:
            print(command)

        if not opts.dryRun:
            call(command, shell=True)


exit(0)
