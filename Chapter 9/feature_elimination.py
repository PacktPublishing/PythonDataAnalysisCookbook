from sklearn.feature_selection import RFE
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
import dautil as dl
import warnings
import numpy as np

warnings.filterwarnings("ignore", category=DeprecationWarning)
clf = SVC(random_state=42, kernel='linear')
selector = RFE(clf)

df = dl.data.Weather.load().dropna()
df['RAIN'] = df['RAIN'] == 0
df['DOY'] = [float(d.dayofyear) for d in df.index]
scaler = MinMaxScaler()

for c in df.columns:
    if c != 'RAIN':
        df[c] = scaler.fit_transform(df[c])

dl.options.set_pd_options()
print(df.head(1))
X = df[:-1].values
np.set_printoptions(formatter={'all': '{:.3f}'.format})
print(X[0])
np.set_printoptions()

y = df['RAIN'][1:].values
selector = selector.fit(X, y)
print('Rain support', df.columns[selector.support_])
print('Rain rankings', selector.ranking_)

reg = SVR(kernel='linear')
selector = RFE(reg)
y = df['TEMP'][1:].values
selector = selector.fit(X, y)
print('Temperature support', df.columns[selector.support_])
print('Temperature ranking', selector.ranking_)
