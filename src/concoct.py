#!/usr/bin/env python
import fileinput
import sys
import os
from argparse import ArgumentParser

import itertools
from scipy import linalg
import pylab as pl
import matplotlib as mpl


import pandas as p
import sklearn.mixture as mixture
from sklearn import preprocessing
import numpy as np


def main(coverage_file,output_base,n_components,header=None):
    df = p.read_csv(coverage_file,header=header,index_col=0)
    X = df.values
    X = preprocessing.scale(X)
    cv_type='full'

    # Fit a mixture of gaussians with EM
    gmm = mixture.GMM(n_components=n_components, covariance_type=cv_type)
    gmm.fit(X)
    labels = gmm.predict(X)
    bic = gmm.bic(X)
    convergence = gmm.converged_
    sys.stderr.write('Convergence: ' + str(convergence) +'\n')
    class_series = p.Series(labels,index=df.index)
    setting = str(n_components)+"_" + str(cv_type)
    
    class_series.to_csv(output_base+"_" +setting+str(gmm.bic(X))+ '.csv')
    
if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument('coverage',
                        help='specify the coverage file')
    parser.add_argument('-o','--output',
                        help='specify the output base file_name, the number of components and cv_type will be added to this file name.')
    parser.add_argument('--n_start', type=int,
                        help='The number of clusters to.')
    parser.add_argument('--header', action='store_true',
                        help='Use this tag if header is included in coverage file')
    args = parser.parse_args()

    if not args.output:
       sys.exit(-1) 
    if args.header:
        header=0
    else:
        header=None

    main(args.coverage,args.output,args.n_start,header)

