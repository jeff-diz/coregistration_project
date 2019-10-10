#!/bin/bash

#PBS -l walltime=40:00:00,nodes=1:ppn=2
#PBS -m n
#PBS -k oe
#PBS -j oe


## Expected environment variables (passed with -v argument)
# p1 :: Reference DEM
# p2 :: Comparison DEM (to be translated)
# p3 :: Output path for diff DEM (dir with be used for other outputs)

source /mnt/pgc/data/scratch/jeff/build/miniconda3/bin/activate nk

cd $PBS_O_WORKDIR

echo $PBS_JOBID
echo $PBS_O_HOST
echo $PBS_NODEFILE

echo $p1 $p2 $p3
python ~/scratch/code/cloned_repos/setsm_postprocessing_python/diff_strips.py $p1 $p2 -o $p3 -m
