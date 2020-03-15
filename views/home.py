import flask
from flask import render_template, request
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show

blueprint = flask.Blueprint('home', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
def miles_ran():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        create_connection()
        graph()
        return render_template('home.html')


def create_connection():
    connection = sqlite3.connect('data')
    cursor = connection.cursor()
    miles = request.form['mile_input']
    insert_into_table(miles, cursor, connection)
    close_connection(cursor, connection)


def insert_into_table(miles, cursor, connection):
    cursor.execute('insert into run (miles_ran) values (\"%s\")' % miles)
    connection.commit()


def close_connection(cursor, connection):
    cursor.close()
    connection.close()


def graph():
    engine = create_engine('sqlite:///data')
    df = pd.read_sql('select * from run', engine)
    x_axis = df['Day'].tolist()
    y_axis = df['Miles_Ran'].tolist()
    df2 = df[1:]
    ColumnDataSource(df2)
    output_file("templates/graph.html")
    p = figure(title="Miles Ran", x_axis_label='day', y_axis_label='miles', height=225, width=950,
               toolbar_location='above')
    p.background_fill_color = '#f4f4f4'
    p.line(x_axis, y_axis, legend_label="Miles per Day", line_width=2, line_color="#000000")
    show(p)
