from flask import Flask, render_template


input_string ="Have a good day!"
app = Flask(__name__)

@app.route('/')
def html():
    return render_template('flight.html',input_str = input_string)


app.run(debug=True)