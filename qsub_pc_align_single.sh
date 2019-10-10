#!/bin/bash

#PBS -l walltime=40:00:00,nodes=1:ppn=2
#PBS -m n
#PBS -k oe
#PBS -j oe

## Expected environment variables (passed with -v argument)
# p1 :: Reference DEM
# p2 :: Source DEM (to be translated)
# p3 :: Output prefix: abs path to pair directory

## Does this change my cwd?
cd $PBS_O_WORKDIR

echo $PBS_JOBID
echo $PBS_O_HOST
echo $PBS_NODEFILE

module load gdal/2.1.3
module load asp


echo $p1 $p2 $p3

# pc_align --max-displacement 10.0 --save-transformed-source-points coreg/data/pc_align_reg/WV02_20150912_WV03_20150910/WV02_20150912_103001004805F200_1030010048CF3300_seg2_2m_dem.tif coreg/data/pc_align_reg/WV02_20150912_WV03_20150910/WV03_20150910_1040010010401D00_1040010011C86F00_seg3_2m_dem.tif -o coreg/data/pc_align_reg/WV02_20150912_WV03_20150910/
point2dem coreg/data/pc_align_reg/WV02_20150912_WV03_20150910/-trans_source.tif -o coreg/data/pc_align_reg/WV02_20150912_WV03_20150910/WV03_20150910
