import os
import pandas as pd
import glob
from datetime import date
import numpy as np
from sklearn import preprocessing

from mplsoccer import Pitch, VerticalPitch, PyPizza, Radar, grid
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.font_manager as fm
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as patches
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)

from PIL import Image
from tempfile import NamedTemporaryFile
import urllib
import os

github_url = 'https://github.com/google/fonts/blob/main/ofl/poppins/Poppins-Bold.ttf'
url = github_url + '?raw=true'

response = urllib.request.urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()

bold = fm.FontProperties(fname=f.name)

github_url = 'https://github.com/google/fonts/blob/main/ofl/poppins/Poppins-Regular.ttf'
url = github_url + '?raw=true'

response = urllib.request.urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()

reg = fm.FontProperties(fname=f.name)

path_eff = [path_effects.Stroke(linewidth=2, foreground='#ffffff'),
            path_effects.Normal()]

def progressive_plot(data, player):
  dfx = data.copy()
  fig, ax = plt.subplots(figsize=(20, 20), dpi=500)
  fig.patch.set_facecolor('#FFFFFF')
  ax.set_facecolor('#FFFFFF')
  pitch = Pitch(pitch_type='wyscout', pitch_color='#FFFFFF', line_color='#346594',
                corner_arcs=True, goal_type='circle', linewidth=1.5, pad_bottom=5)
  pitch.draw(ax=ax)

  dfx = dfx[dfx['Act Name']==player].reset_index(drop=True)
  for i in range(len(dfx)):
    if dfx['Type'][i] == 'Basic':
      pitch.arrows(dfx['X1'][i], dfx['Y1'][i], dfx['X2'][i], dfx['Y2'][i], alpha=0.05,
                   width=2, headwidth=5, headlength=5, color='#000000', ax=ax)
    else:
      pitch.arrows(dfx['X1'][i], dfx['Y1'][i], dfx['X2'][i], dfx['Y2'][i], alpha=0.75,
                   width=2, headwidth=5, headlength=5, color='#ff0004', ax=ax)

  ax.text(0, -7, player, ha='left', fontproperties=bold, color='#000000', size='28', va='center')
  ax.text(0, -3.5, 'Progressive Passes', ha='left', fontproperties=reg, color='#000000', size='20', va='center')

  return fig

def third_plot(data, player):
  dfx = data.copy()

  fig, ax = plt.subplots(figsize=(20, 20), dpi=500)
  fig.patch.set_facecolor('#FFFFFF')
  ax.set_facecolor('#FFFFFF')
  pitch = Pitch(pitch_type='wyscout', pitch_color='#FFFFFF', line_color='#346594',
                corner_arcs=True, goal_type='circle', linewidth=1.5, pad_bottom=5)
  pitch.draw(ax=ax)

  dfx = dfx[dfx['Act Name']==player].reset_index(drop=True)
  for i in range(len(dfx)):
    if dfx['Ket.'][i] == 'basic':
      pitch.arrows(dfx['X1'][i], dfx['Y1'][i], dfx['X2'][i], dfx['Y2'][i], alpha=0.05,
                   width=2, headwidth=5, headlength=5, color='#000000', ax=ax)
    else:
      pitch.arrows(dfx['X1'][i], dfx['Y1'][i], dfx['X2'][i], dfx['Y2'][i], alpha=0.75,
                   width=2, headwidth=5, headlength=5, color='#ff0004', ax=ax)

  ax.vlines(66.7, 0, 100, ls='--', lw=1.5, color='#346594')
  ax.text(0, -7, player, ha='left', fontproperties=bold, color='#000000', size='28', va='center')
  ax.text(0, -3.5, 'Passes to Final Third', ha='left', fontproperties=reg, color='#000000', size='20', va='center')

  return fig

def chance_plot(data, player):
  dfx = data.copy()

  fig, ax = plt.subplots(figsize=(20, 20), dpi=500)
  fig.patch.set_facecolor('#FFFFFF')
  ax.set_facecolor('#FFFFFF')
  pitch = Pitch(pitch_type='wyscout', pitch_color='#FFFFFF', line_color='#346594',
                corner_arcs=True, goal_type='circle', linewidth=1.5, pad_bottom=5)
  pitch.draw(ax=ax)

  dfx = dfx[dfx['Act Name']==player].reset_index(drop=True)
  for i in range(len(dfx)):
    if dfx['Action'][i] == 'key pass':
      pitch.arrows(dfx['X1'][i], dfx['Y1'][i], dfx['X2'][i], dfx['Y2'][i], alpha=0.75,
                   width=2, headwidth=5, headlength=5, color='#346594', ax=ax)
    else:
      pitch.arrows(dfx['X1'][i], dfx['Y1'][i], dfx['X2'][i], dfx['Y2'][i], alpha=0.75,
                   width=2, headwidth=5, headlength=5, color='#ff0004', ax=ax)

  ax.annotate('-Key Pass->', size=16, xy=(5, 90), xytext=(0,0),
              textcoords='offset points', color='#346594', ha='left',
              zorder=9, va='center', fontproperties=reg)

  ax.annotate('-Assist->', size=16, xy=(5, 93), xytext=(0,0),
              textcoords='offset points', color='#ff0004', ha='left',
              zorder=9, va='center', fontproperties=reg)

  ax.text(0, -7, player, ha='left', fontproperties=bold, color='#000000', size='28', va='center')
  ax.text(0, -3.5, 'Chances Created', ha='left', fontproperties=reg, color='#000000', size='20', va='center')

  return fig

def goal_plot(data):
  data = data.copy()

  fig, ax = plt.subplots(figsize=(20,10))
  fig.patch.set_facecolor('#ffffff')
  ax.set_facecolor('#ffffff')
  ax.grid(axis='y', alpha=0.25, zorder=-10)
  temp = data['Gameweek'].to_list()

  bar = ax.bar(data['Gameweek'], data['Goals'], color='#346594', width=0.4, hatch='', zorder=10)

  for bar in bar.patches:
    ax.annotate(bar.get_height(), (bar.get_x() + bar.get_width()/2, bar.get_height()+.5), ha='center', va='center',
                size=20, xytext=(0, 8), fontproperties=bold, textcoords='offset points',color='#000000')
  
  ax.set_ylim([0, 40])
  ax.set_xticks(data['Gameweek'], temp)
  ax.set_yticks([0, 10, 20, 30, 40])

  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_color('#346594')
  ax.spines['bottom'].set_color('#346594')

  for t in ax.xaxis.get_ticklines():
    t.set_color('#346594')
  for t in ax.yaxis.get_ticklines():
    t.set_color('#346594')

  ax.tick_params(axis='x', colors='#346594')
  ax.tick_params(axis='y', colors='#346594')

  ax.set_ylabel('Goals scored', color='#346594', fontproperties=bold, size=16)
  ax.set_xlabel('Gameweeks', color='#346594', fontproperties=bold, size=16)

  for tick in ax.get_xticklabels():
    tick.set_fontproperties(bold)
    tick.set_size(20)
  for tick in ax.get_yticklabels():
    tick.set_fontproperties(bold)
    tick.set_size(20)

  return fig
