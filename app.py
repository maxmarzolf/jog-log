import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, render_template, request
from bokeh.plotting import figure, output_file, show


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def miles_ran():
    if request.method == 'GET':
        return render_template('main.html')
    elif request.method == 'POST':
        miles = request.form['mile_input']
        insert_into_table(miles)
        return render_template('main.html')


def insert_into_table(miles):
    connection = sqlite3.connect('data')
    cursor = connection.cursor()
    cursor.execute('insert into run (miles_ran) values (\"%s\")' % miles)
    connection.commit()
    cursor.close()
    connection.close()


def show_graph():
    engine = create_engine('sqlite:///data')
    dataframe = pd.read_sql('select * from run', engine)
    x_axis = dataframe['Day'].tolist()
    y_axis = dataframe['Miles_Ran'].tolist()
    output_file("templates/graph.html")
    p = figure(title="Miles Ran", x_axis_label='day', y_axis_label='miles', height=375, width=1200)
    p.line(x_axis, y_axis, legend_label="Miles per Day", line_width=2)
    show(p)


@app.route("/graph.html", methods=['POST'])
def move_forward():
    show_graph()
    return render_template('graph.html')


if __name__ == '__main__':
    app.run(debug=True)
