# trackhub

A [Click]-based command line interface built upon [daler/trackhub][trackhub],
a Python library for creating, managing, and uploading "track hubs" for use
with the [UCSC Genome Browser][gb].

For details on the underlying Python library, see
[`README_daler.rst`](README_daler.rst).

## Quick Start

With Python (2.7 or 3.x) using [pip]:

```bash
pip install --user https://github.com/ernstki/trackhub/archive/add-click-cli.zip
```

Some data files need to be obtained from UCSC in order for the conversion to
bigBed and bigWig to work properly (more information [here][bigbed]):

```bash
# replace with 'python3' if using Python 3.x
datadir=$( python -c '
import pkg_resources
print(pkg_resources.resource_filename("trackhub", "data"))
' )

mkdir -p $datadir && pushd $datadir

# log in to the HTTP proxy first, if required on your network
./fetch_chrom_sizes.sh
```

_This process is, sadly, not yet automatic; see #4 in the issue tracker._

Finally make sure `~/.local/bin` is in your path, else

```bash
echo -e "\nexport PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
```

on Linux, and 

```bash
# store off major.minor version number of your default Python
majmin=$( python -V |& perl -pe 's/.* (\d+\.\d+)\.\d+/\1/' )

# append *that* Python's 'bin' directory to your PATH
echo -e "\nexport PATH=$HOME/Library/Python/$majmin/bin:$PATH" \
    >> ~/.bashrc
```

on macOS / OS X.

### Make sure it works

```bash
trackhub --help

# Usage: trackhub [OPTIONS] COMMAND [ARGS]...
# 
# Options:
#   -b, --build <BUILD>  Specify the UCSC build (default: hg19).
#   -v, --verbose        Enable verbose (debugging) output.
#   -h, --help           Show this message and exit.
# 
# Commands:
#   convert   Convert files into GB track hub-appropriate formats.
#   generate  Generate GB track hub for discovered files in c.w.d.
# 
#   A Weirauch Lab Production ~ Issues? -> https://tf.cchmc.org/s/dvakj
```

## Feature Requests

Please [file an issue][issue] with the label `featurerequest` in the this
project's issue tracker.

## Authors

Original author: [Ryan Dale](https://github.com/daler), NIH
<br>Command-line interface: [Kevin Ernst](<mailto:kevin.ernst%20-at-%20cchmc.org>),
Cincinnati Children's Hospital Medical Center

## License
MIT. See [`LICENSE.txt`](LICENSE.txt).
 

[pip]: https://pip.pypa.io/en/stable/installing/
[bigbed]: http://genome.ucsc.edu/goldenPath/help/bigBed.html
[gb]: https://genome.ucsc.edu/cgi-bin/hgTracks
[click]: http://click.palletsprojects.com
[trackhub]: https://github.com/daler/trackhub
[issue]: https://tf.cchmc.org/s/dvakj
