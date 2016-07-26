# first line: 45
@memory.cache(ignore=['X', 'y'])
def learn(est, X, y):
    est_cp = deepcopy(est)

    return learning_curve(est_cp, X, y, n_jobs=-1)
