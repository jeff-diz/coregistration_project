import argparse
import logging
import numpy as np
import os
from osgeo import gdal, osr
import random

from lib.RasterWrapper import Raster

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def raster_bounds(raster_obj):
    '''
    GDAL only version of getting bounds for a single raster.
    '''
#    src = raster_obj.data_src
    gt = raster_obj.geotransform
    ulx = gt[0]
    uly = gt[3]
    lrx = ulx + (gt[1] * raster_obj.x_sz)
    lry = uly + (gt[5] * raster_obj.y_sz)
    logger.info('Raster bounds: {}'.format([ulx, uly, lrx, lry]))
    return ulx, lry, lrx, uly

    
def minimum_bounding_box(raster_objs):
    '''
    Takes a list of DEMs (or rasters) and returns the minimum bounding box of all in
    the order of bounds specified for gdal.Translate.
    dems: list of dems
    '''
    ## Determine minimum bounding box
    ulxs, lrys, lrxs, ulys = list(), list(), list(), list()
    #geoms = list()
    for r in raster_objs:
        ulx, lry, lrx, uly = raster_bounds(r)
        ulxs.append(ulx)
        lrys.append(lry)
        lrxs.append(lrx)
        ulys.append(uly)        
    
    ## Find the smallest extent of all bounding box corners
    ulx = max(ulxs)
    uly = min(ulys)
    lrx = min(lrxs)
    lry = max(lrys)

    projWin = [ulx, uly, lrx, lry]
    logger.info('Computed projWin: {}'.format(projWin))
    return projWin


def calc_rmse(l1, l2):
    '''
    Calculates RMSE of two lists of numbers.
    '''
    # debug
    for x in l1:
        if type(x) != np.float32:
            print('not a float: {}'.format(x))
            print(type(x))
        else:
            pass
    for x in l2:
        if type(x) != np.float32:
            print('not a float: {}'.format(x))
            print(type(x))
    
    diffs = [x - y for x, y in zip(l1, l2)]
    sq_diff = [x**2 for x in diffs]
    mean_sq_diff = sum(sq_diff) / len(sq_diff)
    rmse_val = np.sqrt(mean_sq_diff)
    
    return rmse_val


def sample_random_points(dem1, dem2, n):
    """
    Generates n random points within projWin [ulx, uly, lrx, lry]
    """
    logger.info('Sampling DEMs at {} points.'.format(n))
    # Get DEM no data values
    dem1_nodata = dem1.nodata_val
    dem2_nodata = dem2.nodata_val
    
    # Get overlap bounding box
    projWin = minimum_bounding_box([dem1, dem2])
#    minx, maxy, maxx, miny = projWin
    ulx, uly, lrx, lry = projWin
    
    # Use pixel sizes to avoid selecting last col/row
    # height is negative (min)
    max_pix_height = min([dem1.pixel_height, dem2.pixel_height])
    max_pix_width = max([dem1.pixel_width, dem2.pixel_width])
    

    # Sample random points, storing the points+differences, and sampled values
    sample_pts_vals = []
    ctr = 0
    max_tries = 10000000
    
    logging.info('Random point bounds: ')
    logging.info('low y: {}'.format(lry-max_pix_height))
    logging.info('upp y: {}'.format(uly))
    logging.info('low x: {}'.format(ulx))
    logging.info('upp x: {}'.format(lrx-max_pix_width))
    
    while len(sample_pts_vals) < n:
        pt = (round(random.uniform(lry-max_pix_height, uly),3),
              round(random.uniform(ulx, lrx-max_pix_width),3))
        
        val1 = dem1.SamplePoint(pt)
        val2 = dem2.SamplePoint(pt)
        
        if (val1 != dem1_nodata and val2 != dem2_nodata):
            sample_pts_vals.append((pt, val1, val2))
        else:
            pass
        
        ctr += 1
        if ctr % 100000 == 0:
            logging.info('Sample points tried: {}'.format(ctr))
            logging.info('Sample points kept : {}'.format(len(sample_pts_vals)))
        if ctr >= max_tries:
            logging.debug('Max. sample tries reached: {}'.format(ctr))
            break
    logger.info('Total points sampled: {}'.format(len(sample_pts_vals)))
    
    return sample_pts_vals

    
def dem_RMSE(dem1_p, dem2_p, n):
    """
    Calculate RMSE for two DEMs from
    n sample points
    """
    logger.info('Loading DEMs...')
    dem1 = Raster(dem1_p)
    dem2 = Raster(dem2_p)
    
    logger.info('Sampling points...')
    sample_pts_vals = sample_random_points(dem1, dem2, n=n)
    pt, dem1_vals, dem2_vals = zip(*sample_pts_vals)
    
    rmse = calc_rmse(dem1_vals, dem2_vals)
    logger.info('RMSE: {}'.format(rmse))
    
    return sample_pts_vals, rmse

dem1_p = r'V:\pgc\data\scratch\jeff\coreg\data\pairs\WV02_20130523-WV02_20160407\WV02_20130523_10300100233C8A00_10300100238A9900_seg1_2m_dem.tif'
dem2_p = r'V:\pgc\data\scratch\jeff\coreg\data\pairs\WV02_20130523-WV02_20160407\WV02_20160407_1030010052AFFF00_10300100534D3900_seg1_2m_dem.tif'

#dem1 = Raster(dem1_p)
#dem2 = Raster(dem2_p)

#pts_vals = sample_random_points(dem1, dem2, 10000000)
pts_vals, rmse = dem_RMSE(dem1_p, dem2_p, n=100000)