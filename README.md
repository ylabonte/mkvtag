![Python3](https://img.shields.io/badge/Python-3-green.svg?logo=python&style=popout)

# MKVtag

This is a slimmed down wrapper script for the mkvpropedit tool of the
mkvtoolnix package. It is meant to operate on multiple files at once.

Imagine you have a nas full of your favourit series and movies, all backed  
up from your Bluray and DVD collection using eg. [MakeMKV](https://www.makemkv.com/) 
and [HandBrake](https://handbrake.fr/) to get a reasonable sized MKV.

a folder structure of the kind:
```
multimedia/
├── movies/
│   ├── ...
│   ├── The Boondock Saints.mkv
│   └── ...
└── series/
    ├── ...
    ├── Silicon Valley/
    │   ├── Season 1/
    │   │   ├── Silicon Valley - S01E01 - Minimum Viable Product.mkv
    │   │   ├── ...
    │   │   └── Silicon Valley - S01E08 - Optimal Tip-to-Tip Efficiency.mkv
    │   └── ...
    └── Westworld/
        └── ...
```
A call of `./mkvtag -T "multimedia/**/*"` will set the filename (without its 
extension) as the title for each _.mkv_ file in the subtree of the multimedia
directory. Note the double quotes surrounding the path argument. I am using 
the `zsh` as preferred shell, but it has also an automatic filename expansion 
feature. The quotation marks make sure that the python script does the job of
filename expansion, which turns out to be much more efficient in terms of 
performance.

It does not make much sense to use it for editing a single file. In cases
you just want to edit a single file or files that have destinct properties
which cannot be set in a single call, I would recommend you to take a look at
the underlying `mkvpropedit` tool.


## Requirements

* Python 3
* [mkvpropedit](https://mkvtoolnix.download/doc/mkvpropedit.html) 
(this is part of the [mkvtoolnix](https://mkvtoolnix.download/) package)


## How to use

Just clone the repo or download the mkvtag.py, check that it's executable
and you are ready to go. Wait! One thing. As mentoined in the previous section:
You have to have [mkvtoolnix package installed](https://mkvtoolnix.download/downloads.html).
On most systems it should be available through the package manager.

The following example will check all files in your Movies directory for a _.mkv_ 
file extension and prints our the command for each file for setting the title meta
property of the _.mkv_ files to their filename omitting the file extension. 
Actually it is the dry-run mode (`-n`) combined with the verbose flag (`-v`) and
the filename to title function (`-T`).
```
$ ./mkvtag.py -nvT ~/Movies/*
```
When you omit the `n` in `-nvT` the tool will actually process the files using
exact the command printed in the call above.
```
$ ./mkvtag.py -vT ~/Movies/*
```

Basically simply use the `-h` switch to get help:
```
Usage: ./mkvtag.py [options] <filename> ...

This tool is meant to ease MKV tagging. It's primary purpose is to set the
filename (without extension) as video title. Use common filename patterns to
edit multiple files at once.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -q, --quiet           Be quiet and do your work.
  -v, --verbose         Verbose output.
  -n, --dry-run         Do not actually touch anything.
  -t <tag>=<value>, --tag=<tag>=<value>
                        Set custom tag.
  -T, --filename2title  Set filename (without extension) as title.
  -E <path-to-executable>, --executable=<path-to-executable>
                        name or path of `mkvpropedit` (default: mkvpropedit).

Author: Yannic Labonte <yannic.labonte@gmail.com>
```
