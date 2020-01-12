![Python3](https://img.shields.io/badge/Python-3-green.svg?logo=python&style=popout)

# MKVtag

This is a slimmed down wrapper script for the mkvpropedit tool of the
mkvtoolnix package. It is meant to operate on multiple files at once.

Imagine you have backed up a bunch of series and movies from your Bluray and DVD
collection using eg. [MakeMKV](https://www.makemkv.com/) and
and [HandBrake](https://handbrake.fr/) to get a reasonable sized MKV. It is more
than enough work to name all the files properly. In the end you might end up
with a directory structure like this:
<a name="directory-structure"></a>
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
But as you might have noticed: Most video players do not display the filename.
They’re displaying a title stored as meta data property.

A call of `./mkvtag -T 'multimedia/**/*'` will set the filename (without its
extension) as the title for each _.mkv_ file in the subtree of the multimedia
directory. Note the double quotes surrounding the path argument. I am using
the `zsh` as preferred shell, but it has also an automatic filename expansion
feature. The quotation marks make sure that the python script does the job of
filename expansion, which turns out to be much more efficient in terms of
performance.

It does not make much sense to use it for editing a single file. In cases
you just want to edit a single file or files that have distinct properties
which cannot be set in a single call, I would recommend taking a look at
the underlying [`mkvpropedit`](https://mkvtoolnix.download/doc/mkvpropedit.html) tool.


## Requirements

* Python 3
* [`mkvpropedit`](https://mkvtoolnix.download/doc/mkvpropedit.html)
(this is part of the [mkvtoolnix](https://mkvtoolnix.download/) package)


## How to use

Just clone the repo or download the mkvtag.py, check that it’s executable
and you are ready to go. Wait! One thing... As mentoined in the previous section:
You have to have the [mkvtoolnix package installed](https://mkvtoolnix.download/downloads.html).
On most systems it should be available through the package manager.

### Set filename as title

The following example will check all files in your Movies directory for a _.mkv_
file extension and prints out the command, which would be used for each file to
set its title meta property to its filename (except the file extension).
Actually it is the dry-run mode (`-n`/`--dry-run`) combined with the verbose flag
(`-v`/`--verbose`) and the filename-to-title function (`-T`/`--filename2title`).
```
$ ./mkvtag.py -nvT ~/Movies/*
```
When you omit the `n` in `-nvT` the tool will actually process the files using
exact the command printed in the call above.
```
$ ./mkvtag.py -vT ~/Movies/*
```

### More advanced titles

I added a more advanced naming scheme for my series. Regarding the naming of the
[Silicon Valley episodes in the file system tree example above](#directory-structure),
the hard-coded default pattern would match and set the titles to  
'_`episode number`. `episode title` (`series title` - Season `season number`)_'.
So you could just use the `-s`/`--use-pattern` switch:
```
$ ./mkvtag.py -s 'multimedia/series/Silicon Valley/**'
```
This strictly assumes the naming scheme used in the example. The title of the
episodes will then set to:
> 1\. Minimum Viable Product (Silicon Valley - Season 1)  
> ...  
> 8\. Optimal Tip-to-Tip Efficiency (Silicon Valley - Season 1)

This is done by a regular expression substitution. More precise: It is done by the
default values of the `-P` and `-R` options.

#### Using custom patterns

You can alter the applied search pattern (`-P`/`--pattern`) as well as the
replacement string (`-R`/`--repl`). Let’s assume the filename
'_Torchwood - S04E01 - Miracle Day - The New World.mkv_'. It’s built on the
series title, season number, episode number, a season title, episode title and
at least the _.mkv_ file extension. So this file would not be processed using
the command from the most recent example, which relied on the default pattern
(and replacement strings). But you could set the title to everything you want
using your own parameters. Let’s say you want to set the title to
'_Miracle Day - Chapter 1: The New World (Torchwood, Season 4)_'. The following
parameters will do the job:
```
$ ./mkvtag.py -s -P '(.*) - S0*(\d+)E0*(\d+) - (.*) - (.*).mkv' -R '\4 - Chapter \3: \5 (\1, Season \2)' '*'
```
See the [Python 3 documentation on the regular expression module (re)](https://docs.python.org/3/library/re.html)
for details on how to work with groups or named groups.

#### The default pattern

The hard-coded default pattern uses named groups. This is important to know, if
your filenames match the default pattern but you want to alter the title scheme.
```
(?P<series>.*) - S0*(?P<season>\d+)E0*(?P<episode>\d+) - (?P<title>.*)\.mkv
```
The corresponding default replacement string is:
```
\g<episode>. \g<title> (\g<series> - Season \g<season>)
```
You can use this if you have files matching the default pattern, but want 
another naming scheme for your titles. For example to set only the episode title
as meta title for the MKV, you could use:
```
$ ./mkvtag -s -R '\g<title>' '*'
```

## More help

Basically simply use the `-h` switch to get help:
```
Usage: ./mkvtag [options] <filename> ...

This tool is meant to ease MKV tagging. It’s primary purpose is to set the
filename (without extension) as video title. Use common filename patterns to
edit multiple files at once.

Options:
  --version             show program’s version number and exit
  -h, --help            show this help message and exit
  -q, --quiet           Be quiet and do your work.
  -v, --verbose         Verbose output.
  -n, --dry-run         Do not actually touch anything.
  -t <tag>=<value>, --tag=<tag>=<value>
                        Set custom tag.
  -T, --filename2title  Set filename (without extension) as title.
  -s, --use-pattern     Use the pattern to parse filename and set title.
  -P <subst-pattern>, --pattern=<subst-pattern>
                        Substitution pattern.
  -R <subst-repl>, --repl=<subst-repl>
                        Substitution replacement string (`repl` argument).
  -E <path-to-executable>, --executable=<path-to-executable>
                        name or path of `mkvpropedit` (default: mkvpropedit).

Author: Yannic Labonte <yannic.labonte@gmail.com>
```
