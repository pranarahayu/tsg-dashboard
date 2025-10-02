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
#from yellowbrick.cluster import KElbowVisualizer
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

def thirddata(data):
  dfx = data.copy()
  dfx = dfx[dfx['Action']=='passing']
  dfx['Ket.'] = 'basic'

  condition = (dfx['Pas Zone'].str.contains("5|6", na=False)) & (dfx['Act Zone'].str.contains("1|2|3|4", na=False))
  dfx.loc[condition, 'Ket.'] = '3rd'

  dfx = dfx[['Act Name','Team','Match','Action','X1','Y1','X2','Y2','Ket.']]

  dfy = dfx.groupby(['Act Name','Team','Match','Ket.'], as_index=False).count()
  dfy = dfy[['Act Name','Team','Match','Ket.','Action']]
  dfy = dfy[dfy['Ket.']=='3rd'].sort_values(by='Action', ascending=False).reset_index(drop=True)

  return dfx, dfy

def chance(data):
  dfx = data.copy()
  dfx = df2[(df2['Action']=='key pass') | (df2['Action']=='assist')]
  dfx = dfx[['Act Name','Team','Match','Action','X1','Y1','X2','Y2']]

  dfy = dfx[['Act Name','Team','X1']].groupby(['Act Name','Team'], as_index=False).count()
  dfy = dfy.sort_values(by='X1', ascending=False).reset_index(drop=True)

  return dfx, dfy

def gendata(data1, data2):
  #fin = pd.DataFrame()
  #gw_list = gw
  df = data1.copy()
  #df = df[df['Gameweek'].isin(gw)]
  #mac = df['Match'].unique().tolist()
  db = data2.copy()

  st = ['Match','Result','Gameweek','Date','Venue']
  st_data = df[st]
  st_data = st_data.groupby('Match', as_index=False).first()
  st_data['Home Team'] = st_data['Match'].str.split(' - ').str[0]
  st_data['Away Team'] = st_data['Match'].str.split(' - ').str[1]
  st_data['Home Score'] = st_data['Result'].str.split(' - ').str[0]
  st_data['Away Score'] = st_data['Result'].str.split(' - ').str[1]
  st_data['KO Time'] = st_data['Date'].str.split(' 1').str[1]
  st_data['KO Time'] = '1'+st_data['KO Time']
  st_data['Date'] = st_data['Date'].str.split(' 1').str[0]
  st_data['Date'] = pd.to_datetime(st_data['Date'])
  st_data['Day'] = st_data['Date'].dt.day_name()
  st_data['Week'] = ''
  for i in range(len(st_data)):
    if st_data['Gameweek'][i] < 10:
      st_data['Week'][i] = 'W-0'+str(st_data['Gameweek'][i])
    else:
      st_data['Week'][i] = 'W-'+str(st_data['Gameweek'][i])
  st_data = st_data[['Match','Home Team','Away Team','Home Score','Away Score','Week','Day','Date','KO Time','Venue']]

  nu = ['Match','Home/Away','Shot on','Shot off','Shot Blocked','Pass','Pass Fail',
        'Corner','Tackle','Offside','Own Goal','Foul','Yellow Card','Red Card']
  bp = ['Match','Home/Away','Ball Possession']
  bp_data = df[bp]
  nu_data = df[nu]
  nu_data = nu_data.groupby(['Match','Home/Away'], as_index=False).sum()
  bp_data = bp_data.groupby(['Match','Home/Away'], as_index=False).max()

  db = db[['Name','Nationality']]
  da = df[['Match','Home/Away','Name','Starter/Subs']]
  da = da[da['Starter/Subs']=='Starter'].reset_index(drop=True)
  da = pd.merge(da, db, on='Name', how='left')
  da['Status'] = 'Lokal'
  for i in range(len(da)):
    if da['Nationality'][i] != 'Indonesia':
      da['Status'][i] = 'Asing'
  da = da[['Match','Home/Away','Status']]
  da = da[da['Status']=='Asing'].reset_index(drop=True)
  da = da.groupby(['Match','Home/Away'], as_index=False).count()

  nu_data = pd.merge(nu_data, bp_data, on=['Match','Home/Away'], how='left')
  nu_data = pd.merge(nu_data, da, on=['Match','Home/Away'], how='left')

  nu_data['Shots'] = nu_data['Shot on']+nu_data['Shot off']+nu_data['Shot Blocked']
  nu_data['Shot on Target Ratio'] = nu_data['Shot on']/nu_data['Shots']
  hnu_data = nu_data[nu_data['Home/Away']=='Home'].reset_index(drop=True).drop(['Home/Away'], axis=1)
  hnu_data = hnu_data.rename(columns={'Shot on':'Shots on Target - Home','Shots':'Shots - Home','Shot on Target Ratio':'Shot on Target Ratio - Home',
                                      'Ball Possession':'Ball Possession (%) - Home','Pass':'Successful Passes - Home',
                                      'Pass Fail':'Passes Failed - Home','Corner':'Corner Kicks - Home','Tackle':'Successful Tackles - Home',
                                      'Offside':'Offsides - Home','Own Goal':'Own Goals - Home','Foul':'Fouls Commited - Home',
                                      'Yellow Card':'Yellow Cards - Home','Red Card':'Red Cards - Home','Status':'Starter Asing - Home'})

  anu_data = nu_data[nu_data['Home/Away']=='Away'].reset_index(drop=True).drop(['Home/Away'], axis=1)
  anu_data = anu_data.rename(columns={'Shot on':'Shots on Target - Away','Shots':'Shots - Away','Shot on Target Ratio':'Shot on Target Ratio - Away',
                                      'Ball Possession':'Ball Possession (%) - Away','Pass':'Successful Passes - Away',
                                      'Pass Fail':'Passes Failed - Away','Corner':'Corner Kicks - Away','Tackle':'Successful Tackles - Away',
                                      'Offside':'Offsides - Away','Own Goal':'Own Goals - Away','Foul':'Fouls Commited - Away',
                                      'Yellow Card':'Yellow Cards - Away','Red Card':'Red Cards - Away','Status':'Starter Asing - Away'})

  nu_data = pd.merge(hnu_data, anu_data, on=['Match'], how='left')
  metriks = ['Match','Starter Asing - Home','Starter Asing - Away','Shots on Target - Home','Shots on Target - Away','Shots - Home',
             'Shots - Away','Shot on Target Ratio - Home','Shot on Target Ratio - Away',
             'Ball Possession (%) - Home','Ball Possession (%) - Away','Successful Passes - Home','Successful Passes - Away',
             'Passes Failed - Home','Passes Failed - Away','Corner Kicks - Home','Corner Kicks - Away','Successful Tackles - Home',
             'Successful Tackles - Away','Offsides - Home','Offsides - Away','Own Goals - Home','Own Goals - Away','Fouls Commited - Home',
             'Fouls Commited - Away','Yellow Cards - Home','Yellow Cards - Away','Red Cards - Home','Red Cards - Away']
  nu_data = nu_data[metriks]

  datas = pd.merge(st_data, nu_data, on=['Match'], how='left')
  #fin = pd.concat([fin, datas], ignore_index=True)

  return datas

def findata(data1, data2, gw):
  gw_list = gw
  df = data1.copy()
  db = data2.copy()
  df = df[df['Gameweek'].isin(gw)]
  mac = df['Match'].unique().tolist()
  fin = pd.DataFrame()
  for i in mac:
    data = df[df['Match']==i]
    temp = gendata(data, db)
    fin = pd.concat([fin, temp], ignore_index=True)
  return fin
