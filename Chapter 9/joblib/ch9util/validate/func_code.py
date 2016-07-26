# first line: 17
@memory.cache(ignore=['X', 'y'])
def validate(est, X, y, pname, prange):
    est_cp = deepcopy(est)

    return validation_curve(est_cp, X, y, param_name=pname,
                            param_range=prange, n_jobs=1)
