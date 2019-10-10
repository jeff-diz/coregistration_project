"""Parse jobfile logs for erros and count"""

import argparse
import os
import glob
from pprint import pprint
import re


def count_comm_errs(src_dir, jobid_range):
	jobids = [x for x in range(jobid_range[0], jobid_range[1])]

	common_errors = {'AssertionError': 0, 'OverflowError:': 0, 'No errs found': 0, 'RMSE': 0}

	for jobid in jobids:
		pattern = os.path.join(src_dir, '*{}*'.format(jobid))
		matches = glob.glob(pattern)
		if len(matches) > 0:
			for m in matches:
				print('parsing: {}'.format(m))
				with open(m, 'r') as logfile:
					for err in common_errors.keys():
						err_found = False
						filetext = logfile.read()
						filetext = filetext.strip()
						print(filetext)
						# if err in filetext:
						if filetext.find(err) != -1:
							err_found = True
							common_errors[err] += 1
					if err_found is False:
						common_errors['No errs found'] += 1

	pprint(common_errors)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('src_dir', type=os.path.abspath,
						help='directory to parse for job files')
	parser.add_argument('jobid_min', type=int,
						help='starting job id to parse')
	parser.add_argument('jobid_max', type=int,
						help='ending job id to parse')

	args = parser.parse_args()

	jobid_range = (args.jobid_min, args.jobid_max)

	count_comm_errs(args.src_dir, jobid_range)
