# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 22:14:51 2019

@author: disbr007
"""

import argparse
import os
import logging

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_shp(csv_p):
    """
    Create shapefile from csv path provided
    csv should be formated:
        y,x,val1,val2
    """
    
    
    logger.info('Reading into dataframe...')
    csv_df = pd.read_csv(csv_p)
    
    cols = list(csv_df)
    
    if 'y' in cols:
        ycol = 'y'
    elif ' y' in cols:
        ycol = ' y'
    if ' x' in cols:
        xcol = ' x'
    elif 'x' in cols:
        xcol = 'x'
    if ' val1' in cols:
        val1 = ' val1'
    elif 'val1' in cols:
        val1 = 'val1'
    if ' val2' in cols:
        val2 = ' val2'
    elif 'val2' in cols:
        val2 = 'val2'

    float_type = 'float64'
    col_types = {xcol:float_type, ycol:float_type, val1:float_type, val2:float_type}
    csv_df = csv_df.astype(col_types)

    def create_point(x, y):
        """
        create a shapely Point from x, y coordinates
        """

        pt = Point(x,y)

        return pt

    logger.info('Calculating differences...')
    csv_df['diff'] = csv_df[val1] - csv_df[val2]
    csv_df['abs_diff'] = abs(csv_df['diff'])
    logger.info('Creating geometries from coordinates...')
    csv_df['geometry'] = csv_df.apply(lambda x: create_point(x[xcol], x[ycol]), axis=1)

    gdf = gpd.GeoDataFrame(csv_df, geometry='geometry', crs={'init':'epsg:3413'})
    
    out_dir = os.path.split(csv_p)[0]
    out_name = os.path.split(out_dir)[1]
    out_shp = os.path.join(out_dir, '{}.shp'.format(out_name))
    #    out_json = os.path.join(out_dir, '{}.json'.format(out_name))
    logger.info('Writing points to file: {}'.format(out_shp))
    gdf.to_file(out_shp, driver='ESRI Shapefile')
    #    gdf.to_file(out_json, driver='GeoJSON')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('csv', type=os.path.abspath,
                        help='Path to csv holding coordinate and error info.')
    
    args = parser.parse_args()
    logger.info(args.csv)
    create_shp(args.csv)
    logger.info('Done')