#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 13:36:22 2019

@author: disbr007
"""

import argparse
import glob
import os
import subprocess
from subprocess import PIPE, STDOUT


def batch_apply_setsm_registration_groups(src_dir, output_dir, dryrun):
    '''
    Run point2dem in batch on cluster using qsub
    src_dir: dir holding subdirs of paired 
    dryrun: flag to just print commands with no job submission
    '''
     ## List subdirectory names   
    pairs = os.listdir(src_dir)
    
    for pair_dir in pairs:
        pair_dir_abs = os.path.join(src_dir, pair_dir)

        ## Build cmd
        cmd = 'qsub -v p1="{}",p2="{}" ~/scratch/code/coreg/qsub_apply_setsm_registration_group.sh'.format(src_dir, output_dir)
 
        if dryrun:
            print(cmd)
        else:
            p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            output = p.stdout.read()
            print(output)
            


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('src_dir', type=os.path.abspath,
        help='Path to directory holding pair directories')
    parser.add_argument('output_dir', type=os.path.abspath,
        help='Path to write symlink to dem1, translated dem2, and diff.')
    parser.add_argument('--dryrun', action='store_true',
        help='Print qsub commands without submitting')
    args = parser.parse_args()

    src_dir = args.src_dir
    output_dir = args.output_dir
    dryrun = args.dryrun

    batch_apply_setsm_registration_groups(src_dir, output_dir, dryrun)
    