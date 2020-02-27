#----------------------------------------------------------------------------#
# Imports

# Python modules
import os, logging
from matplotlib import pyplot
import datetime as dt
import pandas as pd
import numpy as np
#rom plot_codes import dicharge_no
import plotly
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import  plot
# Flask modules
from flask               import Flask , render_template, request, url_for, redirect, send_from_directory
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
import pathlib
# App modules
#from app
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
#from forms import *
import os
app = Flask(__name__)

#----------------------------------------------------------------------------#
# App Config.
app.config.from_object('config')
#----------------------------------------------------------------------------#

# = Flask(__name__)


#create path
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

#Data function
def data_used():
    # Import data
    df = pd.read_csv(
        "C:\\Users\\lmumelo\\OneDrive - Kemri Wellcome Trust\\app\\flask-dashboard-adminator-master\\data\\fullredcap.csv", low_memory=False)
    return df

#####################################################################################
def create_df():
    # get counts per NAR type
    df_nar = pd.DataFrame(data_used().groupby('Hospital_id')['Document Source'].value_counts())
    df_nar = df_nar.rename({'Document Source': 'Doc count'}, axis='columns')
    df_nar = df_nar.reset_index()

    return df_nar



def create_plot(df_nar):
    # set up plotly figure
    fig = go.Figure()
    # Manage NAR types (who knows, there may be more types with time?)
    nars = df_nar['Document Source'].unique()
    nars = nars.tolist()
    nars.sort(reverse=False)
    # add one trace per NAR type and show counts per hospital
    data = []
    for nar in nars:
        # subset dataframe by NAR type
        df_ply = df_nar[df_nar['Document Source'] == nar]

        # add trace
        fig.add_trace(go.Bar(x=df_ply['Hospital_id'], y=df_ply['Doc count'], name='Document Type=' + str(nar)))

    # make the figure a bit more presentable
    fig.update_layout(title='Document Use per hospital',
                      yaxis=dict(title='<i>count of Docuement types</i>'),
                      xaxis=dict(title='<i>Hospital</i>'))

    graphe = plot(fig,config={"displayModeBar": False},
                  show_link=False, include_plotlyjs=False,
                  output_type='div')

    return graphe


@app.route('/')
def chart_out():

    bar = create_plot(create_df())
    return render_template('pages/charts.html', plot=bar)


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
