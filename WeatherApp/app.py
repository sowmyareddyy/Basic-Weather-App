from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY', 'd7cc2a3d0b940730cbe1843ad513f261')

def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return None

        weather_details = {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"].capitalize()
        }
        return weather_details

    except Exception as e:
        print(f"Weather fetch error: {str(e)}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather = fetch_weather(city)
            if weather:
                return render_template('index.html', weather=weather)
            else:
                return render_template('error.html')  # Redirect to error page if city is not found
        else:
            return render_template('error.html')  # Redirect to error page if input is empty

    return render_template('index.html', weather=None)

if __name__ == "__main__":
    app.run(debug=True)
