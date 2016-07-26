import numpy as np
import dautil as dl
from sklearn.utils import check_random_state


def classifiers():
    return '''
bagging -  BaggingClassifier {'n_estimators': 320, 'bootstrap_features': True, 'base_estimator__criterion': 'gini'}
default = DecisionTreeClassifier(random_state=53, min_samples_leaf=3, max_depth=4)
entropy = DecisionTreeClassifier(criterion='entropy', min_samples_leaf=3, max_depth=4, random_state=57)
random = DecisionTreeClassifier(splitter='random', min_samples_leaf=3, max_depth=4, random_state=5)
rfc - RandomForestClassifier  {'min_samples_leaf': 3, 'n_estimators': 100, 'max_depth': 4, 'criterion': 'gini'}
stacking - DecisionTreeClassifier
votes - VotingClassifier {'voting': 'soft', 'weights': (2, 1, 1)}
'''


def regressors():
    return '''
boosting - AdaBoostRegressor {'base_estimator__min_samples_leaf': 2,
'loss': 'exponential'}
etr = ExtraTreesRegressor{'min_samples_leaf': 4,
'bootstrap': True, 'min_samples_split': 1}
ransac - RANSACRegressor {'stop_probability': 0.99, 'max_trials': 50}
'''


def plot_bars(ax, vals, labels=None, rotate=False):
    if labels is None:
        dl.plotting.bar(ax, rain_labels(), vals)
        ax.set_ylim(min(vals) - 0.03, max(vals))
    else:
        dl.plotting.bar(ax, labels, vals)

        if rotate:
            ax.set_xticklabels(labels, rotation='vertical')


def temp_labels():
    return ['boosting', 'etr', 'ransac']


def rain_labels():
    return ['bagging', 'default', 'entropy', 'random',
            'rfc', 'stacking', 'votes']


def rain_preds():
    files = rain_labels()

    return [np.load(f + '.npy').T for f in files]


def temp_preds(full=False):
    files = temp_labels()

    return [np.load(f + '.npy').T for f in files]


def plot_bootstrap(reg, func, ax):
    rs = check_random_state(34)
    y_test = np.load('temp_y_test.npy')
    n = len(y_test)
    preds = np.load(reg + '.npy')
    stats = []

    for i in range(500):
        indices = rs.choice(n, size=n)
        stats.append(func(y_test[indices], preds[indices]))

    dl.plotting.hist_norm_pdf(ax, np.array(stats))
    ax.set_ylabel('Frequency')
    ax.axvline(func(preds, y_test), color='k',
               lw=3, label=reg + ' Observed')
