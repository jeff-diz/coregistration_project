"""
Created on Sun Sep 22 13:36:22 2019.

@author: disbr007
"""

import argparse
import glob
import os
import subprocess
from subprocess import PIPE, STDOUT


def get_dems(src_dir, pair_dir):
    """
    Iterate over a subdirectory containing pairs.
    Returns two dems in date order.
    src_dir: directoring containing subdirectories
    pair_dir: subdirectory containing pairs
    """
    # Abs path to subdirectory
    dems_dir = os.path.join(src_dir, pair_dir)
    # Get all DEMs in subdir (should be two)
    dems_pattern = os.path.join(dems_dir, '*_dem.tif')
    dems = glob.glob(dems_pattern)

    # Identify old and new dems
    # Included index (i) in date to account for the same date  to
    # prevent overwriting the key
    # {date_[i]: dem_path}
    dems_dict = {'{}_{}'.format(os.path.split(x)[1].split('_')[1], i):x for i, x in enumerate(dems)}
    dem1, dem2 = dems_dict[sorted(dems_dict)[0]], dems_dict[sorted(dems_dict)[1]]
    if len(dems) == 2:
        return dem1, dem2
    else:
        print('Incorrect number of matching DEM files: {}'.format(len(dems)))


def batch_diff_strips(src_dir, output_dir, dryrun):
    """
    Run point2dem in batch on cluster using qsub
    src_dir: dir holding subdirs of paired 
    dryrun: flag to just print commands with no job submission
    """
    # List subdirectory names
    pairs = os.listdir(src_dir)

    for pair_dir in pairs:
        # Get DEMs in date order
        dem1, dem2 = get_dems(src_dir, pair_dir)
        out_pair_dir = os.path.join(output_dir, pair_dir)
        if not os.path.exists(out_pair_dir):
            os.mkdir(out_pair_dir)
        output_diff = os.path.join(out_pair_dir, '{}_diff_strips.tif'.format(pair_dir))

        if not os.path.exists(output_diff):
            # Build cmd
            if dryrun:
                dryrun == '--dryrun'
            cmd = 'qsub -v p1="{}",p2="{}",p3="{}" ~/scratch/code/coreg/qsub_diff_strips.sh'.format(dem2, dem1, output_diff)

            if dryrun:
                print(cmd)
            else:
                p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
                output = p.stdout.read()
                print(output)

def count_success(output_dir):
    """
    Count the number of directories with a *_diff.tif file
    """
    ctr = 0
    pairs = os.listdir(output_dir)

    for pair_dir in pairs:
        # Get DEMs in date order
        dem1, dem2 = get_dems(src_dir, pair_dir)
        out_pair_dir = os.path.join(output_dir, pair_dir)
        output_diff = os.path.join(out_pair_dir, '{}_diff_strips.tif'.format(pair_dir))
        if os.path.exists(output_diff):
            ctr += 1
    print('Diff files found: {}'.format(ctr))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('src_dir', type=os.path.abspath,
                        help='Path to directory holding pair directories')
    parser.add_argument('output_dir', type=os.path.abspath,
                        help='Path to write symlink to dem1, translated dem2, and diff.')
    parser.add_argument('--count', action='store_true',
                        help='Flag to just count *_diff.tif files.')
    parser.add_argument('--dryrun', action='store_true',
                        help='Print qsub commands without submitting')

    args = parser.parse_args()

    src_dir = args.src_dir
    output_dir = args.output_dir
    dryrun = args.dryrun

    if args.count:
        count_success(output_dir)
    else:
        batch_diff_strips(src_dir, output_dir, dryrun)
