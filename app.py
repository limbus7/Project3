from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Homepage.html')

@app.route('/bitcoin_details')
def bitcoin_details():
    return render_template('bitcoin_details.html')

@app.route('/bitcoin_both')
def bitcoin_both():
    return render_template('both.html')

if __name__ == "__main__":
    app.run(debug=True)



    
    