# this is a script to generate test data for the project
# select randomly 100 to 1000 genes from hgnc_symbol in the DEPrior_gini_g2p.txt
# add randomly generated FDR score < 0.05 to the matrix
# Also add add randomly generated logFC value to the matrix
# and save it as test_data.csv

import pandas as pd
import numpy as np
import os
import random
import argparse

def main(x):
	# seed setting
	random.seed(x)
	np.random.seed(x)

	df = pd.read_csv("resources/DEPrior_gini_g2p.txt", sep="\t")

	# select random number from 100 to 1000 
	rand_n = random.randint(100, 1000)

	# select random genes from hgnc_symbol
	rand_genes = random.sample(list(df["hgnc_symbol"]), rand_n)

	# select random FDR score < 0.05
	# final lenght is same as rand_n
	rand_FDR = np.random.rand(rand_n) * 0.05

	# select random logFC
	rand_logFC = np.random.rand(rand_n)

	# create test data
	test_data = pd.DataFrame({
		"hgnc_symbol": rand_genes,
		"logFC": rand_logFC,
		"FDR": rand_FDR,
	})

	return test_data
	# save test data
	# file name has seed in it

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate test data for Clover')
	parser.add_argument("--seed", "-s",
					type=int,
					default=1,
					help="seed number")
	args = parser.parse_args()

	test_data = main(args.seed)
	test_data.to_csv(f"test_data_{args.seed}.csv", index=False)


