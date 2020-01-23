from flask import Flask, render_template, request
from datetime import datetime
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
    conn = sqlite3.connect('data')
    c = conn.cursor()
    c.execute('insert into run values (current_date, \"%s\")' % miles)
    conn.commit()


if __name__ == '__main__':
    app.run(debug=True)
