import os
import glob
import click
import shlex
import logging
import subprocess

from time import time
from multiprocessing.pool import Pool

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(name)s:%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

BUILD = 'hg19'
DATABANK = '/data/weirauchlab/databank'
CHROMSIZES = 'hg19.chrom.sizes'
# CHROMSIZES = "{databank}/chrom/{build}/{build}.chrom.sizes"\
#    .format(databank=DATABANK, build=BUILD)

EXTCONVS = {
    '.bb': None,
    '.bw': None,
    '.bigwig': None,
    '.bed': "bedToBigBed '{{infile}}' '{}' '{{base}}.bb'".format(CHROMSIZES),
    '.wig': "wigToBigWig '{{infile}} '{}' '{{base}}.bw".format(CHROMSIZES),
    '.wiggle': "wigToBigWig '{{infile}} '{}' '{{base}}.bw".format(CHROMSIZES),
}


def converter(infile):
    ts = time()
    base, ext = os.path.splitext(infile)
    if not EXTCONVS.get(ext, None):
        return
    cmd = EXTCONVS[ext].format(infile=infile, base=base)
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    logging.info("Invoking subprocess: {}".format(cmd))
    outs, errs = proc.communicate()
    if errs:
        logging.warning("Subprocess call to {} failed for {}; returned {}"
                        .format(cmd[0], infile, proc.returncode))
    else:
        logger.info("Subprocess {} succeeded for {}; elapsed {}'"
                    .format(cmd[0], infile, time() - ts))


@click.group()
def cli():
    pass


@cli.command
def convert():
    """Convert all discovered files into Track Hub-appropriate formats"""
    files = glob.glob(os.path.join(os.getcwd(), '*'))

    with Pool(4) as p:
        p.map(converter, files)


@cli.command()
def gen():
    click.echo("Generating... (not really)")


if __name__ == '__main__':
    cli()
