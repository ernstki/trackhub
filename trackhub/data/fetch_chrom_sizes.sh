#!/bin/bash
set -uo pipefail

BUILDS=(
    hg19
    hg38
    mm9
    mm10
)

discreetly() { "$@" 2>/dev/null ; }
silently() { "$@" &>/dev/null; }

RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
RESET=$(tput sgr0)

if ! silently which fetchChromSizes; then
    echo >&2
    echo "${RED}OH NOES!${RESET}" >&2
    echo >&2
    echo "Could not find 'fetchChromSizes' in your \$PATH." >&2
    echo "Maybe download it from http://hgdownload.soe.ucsc.edu/admin/exe?" >&2
    echo >&2
    exit 1
fi

for build in ${BUILDS[*]}; do
    chrsizes=${build}.chrom.sizes
    if [[ -f $chrsizes ]]; then
        echo "Found $chrsizes already present, ${YELLOW}skipping${RESET}." >&2
    else
        echo -n "Downloading $chrsizes... " >&2
        # fetchChromSizes doesn't return non-zero if build doesn't exist :(
        discreetly fetchChromSizes $build | tee $chrsizes | \
            grep -q "404 Not Found"

        # grep should NOT find "Not Found" in the output
        if (( $? )); then
            echo "${GREEN}done${RESET}." >&2
        else
            rm $chrsizes
            echo "${RED}FAILED${RESET}." >&2
        fi
    fi
done
