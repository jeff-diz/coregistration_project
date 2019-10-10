import argparse
import os


def count_subdir_files(src_dir):
	pairs = os.listdir(src_dir)

	for p in pairs:
		files = os.listdir(os.path.join(src_dir, p))
		if len(files) > 1:
			print('{}: {}'.format(p, len(files)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('src_dir', type=os.path.abspath,
        help='Path to directory holding pair directories')
    args = parser.parse_args()

    src_dir = args.src_dir

    count_subdir_files(src_dir)