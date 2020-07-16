from flask import *
import pandas as pd
import os
import re
import knapsack_code
import json

"""
# Nicolas Navarrete - 19697438
# Diseno y analisis de algoritmos
"""

app = Flask(__name__)

filename='portfolio.xlsx'
data = [pd.read_excel(filename,sheet_name=i,header=1) for i in range(5)]

@app.route("/")
def show_tables():
    df = data[0].fillna('')
    weights=df.columns[1:7].get_values()
    values=df.columns[7:14].get_values()
    return render_template('index.html')


@app.route('/optimize', methods= ['POST'])
def optimize():
    period = int(request.form['period'])
    weight = int(request.form['weight'])
    value = int(request.form['value'])
    df = data[period].fillna('')
    df=df[[df.columns[weight],df.columns[value]]]
    weights = list(df.iloc[:,0])
    values = list(df.iloc[:,1])

    return render_template('optimize.html', weights=weights, values = values, tables=[re.sub(' mytable', '" id="example', df.to_html(classes='mytable'))],
    titles = ['Portfolio Optimization'])


@app.route('/calculate', methods=['POST'])
def calculate():
    l = request.get_data()
    data  = json.loads(l)
    values = data['values']
    weights = data['weights']
    max_weight = data['max']
    elements_g, knapsack_weight_g, knapsack_value_g = knapsack_code.greedy_knapsack_int(weights, values, max_weight)
    elements_dp, knapsack_weight_dp, knapsack_value_dp = knapsack_code.dp_knapsack_int(weights, values, max_weight)
    # json.dumps({'a':1,'b':2})
    return json.dumps({'r1':elements_g, 'r2': knapsack_weight_g, 'r3':knapsack_value_g,
                       'r4':elements_dp, 'r5':knapsack_weight_dp, 'r6':knapsack_value_dp})

if __name__ == "__main__":
    app.run(debug=True)
