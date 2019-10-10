

def constrict_pairs(run_pairs_f, pairs):
	'''
	Run only pairs in run_pairs_f txt file,
	by removing any pairs not in that file
	from pairs.
	'''
	if run_pairs_f:
	    with open(run_pairs_f) as rpf:
	        run_pairs = rpf.readlines()
	        run_pairs = [x.strip() for x in run_pairs]
	        pairs = [x for x in pairs if x in run_pairs]
	return pairs