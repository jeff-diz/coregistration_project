# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 11:53:49 2019

@author: disbr007
"""

import geopandas as gpd

pts_p = r'V:\pgc\data\scratch\jeff\coreg\data\icesat_reg\WV02_20120522-WV02_20170413\WV02_20120522-WV02_20170413.shp'
pts = gpd.read_file(pts_p, driver='ESRI Shapefile')