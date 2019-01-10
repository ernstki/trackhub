Genome Build Chromosome Sizes
=============================

These files are required by the UCSC 'bedToBigBed' and other utilities
obtained from: http://hgdownload.soe.ucsc.edu/admin/exe/.

A sample invocation for the 'hg19' build would look like:

    BUILD=hg19  
    fetchChromSizes $BUILD > $BUILD.chrom.sizes

The 'fetchChromSizes' utility (which requires network access) is obtained from
the same URL, above.

If you already have that utility available in your $PATH, you can just run
'./fetch_chrom_sizes.sh' to fetch the common ones.
