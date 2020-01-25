from flask import Flask, render_template, request
from datetime import datetime
from bokeh.plotting import figure, output_file, show
import pandas as pd
from sqlalchemy import create_engine
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def miles_ran():
    if request.method == 'GET':
        return render_template('test.html')
    elif request.method == 'POST':
        miles = request.form['mile_input']
        insert_into_table(miles)
        return "miles are {}".format(miles)
    else:
        return render_template('test.html')


def insert_into_table(miles):
    current_date = datetime.now()
    connection = sqlite3.connect('C:\\Users\\bmbur\\dev\\jog-log\\data')
    cursor = connection.cursor()
    cursor.execute('insert into run values (\"%s\")' % miles)
    connection.commit()
    show_graph()


def show_graph():
    engine = create_engine('sqlite:///data')
    dataframe = pd.read_sql('select * from run', engine)
    x_axis = [1, 2, 3, 4, 5, 6, 7, 8]
    y_axis = dataframe.values.tolist()
    output_file("templates/graph.html")
    p = figure(title="Miles Ran", x_axis_label='day', y_axis_label='miles')
    p.line(x_axis, y_axis, legend_label="Miles per Day", line_width=2)
    show(p)

if __name__ == '__main__':
    app.run(debug=True)
