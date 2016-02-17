#!/usr/bin/env python

import subprocess
import argparse

parser = argparse.ArgumentParser(
    description = "Calls the detect edit clusterprogram for one or more files",
    epilog = """This program allows for batch calls of the sliding window
    program. If files have routine structure and are named in a consistent
    manner including information such as organism and gene name then a simple
    wrapper script such as this can easily automate largescale analysis""")
parser.add_argument('infiles', nargs='+', help='list of infiles')
parser.add_argument('-gen', '--genomic', help='unique string present in genomic sequenc headers')
parser.add_argument('-r', '--RNA', help='unique string present in RNA sequence headers')
parser.add_argument('-out', '--outfile', help='name for master outfile')
args = parser.parse_args()

gen = args.genomic
rna = args.RNA
out = args.outfile

for infile in args.infiles:
    short_in = infile.split('.')[0]
    subprocess.call(["/Users/cklinger/git/Rediting/rediting/detect_edit_clusters.py",
        "-in", infile, "-out", out, "-n", short_in, "-r", rna, "-gen", gen])
