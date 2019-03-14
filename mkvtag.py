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


def store_tag(option, opt, value, parser):
    """Split option argument at '='.

    Expects option argument of type "<key>=<value>" to transfer and store it as
    dictionary (`parser.values[option.dest][<key>] = <value>`).
    """
    (key, val) = value.split('=')
    parser.values.ensure_value('tags', {})
    parser.values.tags[key] = val


parser = OptionParser(version='0.1.0',
                      usage='%prog [options] <filename> ...',
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
parser.add_option('-E', '--executable',
                  action='store', dest='bin', type='string',
                  default='mkvpropedit',
                  metavar='<path-to-executable>',
                  help='name or path of `mkvpropedit` (default: mkvpropedit).',
                  )


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

        command = '%s "%s" --edit info %s' % (
                  opts.bin, abspath, ' '.join(cmdArgs))

        if opts.verbose:
            print(command)

        if not opts.dryRun:
            call(command, shell=True)

exit(0)
