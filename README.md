*THIS IS A WORK IN PROGRESS*

Oh, hai. We ([@humantech/dev](https://github.com/orgs/humantech/teams/dev)) are completely rewriting smush.py so it can satisfy today's need: a more reliable, faster, feature-rich optimizing tool / API for the sakeness of bandwidth usage worldwide. Belive us, it counts, *a lot*. It will also be renamed, since it'll not look like smush.py (when done) at all.

# smush.py - Optimise images for the web

[Smush.it](http://www.smushit.com/) is a service from Yahoo that applies lossless optimisations to images for display on the web. Unfortunately they don't provide an API, and sometimes it's convenient to have a local command-line script.

smush.py uses the same tools as Smushit (read more at: http://oreilly.com/server-administration/excerpts/9780596522315/optimizing-images.html), but can be run locally.

The following lossless optimisations are performed:

* GIFs - If they're animated GIFs, they are optimised with Gifsicle. If they aren't animated, they're converted to PNGs with ImageMagick, then optimised as PNGs as below.
* PNGs - Quantised with pngnq, then crushed with pngcrush.
* JPGs - Optionally remove ALL metadata (it may not be legal to remove copyright notices, so only use this on images you own the copyright to or that don't have copyright notices). If they're larger than 10kb, they're converted to progressive JPGs. Compression is optimised with jpegtran.

*Note: If a GIF is converted to a PNG, it keeps the old `.gif` file extension in case the file name is in a database.*

## Installation

### Install all of the following required software:

* Python 2.x >= 2.5
* Gifsicle - http://www.lcdf.org/gifsicle/
* ImageMagick - http://www.imagemagick.org
* pngcrush - http://pmt.sourceforge.net/pngcrush/
* jpegtran from libjpeg
* pngnq

## Usage

This script is intended to be run over a collection of existing images - GIFs (perhaps animated), PNGs and JPEGs. It will perform lossless optimisations and will OVERWRITE THE ORIGINAL file. It is intended to be able to be used to optimise images that have a reference stored in a database, hence the reason for not modifying input file names at all.

It can be run as follows:

```
$ smush_it /path/to/file/or/directory(ies)
```

where /path/to/file/or/directory(ies) is a file or directory path, or list of space-separated paths to files or directories that will be optimised.

Or type:

```
$ smush_it --help
```

for usage information.

It is safe to run this script multiple times on the same files since all operations are lossless. In fact, PNG images may be optimised further by repeatedly smushing them.

Unless the `-q` option is given, statistics will be displayed when smushing has finished - these stats are approximate. GIFGIF refers to animated GIFs.

*Note 1: This software has been tested on Mac OSX and a lot of flavours of Linux.*
*Note 2: We also tested forks of smush.py listed by github - searching for other sources of inspiration - and one did poped up: the usage of pngquant instead of pngnq. It indeed has a better result regarding PNG size and time taken, but, believe us, IT IS NOT LOSSLESS. Just try yourself smushing [test/smush_me.png](https://raw.githubusercontent.com/humantech/smush.py/master/tests/smush_me.png) (1600x900 file generated using a [SubtlePatterns pattern](https://raw.githubusercontent.com/subtlepatterns/SubtlePatterns/gh-pages/soft_circle_scales.png)) to see the difference.*
