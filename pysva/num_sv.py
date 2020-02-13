import anndata
import pasty
import numpy as np
import pandas as pd


def num_sv(adata, model_matrix, method='be', vfilter=None, B=20, seed=None):
    if seed is not None:
        try:
            np.random.seed(seed)
        except:
            raise ValueError("seed should be integer")

    if vfilter is not None:


    