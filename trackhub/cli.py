import os
import glob
import click
import logging
import subprocess as subp
import pkg_resources

from multiprocessing.pool import Pool

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(name)s:%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

DEFAULTS = {
    'build': 'hg19',
}

# where to find supporting data like '<build>.chr.sizes' for given build
DATADIR = pkg_resources.resource_filename(__name__, 'data')

EXTCONVS = {
    '.bb': None,
    '.bw': None,
    '.bigwig': None,
    '.bed': [
        "cut -f1-4 '{infile}' | sort -k1,1 -k2,2n > '{infile}.tmp'",
        "bedToBigBed '{infile}.tmp' '{chromsizes}' '{base}.bb'",
        "rm '{infile}.tmp'",
    ],
    '.wig': "wigToBigWig '{infile} '{chromsizes}' '{base}.bw",
    '.wiggle': "wigToBigWig '{infile} '{chromsizes}' '{base}.bw",
}


def get_chrome_sizes(build):
    """Return filename of the <build>.chrome.sizes file."""
    chrsize = os.path.join(DATADIR, "{}.chrom.sizes".format(build))
    if os.path.isfile(chrsize) and os.stat(chrsize).st_size > 0:
        return chrsize
    else:
        return None


# click.secho("OOPS!", color='red', err=True)
# click.echo("Missing required file {}".format(chrsize), err=True)
# click.echo("Please run 'fetch_chrome_sizes.sh' inside {}"
#            .format(DATADIR), err=True)


def converter(infile, build=DEFAULTS['build']):
    if os.path.isdir(infile):
        return

    base, ext = os.path.splitext(infile)
    basename = os.path.basename(infile)

    if not EXTCONVS.get(ext, None):
        logger.debug("No conversion handler for file {}; skipping"
                     .format(basename))
        return

    chrsizes = get_chrome_sizes(build)
    cmds = [EXTCONVS[ext]] if type(EXTCONVS[ext]) == str else EXTCONVS[ext]
    step = 1

    logger.info("Starting conversion for '{}'".format(basename))

    for cmd in cmds:
        cmd = cmd.format(infile=infile, chromsizes=chrsizes, base=base)
        proc = subp.Popen(cmd, shell=True, stdout=subp.PIPE, stderr=subp.PIPE)

        logger.debug("Invoking converter step {}/{} for '{}': {} (PID: {})"
                     .format(step, len(cmds), basename, cmd, proc.pid))
        outs, errs = proc.communicate()

        if proc.returncode:
            logger.error("Failed step {}/{} for '{}' with exit code {}"
                         .format(step, len(cmds), basename, proc.returncode))
            logger.error("Error detail: {}"
                         .format(errs.decode('utf-8').split("\n")[0]))
        else:
            logger.debug("Completed step {}/{} for '{}'"
                         .format(step, len(cmds), basename))
        step += 1

    logger.info("Completed conversion for '{}'".format(basename))


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-b', '--build', type=str,
              help="Specify the UCSC build (default: hg19).",
              metavar='<BUILD>', default=DEFAULTS['build'], )
@click.option('-v', '--verbose', is_flag=True,
              help="Enable verbose (debugging) output.")
@click.pass_context
def cli(ctx, build, verbose):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    # ref: https://tf.cchmc.org/s/ulsa6
    ctx.ensure_object(dict)

    ctx.obj['BUILD'] = build
    ctx.obj['VERBOSE'] = verbose

    if verbose:
        logger.setLevel(logging.DEBUG)


@cli.command()
@click.pass_context
def convert(ctx):
    """Convert files into GB track hub-appropriate formats."""
    files = glob.glob(os.path.join(os.getcwd(), '*'))

    with Pool(4) as p:
        p.map(converter, files)


@cli.command()
@click.pass_context
def gen(ctx):
    """Generate GB track hub for discovered files in c.w.d."""
    click.echo("Generating... (not really)")


if __name__ == '__main__':
    cli(obj={})
