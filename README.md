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

Then make sure `~/.local/bin` is in your path, else

```bash
echo -e "\nexport PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
```

on Linux, and 

```bash
# store off major.minor version number of your default Python
majmin=$( python -V |& perl -pe 's/.* (\d+\.\d+)\.\d+/\1/' )

# append *that* Python's 'bin' directory to your PATH
echo -e "\nexport PATH=$HOME/Library/Frameworks/Python/$majmin/bin:$PATH" \
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
[gb]: https://genome.ucsc.edu/cgi-bin/hgTracks
[click]: http://click.palletsprojects.com
[trackhub]: https://github.com/daler/trackhub
[issue]: https://tf.cchmc.org/s/dvakj
