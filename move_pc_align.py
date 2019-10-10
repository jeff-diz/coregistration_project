#### Move outputs from pc_align and point2dem to
#### separate folders by pairname
import argparse
import os
import glob
import shutil

# src_dir = r'V:\pgc\data\scratch\jeff\coreg\data\pairs'
# dst_dir = r'V:\pgc\data\scratch\jeff\coreg\data\pc_align_reg'

# pc_patterns = (
# 			'*-DEM.tif',
# 			'*-log-point2dem*',
# 			'*-end_errors.csv',
# 			'*-beg_errors.csv*',
# 			'*-log-pc_align*',
# 			'*-transform.txt',
# 			# '*-inverse-transform.txt',
# 			'*-trans_source.tif*',
# 			'*-iterationInfo.csv'
# 			)

def move_pattern_files(src_dir, dst_dir, pattern):

	pair_dirs = os.listdir(src_dir)

	for pair_dir in pair_dirs:
		print(pair_dir)
		abs_pair_src_dir = os.path.join(src_dir, pair_dir)
		abs_pair_dst_dir = os.path.join(dst_dir, pair_dir)

		if not os.path.exists(abs_pair_dst_dir):
			os.mkdir(abs_pair_dst_dir)

		pc_files = tuple([os.path.join(abs_pair_src_dir, x) for x in pc_patterns])
		
		pca_matches = []

		for pca_f in pc_files:
			# print(pca_f)
			pca_f_matches = glob.glob(pca_f)
			pca_matches.extend(pca_f_matches)

		for src_f in pca_matches:
			dst_name = os.path.basename(src_f)
			dst_f = os.path.join(abs_pair_dst_dir, dst_name)
			shutil.move(src_f, dst_f)


def get_dems(src_dir, pair_dir):
    '''
    Iterate over a subdirectory containing pairs.
    Returns two dems in date order.
    src_dir: directoring containing subdirectories
    pair_dir: subdirectory containing pairs
    '''
    ## Abs path to subdirectory
    dems_dir = os.path.join(src_dir, pair_dir)
    ## Get all DEMs in subdir (should be two)
    dems = glob.glob(dems_dir, '*_dem.tif')
    
    # Identify old and new dems
    # Included index (i) in date to account for the same date  to
    # prevent overwriting the key
    # {date_[i]: dem_path}
    dems_dict = {'{}_{}'.format(os.path.split(x)[1].split('_')[1], i):x for i, x in enumerate(dems)}
    dem1, dem2 = dems_dict[sorted(dems_dict)[0]], dems_dict[sorted(dems_dict)[1]]

    return dem1, dem2


def rename_pc_align(dst_dir):
	## Rename pc_align
	## Correct misnaming of pc_align outputs
	pair_dirs = os.listdir(dst_dir)

	for pair_dir in pair_dirs:
		try:
			demA_name, demB_name = pair_dir.split('-')
		except ValueError:
			splits = pair_dir.split('_')
			demA_name = '_'.join(splits[:2])
			demB_name = '_'.join(splits[2:])
		# print(demA_name, demB_name)
		dems = [demA_name, demB_name]

		dems.sort(key = lambda x: x.split('_')[1])
		dem1_name, dem2_name = dems[0], dems[1]
		# print(dem1, dem2)
		if dem1_name == dem2_name:
			print('DEM names the same. Skipping.')
		else:	
			# abs_pair_src_dir = os.path.join(src_dir, pair_dir)
			abs_pair_dst_dir = os.path.join(dst_dir, pair_dir)

			if not os.path.exists(abs_pair_dst_dir):
				os.mkdir(abs_pair_dst_dir)

			pc_files = tuple([os.path.join(abs_pair_dst_dir, x) for x in pc_patterns])

			pca_matches = []

			for pca_f in pc_files:
				
				pca_f_matches = glob.glob(pca_f)
				pca_matches.extend(pca_f_matches)

			# print(pca_matches)

			for src_f in pca_matches:
				dirname, src_f_name = os.path.split(src_f)

				if src_f_name.startswith(dem2_name):
					_, suffix = src_f_name.split(dem2_name)

					dst_f = os.path.join(dirname, '{}{}'.format(dem1_name, suffix))
					print(src_f)
					print(dst_f)
					shutil.move(src_f, dst_f)


def add_sym_link2new(src_dir, dst_dir):

	pair_dirs = os.listdir(src_dir)

	for pair_dir in pair_dirs:
		try:
			demA_name, demB_name = pair_dir.split('-')
		except ValueError:
			splits = pair_dir.split('_')
			demA_name = '_'.join(splits[:2])
			demB_name = '_'.join(splits[2:])
		# print(demA_name, demB_name)
		dems = [demA_name, demB_name]

		dems.sort(key = lambda x: x.split('_')[1])
		dem1_name, dem2_name = dems[0], dems[1]

		dem2_pattern = os.path.join(src_dir, pair_dir, '{}*_dem.tif'.format(dem2_name))
		dem2_src = glob.glob(dem2_pattern)[0]
		dem2_f_name = os.path.basename(dem2_src)
		dem2_dst = os.path.join(dst_dir, pair_dir, dem2_f_name)

		if not os.path.exists(dem2_dst):
			# print(dem2_src)
			# print(dem2_dst)
			os.symlink(dem2_src, dem2_dst)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('src_dir', type=os.path.abspath,
		help='Path to source directory.')
	parser.add_argument('dst_dir', type=os.path.abspath,
		help='Path to the destination directory.')

	args = parser.parse_args()

	add_sym_link2new(args.src_dir, args.dst_dir)