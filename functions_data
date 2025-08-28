import sys
import io

import os
import pandas as pd
import glob
from datetime import date
import numpy as np
import math

from sklearn import preprocessing
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from tempfile import NamedTemporaryFile
import urllib
from textwrap import wrap

def progpass(data):
  tl = data.copy()
  dfx = tl[['Act Name','Team','Action','X1','Y1','X2','Y2','Sub 4']]
  dfx['x1'] = dfx['X1']*1.05
  dfx['y1'] = dfx['Y1']*0.68
  dfx['x2'] = dfx['X2']*1.05
  dfx['y2'] = dfx['Y2']*0.68
  dfx = dfx[dfx['Action']=='passing'].reset_index(drop=True)
  dfx['beginning'] = np.sqrt(np.square(105-dfx['x1']) + np.square(34 - dfx['y1']))
  dfx['end'] = np.sqrt(np.square(105 - dfx['x2']) + np.square(34 - dfx['y2']))
  dfx['Type'] = ''

  for i in range(len(dfx)):
    if (dfx['beginning'][i] > 52.5) & (dfx['end'][i] > 52.5):
      if dfx['beginning'][i]-dfx['end'][i] >= 30:
        dfx['Type'][i] = 'Progressive'
      else:
        dfx['Type'][i] = 'Basic'
    elif (dfx['beginning'][i] >= 52.5) & (dfx['end'][i] <= 52.5):
      if dfx['beginning'][i]-dfx['end'][i] >= 15:
        dfx['Type'][i] = 'Progressive'
      else:
        dfx['Type'][i] = 'Basic'
    elif (dfx['beginning'][i] < 52.5) & (dfx['end'][i] < 52.5):
      if dfx['beginning'][i]-dfx['end'][i] >= 10:
        dfx['Type'][i] = 'Progressive'
      else:
        dfx['Type'][i] = 'Basic'
    else:
      dfx['Type'][i] = 'Basic'
  dfx = dfx[['Act Name','Team','X1','Y1','X2','Y2','Type']]

  dfy = dfx.groupby(['Act Name','Team','Type'], as_index=False).count()
  dfy = dfy[['Act Name','Team','Type','X1']]
  dfy = dfy[dfy['Type']=='Progressive'].sort_values(by='X1', ascending=False).reset_index(drop=True)

  return dfx, dfy
