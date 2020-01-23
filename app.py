from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def miles_ran():
    print(request.method)
    if request.method == 'GET':
        return render_template('test.html')
    elif request.method == 'POST':
        miles = request.form['mile_input']
        return "miles are {}".format(miles)
    else:
        return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)
