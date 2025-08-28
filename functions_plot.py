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

