from flask import Flask, render_template, request
import random
import requests
from datetime import datetime

app = Flask(__name__)

message_list = [("Bot", "Write me some message ;)")]

def add_user_message(message):
    message_list.append(("You", message))

def add_bot_message(message):
    message_list.append(("Bot", message))

def create_bot_answer(message):
    message = message.lower()

    if any(s in message for s in ['hi', 'hello', 'good']):
        add_bot_message("Nice to see you!")
    elif 'how are you' in message:
        add_bot_message('I am a bot, so I am always fine :) And how are you doing?')
    elif 'fine' in message:
        add_bot_message('That`s great!')
    elif any(s in message for s in ['date', 'time']):
        add_bot_message(f'Current date and time is {get_current_time()}')
    elif 'weather' in message:
        add_bot_message(f'Current weather in Saint Petersburg is {get_weather()}')
    elif 'random' in message:
        add_bot_message(f'Here is your random number: {get_random_number()}')
    elif 'joke' in message:
        setup, delivery = tell_joke()
        add_bot_message(setup)
        add_bot_message('...')
        add_bot_message(delivery)
    elif any(s in message for s in ['bye', 'goodbye']):
        add_bot_message('Have a nice day! See you later.')
    else:
        add_bot_message("I don`t know, what to say about this :(")

def get_current_time():
    dt = datetime.today()
    return dt.ctime()

def get_weather():
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id=498817&appid=19eee7385e1f56ec982048604426b42c&units=metric')
    
    data = r.json()
    description = data['weather'][0]['description']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']

    return f'{description}, temperature: {temp}°C, feels like: {feels_like}°C, pressure: {pressure} hPa, humidity: {humidity} %'

def get_random_number():
    return random.randint(0,100)

def tell_joke():
    r = requests.get('https://v2.jokeapi.dev/joke/Programming,Miscellaneous,Pun?blacklistFlags=nsfw,racist,sexist,explicit&type=twopart')
    data = r.json()
    setup = data['setup']
    delivery = data['delivery']

    return (setup, delivery)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', messages=message_list)
    else:
        new_message = request.form.get("new_message")
        add_user_message(new_message)

        create_bot_answer(new_message)
        return render_template('index.html', messages=message_list)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)