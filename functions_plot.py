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
