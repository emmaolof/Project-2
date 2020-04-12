import requests
import json
import prettytable
import xlwt
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template


def get_bls_data(series, start, end):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"seriesid": series,"startyear":"%d" % (start), "endyear":"%d" % (end)})
    p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)

    try:
        df = pd.DataFrame()
        for series in json_data['Results']['series']:
            df_initial = pd.DataFrame(series)
            series_col = df_initial['seriesID'][0]
            for i in range(0, len(df_initial) - 1):
                df_row = pd.DataFrame(df_initial['data'][i])
                df_row['seriesID'] = series_col
                if 'code' not in str(df_row['footnotes']): 
                    df_row['footnotes'] = ''
                else:
                    df_row['footnotes'] = str(df_row['footnotes']).split("'code': '",1)[1][:1]
                df = df.append(df_row, ignore_index=True)
        return df
    except:
        json_data['status'] == 'REQUEST_NOT_PROCESSED'
        print('BLS API has given the following Response:', json_data['status'])
        print('Reason:', json_data['message'])

start = 2008
end = 2018
series = ['LAUCN180110000000003','LAUCN180110000000004','LAUCN180110000000005','LAUCN180110000000006']

#df = get_bls_data(series=series, start=start, end=end)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/Allen.html")
def Allen():
    return render_template("Allen.html")

@app.route("/Boone.html")
def Boone():
    return render_template("Boone.html")

@app.route("/Decatur.html")
def Decatur():
    return render_template("Decatur.html")

@app.route("/Hamilton.html")
def Hamilton():
    return render_template("Hamilton.html")

@app.route("/Hendricks.html")
def Hendricks():
    return render_template("Hendricks.html")

@app.route("/Johnson.html")
def Johnson():
    return render_template("Johnson.html")

@app.route("/Lake.html")
def Lake():
    return render_template("Lake.html")

@app.route("/Marion.html")
def Marion():
    return render_template("Marion.html")   

@app.route("/Monroe.html")
def Monroe():
    return render_template("Monroe.html")

@app.route("/StJoseph.html")
def StJoseph():
    return render_template("StJoseph.html")

@app.route("/vanderburgh.html")
def vanderburgh():
    return render_template("vanderburgh.html")

@app.route("/Warrick.html")
def Warrick():
    return render_template("Warrick.html")

@app.route("/countynames")
def names():
    """Return a list of sample names."""
    data  = {"County": "1"},{"County": "2"},{"County": "3"}
    sampleNames = jsonify(data)
    # Return a list of the county  names (sample names)
    return sampleNames

if __name__ == '__main__':
    app.run()