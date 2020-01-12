# -*- coding: utf-8 -*-
"""This python module is a wrapper for the `mkvtoolnix` cli suite."""

from subprocess import call
from glob import glob
from os import path

from re import compile, IGNORECASE


"""
MKVTag class
"""


def mkvtag():
    """Initialize mkvtag class."""
    def __init__(self):
        self.abspath = ''
        self.filename = ''
        self.filenameParts = []
        self.fileextension = ''
        self.verbose = False
        self.dry_run = False
        self.bin = ''
        self.cmd_args = []

    def run(self):
        """Execute the command."""
        command = '%s "%s" --edit info %s' % (
            self.bin, self.abspath, ' '.join(self.cmd_args)
        )
        if not self.dry_run:
            call(command, shell=True)
        if verbose:
            return command

    def dryRun(self, on=True):
        """Activate or deactivate the dry-run mode."""
        self.dry_run = on

    def verbose(self, on=True):
        """Set output to be verbose."""
        self.verbose = on

    def setFile(self, absolutePath):
        """Set file to work on."""
        self.abspath = absolutePath

    def setMkvpropeditExec(self, path):
        """Set the mkvpropedit executable path."""
        self.bin = path

    def setMkvFile(self, filepath):
        self.abspath = path.abspath(filepath)
        self.filename = path.basename(filepath)
        self.filenameParts = filename.split('.')
        self.fileextension = self.filenameParts.pop()

        if not path.isfile(self.abspath) or self.fileextension != 'mkv':
            raise Exception('Skipping \'%s\', because it‘s not a MKV.' % abspath)

    def setTitleByFilename(self):
        self.cmd_args.append('--set "title=%s"' % '.'.join(self.filenameParts))

    def setTitleByPattern(self, pattern, repl, filename, abspath):
        """Set file title using regular expression substitution."""
        try:
            test = compile(pattern, IGNORECASE)
            if test.search(filename):
                title = test.sub(repl, filename)
                if title:
                    self.cmd_args.append('--set "title=%s"' % title)
                else:
                    print('Skipping \'%s\', because the pattern match ' +
                          'is not compatible with the replacement string ' +
                          '(`-R/--repl`): \'%s\'' %
                          (self.abspath, repl))
            else:
                print('Skipping \'%s\', because it‘s basename does not ' +
                      'match the specified pattern (`-P/--pattern`): \'%s\'' %
                      (self.abspath, pattern))
        except Exception:
            print('Skipping \'%s\', because of a problem with pattern or ' +
                  'replacement string.')

"""
Start processing
"""


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
