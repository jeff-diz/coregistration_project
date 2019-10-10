#!/bin/bash

#PBS -l walltime=40:00:00,nodes=1:ppn=2
#PBS -m n
#PBS -k oe
#PBS -j oe


## Expected environment variables (passed with -v argument)
# p1 :: Pair directory
# p2 :: Destination directory

cd $PBS_O_WORKDIR

echo $PBS_JOBID
echo $PBS_O_HOST
echo $PBS_NODEFILE

module load gdal/2.1.3
module load asp

echo $p1 $p2
python ~/scratch/code/cloned_repos/pgcdemtools/apply_setsm_registration_groups.py $p1 --dstdir $p2 --groups