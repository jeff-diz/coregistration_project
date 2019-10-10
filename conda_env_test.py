from __future__ import division
import copy
import math
import operator
import os
import sys
from collections import deque
from itertools import product
from PIL import Image
from warnings import warn

import cv2
import gdal, ogr, osr
import numpy as np
import scipy
import shapely.geometry
import shapely.ops
from osgeo import gdal_array
from scipy import ndimage as sp_ndimage
from skimage.draw import polygon_perimeter
from skimage import morphology as sk_morphology
from skimage.filters.rank import entropy
from skimage.util import unique_rows

print('Imported rat packages successfully.')
if sys.version_info[0] < 3:
    from DecimatePoly import DecimatePoly
else:
    from lib.DecimatePoly import DecimatePoly

# from __future__ import division
import argparse
import filecmp
import os
from datetime import datetime

import numpy as np

import lib.raster_array_tools as rat
from lib.scenes2strips import coregisterdems
from batch_scenes2strips import getDemSuffix, selectBestMatchtag

print('Imported all successfully.')