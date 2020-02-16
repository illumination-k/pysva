import anndata
import numpy as np
import pandas as pd
import patsy
import random
from scipy.stats import rankdata
from scipy.linalg import svd


def calc_res(X, H):
    return X - (H @ X.T).T

def calc_dstat(res, idx):
    u, s, v = svd(res)
    return s[:idx]**2/np.sum(s[:idx]**2)

def num_sv(adata, model_matrix, method='be', vfilter=None, B=20, seed=None):
    if seed is not None:
        try:
            np.random.seed(seed)
        except:
            raise ValueError("seed should be integer")
    
    if vfilter is not None:
        if (vfilter < 100) or (vfilter > adata.shape[0]):
            raise ValueError("The number of genes used in the analysis must be between 100 and", str(adata.shape[0]),"\n")
        adata.obs['base_var'] = np.var(adata.X, ddof=1, axis=1)
        adata = adata[rankdata(-adata.obs['base_var']) < vfilter]
        
    if method not in ['be', 'leek']:
        raise ValueError('method should be "be" or "leek"')
        
    
    if method == 'be':
        H = model_matrix @ np.linalg.inv(model_matrix.T @ model_matrix) @ model_matrix.T
        res = calc_res(adata.X, H)
        idx = int(min(adata.shape) - np.ceil(np.sum(np.diag(H))))
        dstat = calc_dstat(res, idx)
        dstat0 = np.zeros((20, idx))
        for i in range(B):
            tmp_res = np.apply_along_axis(lambda x: random.sample(list(x), len(x)), 1, res)
            tmp_res = calc_res(tmp_res, H)
            dstat0[i, ] = calc_dstat(tmp_res, idx)
            
        psv = np.ones(adata.shape[1])
        for i in range(idx):
            psv[i] = np.mean(dstat0[:, i] >= dstat[i])
            
        for i in range(1, idx):
            psv[i] = max(psv[i-1], psv[i])
            
        nsv = np.sum(psv <= 0.10)
        return nsv


    