# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 19:10:52 2019

@author: disbr007
"""


import argparse
import glob
import logging
import os
import subprocess
from subprocess import PIPE, STDOUT


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def batch_RMSE_err_pts(src_dir, overwrite, dryrun):
    """
    Run point2dem in batch on cluster using qsub
    src_dir: dir holding subdirs of paired 
    dryrun: flag to just print commands with no job submission
    """
    
    def submit_job(csv_p, dryrun):
        
        # Build cmd
        cmd = 'qsub -v p1="{}" ~/scratch/code/coreg/qsub_RMSE_err_shp.sh'.format(csv_p)

        if dryrun:
            print(cmd)
        else:
            p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            output = p.stdout.read()
            print(output)

    # List all sample_pts.csv files
    pt_csv_matches = glob.glob(os.path.join(src_dir, '*', '*', '*sample_pts.csv'))

    for csv in pt_csv_matches:
        print(csv)
        if overwrite:
            submit_job(csv, dryrun)
        else:
            outshp_name = '{}.shp'.format(os.path.split(csv)[1][0:29])
            out_shp = os.path.join(os.path.split(csv)[0], outshp_name)
            if not os.path.exists(out_shp):
                submit_job(csv, dryrun)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('src_dir', type=os.path.abspath,
                        help='''Directory holding pair subdirectories
                        with .tifs to calculate RMSE on.''')
    parser.add_argument('--overwrite', action='store_true',
                        help='overwrite existing shapefiles.')
    parser.add_argument('--dryrun', action='store_true',
                        help='Print qsub commands without submitting them.')
    
    args = parser.parse_args()
    
    batch_RMSE_err_pts(args.src_dir, overwrite=args.overwrite, dryrun=args.dryrun)
