import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, render_template, request
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def miles_ran():
    if request.method == 'GET':
        return render_template('main.html')
    elif request.method == 'POST':
        miles = request.form['mile_input']
        insert_into_table(miles)
        show_graph()
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


if __name__ == '__main__':
    app.run(debug=True)
