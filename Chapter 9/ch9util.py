import dautil as dl
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
import seaborn as sns
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.learning_curve import learning_curve
from joblib import Memory
from sklearn.learning_curve import validation_curve
import numpy as np
from copy import deepcopy
import os

memory = Memory(cachedir='.')


@memory.cache(ignore=['X', 'y'])
def validate(est, X, y, pname, prange):
    est_cp = deepcopy(est)

    return validation_curve(est_cp, X, y, param_name=pname,
                            param_range=prange, n_jobs=1)


def plot_validation(ax, est, X, y, pname, prange):
    train_scores, test_scores = validate(est, X, y, pname, prange)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    ax.set_title("Validation Curve for " + pname)
    ax.set_xlabel(pname)
    ax.set_ylabel("Score")
    ax.plot(prange, train_scores_mean, label="Training score", color="r")
    ax.fill_between(prange, train_scores_mean - train_scores_std,
                    train_scores_mean + train_scores_std,
                    alpha=0.2, color="r")
    ax.plot(prange, test_scores_mean, 'g--', label="Cross-validation score")
    ax.fill_between(prange, test_scores_mean - test_scores_std,
                    test_scores_mean + test_scores_std, alpha=0.2, color="g")
    ax.legend(loc="best")


@memory.cache(ignore=['X', 'y'])
def learn(est, X, y):
    est_cp = deepcopy(est)

    return learning_curve(est_cp, X, y, n_jobs=-1)


def plot_learn_curve(ax, est, X, y, title=''):
    train_sizes, train_scores, test_scores = learn(est, X, y)

    ax.set_title('Learning Curve ' + title)
    ax.plot(train_sizes, train_scores.mean(axis=1), label="Train score")
    ax.plot(train_sizes, test_scores.mean(axis=1), '--', label="Test score")
    ax.legend(loc='best')
    ax.set_xlabel('Sample size')
    ax.set_ylabel('Score')


def npy_save(fname, arr):
    dir = dl.data.get_data_dir()
    dir = os.path.join(dir, 'PyDaCbkCh10')

    if not os.path.exists(dir):
        os.mkdir(dir)

    f = os.path.join(dir, fname)

    if not dl.conf.file_exists(f):
        np.save(f, arr)


def rain_split():
    df = dl.data.Weather.load()[['WIND_DIR', 'RAIN', 'PRESSURE']].dropna()
    df['RAIN'] = df['RAIN'] == 0

    X = df.values[:-1]
    y = df['RAIN'].values[1:]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=18)
    npy_save('rain_X_train', X_train)
    npy_save('rain_X_test', X_test)
    npy_save('rain_y_train', y_train)
    npy_save('rain_y_test', y_test)

    return X_train, X_test, y_train, y_test


def temp_split():
    df = dl.data.Weather.load()[['WIND_SPEED', 'TEMP', 'PRESSURE']].dropna()

    X = df.values[:-1]
    y = df['TEMP'].values[1:]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=18)
    npy_save('temp_X_train', X_train)
    npy_save('temp_X_test', X_test)
    npy_save('temp_y_train', y_train)
    npy_save('temp_y_test', y_test)

    return X_train, X_test, y_train, y_test


def report_rain(preds, y_test, params, ax=None):
    cax = ax

    if ax is None:
        cax = plt.gca()

    cm = confusion_matrix(preds.T, y_test)
    normalized_cm = cm/cm.sum().astype(float)
    sns.heatmap(normalized_cm, annot=True, fmt='.2f', vmin=0, vmax=1,
                xticklabels=['Rain', 'No Rain'],
                yticklabels=['Rain', 'No Rain'], ax=cax)
    cax.set_xlabel('Predicted class')
    cax.set_ylabel('Expected class')
    cax.set_title('Confusion Matrix for Rain Forecast')

    html = '<p style="font-size:5px;">Params {}</p>'.format(params)
    return html + '<p style="font-size:5px;">Accuracy {:.2f}</p>'.format(
        float(accuracy_score(preds.T, y_test)))


def scatter_predictions(preds, y_test, params, r2, ax=None):
    cax = ax

    if ax is None:
        cax = plt.gca()

    cax.scatter(preds, y_test, label='Predictions')
    cax.scatter(y_test, y_test, c='r', marker='.', label='Ideal')
    cax.legend(loc='upper left')
    cax.set_xlabel('Predicted')
    cax.set_ylabel('Expected')
    cax.set_title('Temperature Forecast')

    html = '<p style="font-size:5px;">Params {}</p>'.format(params)

    return html + '<p style="font-size:5px;">R^2 {:.2f}</p>'.format(r2)
