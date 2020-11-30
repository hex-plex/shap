import numpy as np
from ..utils import safe_isinstance

def invariants(masker, *args):
    invariants = None
    if safe_isinstance(masker, "shap.maskers.FixedComposite"):
        if callable(getattr(masker, "invariants", None)):
            return masker.invariants(*args)
        else:
            raise AttributeError("FixedComposite masker must define 'invariants' attribute.")
    if callable(getattr(masker, "invariants", None)):
        invariants = masker.invariants(*args)
    return invariants

def variants(masker, *args):
    variants, variants_column_sums, variants_row_inds = None, None, None
    # if the masker supports it, save what positions vary from the background
    _invariants = invariants(masker, *args)
    if _invariants is not None:
        variants = ~_invariants
        variants_column_sums = variants.sum(0)
        variants_row_inds = [
            variants[:,i] for i in range(variants.shape[1])
        ]
    else:
        variants = None

    return variants, variants_column_sums, variants_row_inds

def shape(masker, *args):
    masker_rows, masker_cols = None, None
    if safe_isinstance(masker, "shap.maskers.FixedComposite"):
        if callable(getattr(masker, "shape", None)):
            return masker.shape(*args)
        else:
            raise AttributeError("FixedComposite masker must define 'shape' attribute.")
    # compute the length of the mask (and hence our length)
    if hasattr(masker, "shape"):
        if callable(masker.shape):
            mshape = masker.shape(*args)
            masker_rows = mshape[0]
            masker_cols = mshape[1]
        else:
            mshape = masker.shape
            masker_rows = mshape[0]
            masker_cols = mshape[1]
    else:
        masker_rows = None# # just assuming...
        masker_cols = sum(np.prod(a.shape) for a in args)

    return masker_rows, masker_cols

def data_transform(masker, s):
    if safe_isinstance(masker, "shap.maskers.FixedComposite"):
        if callable(getattr(masker, "data_transform", None)):
            return masker.data_transform(s)
        else:
            raise AttributeError("FixedComposite masker must define 'data_transform' attribute.")
    # transform data
    if hasattr(masker, "data_transform"):
        data = np.array([masker.data_transform(v) for v in s])
    else:
        data = s
    
    return data

def clustering(masker, *args):
    if safe_isinstance(masker, "shap.maskers.FixedComposite"):
        if callable(getattr(masker, "clustering", None)):
            return masker.clustering(*args)
        else:
            raise AttributeError("FixedComposite masker must define 'clustering' attribute.")
    is_dynamic_clustering = False
    if not callable(masker.clustering):
        clustering = masker.clustering
    else:
        if bool(args):
            clustering = masker.clustering(*args)
        else:
            clustering = None
        is_dynamic_clustering = True
    return clustering, is_dynamic_clustering