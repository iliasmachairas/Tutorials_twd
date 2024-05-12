from flask import Flask, render_template, request, redirect, url_for
from twilio.rest import Client

# Your Twilio Account SID and Auth Token
account_sid = 'xxxxxxxxxxxxxxxxxx'
auth_token = 'xxxxxxxxxxxxxxxxxxx'

# Initialize Twilio client
client = Client(account_sid, auth_token)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    date = request.form['date']
    location = request.form['location']
    return redirect(url_for('result', name=name, date=date, location=location))

@app.route('/result')
def result():
    name = request.args.get('name')
    date = request.args.get('date')
    location = request.args.get('location')
    message = client.messages.create(
        body='Details of appointment. Name: '+name+ ', date: '+date+ ' ,location: '+location,
        from_='+xxxxxxxxx',
        to='+xxxxxxxxxxxx'
    )
    print("Message sent successfully. SID:", message.sid)
    return render_template('result.html', name=name, date=date, location=location)

if __name__ == '__main__':
    app.run(debug=True)
