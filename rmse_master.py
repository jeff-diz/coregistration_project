"""
Created on Sat Sep 28 18:08:16 2019

@author: disbr007
"""

import glob
import numpy as np
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

from query_danco import query_footprint



def get_dem_names(row, src_dir):
    '''
    Get the two dem names from a given pair subdir
    '''
    pairs = row['pair']
    dem1_start, dem2_start = pairs[0:13], pairs[14:]
    src = os.path.join(src_dir, pairs)
    pattern = os.path.join(src, '*dem.tif')
    dems = glob.glob(pattern)
    dem_names = [os.path.split(d)[1] for d in dems]
#    dem1_name = dem_names[0]
#    dem2_name = dem_names[1]
    
    dem1_name = [n for n in dem_names if n.startswith(dem1_start)][0]
    dem2_name = [n for n in dem_names if n.startswith(dem2_start)][0]
    return (dem1_name, dem2_name)


def get_num_gcps(row, index):
    '''
    Looks up the number of icesat GCPs in the index table for each row
    '''
    dem1_name = row['dem1_name']
    dem2_name = row['dem2_name']
    
    dem1_src = index[index['dem_name']==dem1_name]
    dem2_src = index[index['dem_name']==dem2_name]
    
    dem1_gcp = int(dem1_src['num_gcps'].values[0])
    dem2_gcp = int(dem2_src['num_gcps'].values[0])

    return (dem1_gcp, dem2_gcp)

    
def get_rmse(row, src_dir):
    '''
    Parse .txt files containing calculated RMSE's.
    '''
    pair = row['pair']
#    print(pair)
    pair_dir = os.path.join(src_dir, pair)
    pattern = os.path.join(pair_dir, '*rmse.txt')
#    print(pattern)
    rmse_files = glob.glob(pattern)
    if len(rmse_files) == 1:
        with open(rmse_files[0], 'r') as rf:
            rmse = rf.read()
            rmse = float(rmse)
            return rmse
    else:
        return -9999.0


def get_missing(master_df, method):
    """
    Gets the missing values for the given method
    """
    missing = list(master_df['pair'][(master_df[method]==-9999) |
            (np.isnan(master_df[method]))])
    return missing


#### Paths
# Setsm danco footprint
setsm_strip_index = query_footprint('pgc_dem_setsm_strips')

# Directory containing all pulled data and aligned
src_dir = r'V:\pgc\data\scratch\jeff\coreg\data'

raw_dir = os.path.join(src_dir, 'pairs')
icesat_dir = os.path.join(src_dir, 'icesat_reg')
pca_dir = os.path.join(src_dir, 'pc_align_reg')
nuth_dir = os.path.join(src_dir, 'nuth_reg')

# Master shapefile
shp_p = r'E:\disbr007\umn\ms_proj_2019jul05\data\shapefile\coreg_master.shp'


#### Create master dataframe
# Columns to create in df
columns = ['pair', 'rmse_none', 'rmse_pca', 'rmse_nuth', 'rmse_ice']
master = pd.DataFrame(columns=columns)
pairs = os.listdir(os.path.join(src_dir, 'pairs'))
# Add column with names of pairs
master['pair'] = pairs
# Parse directories for *rmse.txt
methods = ['rmse_none', 'rmse_ice', 'rmse_pca', 'rmse_nuth']
master['rmse_none'] = master.apply(lambda x: get_rmse(x, raw_dir), axis=1)
master['rmse_ice'] = master.apply(lambda x: get_rmse(x, icesat_dir), axis=1)
master['rmse_pca'] = master.apply(lambda x: get_rmse(x, pca_dir), axis=1)
master['rmse_nuth'] = master.apply(lambda x: get_rmse(x, nuth_dir), axis=1)

## Convert -9999 to nan
master[master==-9999] = np.nan
col_rename = {'rmse_none': 'No Alignment',
              'rmse_ice': 'ICESAT GCPs',
              'rmse_pca': 'NASA AMES Point Cloud Align',
              'rmse_nuth': 'Gradient Descent Nuth and Kaab (2011)'}
master.rename(columns=col_rename, inplace=True)

## Dataframe of summary stats
summary = master.describe()


## Get DEM names for finding ICESAT GCP numbers and other master info
master['dem1_name'], master['dem2_name'] = zip(*master.apply(lambda x: get_dem_names(x, raw_dir), axis=1))
master['dem1_n_gcps'], master['dem2_n_gcps'] = zip(*master.apply(lambda x: get_num_gcps(x, setsm_strip_index), axis=1))



## Load shape
#shp = gpd.read_file(shp_p)
#
## Join csv to shapefile
#shp = shp.merge(master, on='pair')
#
## Write
#outdir = os.path.dirname(shp_p)
#out_name = '{}_rmse.shp'.format(os.path.split(shp_p)[1].split('.')[0])
#out_shp = os.path.join(outdir, out_name)
#shp.to_file(out_shp, driver='ESRI Shapefile')


#### Plotting
plt.style.use('ggplot')
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,10))
rmse_cols = ['No Alignment', 'NASA AMES Point Cloud Align', 'Gradient Descent Nuth and Kaab (2011)', 'ICESAT GCPs']
master[rmse_cols].plot.kde(ax=ax1)

for col in rmse_cols:
    master[col].hist(ax=ax2, alpha=0.5, label=col, bins=20)
#ax.set_title('RMSE Density')
for ax in (ax1, ax2):
    ax.set(xlabel='RMSE')
#    ax.set_ylim(0, 35)


#    ax.annotate('{}: mean {}', xy=(2, 1), xytext=(3, 1.5),
#            arrowprops=dict(facecolor='black', shrink=0.05),
#            )
