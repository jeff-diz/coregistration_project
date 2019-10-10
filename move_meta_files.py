"""Move meta data files associated with DEMs."""

import argparse
import glob
import os


def move_meta(src_dir, dst_dir):
	pairs = os.listdir(src_dir)

	for p in pairs:
		patterns = ('*_matchtag*', '*_meta.txt', '*_reg.txt')
		files_grabbed = []
		for pattern in patterns:
			f_pattern = os.path.join(src_dir, p, pattern)
			files_grabbed.extend(glob.glob(f_pattern))

		for f in files_grabbed:
			f_name = os.path.basename(f)
			dst_f = os.path.join(dst_dir, p, f_name)
			print(dst_f)
			if not os.path.exists(dst_f):
				print('making symlink')
				os.symlink(f, dst_f)
if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('src_dir', type=os.path.abspath,
    					help='Path to directory holding pair directories')
	parser.add_argument('dst_dir', type=os.path.abspath,
						help='Path to write symlink to meta files.')
	args = parser.parse_args()

	move_meta(args.src_dir, args.dst_dir)
