import datetime
import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

AUTHOR = "Wiktor Luksik" 
PORT = 8080

print(f"Data uruchomienia: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Autor: {AUTHOR}")
print(f"Port TCP: {PORT}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Pogoda</title><meta charset="utf-8"></head>
<body style="font-family: Arial; text-align: center; padding: 50px;">
    <h2>Wybierz lokalizację:</h2>
    <form action="/" method="get">
        <select name="city">
            <option value="Lublin">Lublin, Polska</option>
            <option value="Warszawa">Warszawa, Polska</option>
            <option value="Londyn">Londyn, UK</option>
            <option value="Berlin">Berlin, Niemcy</option>
        </select>
        <button type="submit">Sprawdź pogodę</button>
    </form>
    {% if weather %}
        <div style="margin-top: 30px; border: 1px solid #ccc; padding: 20px; display: inline-block;">
            <h3>Aktualna pogoda:</h3>
            <p style="font-size: 24px;">{{ weather }}</p>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    city = request.args.get('city')
    weather_info = None
    if city:
        try:
            response = requests.get(f"http://wttr.in/{city}?format=3")
            if response.status_code == 200:
                weather_info = response.text
            else:
                weather_info = "Błąd pobierania danych."
        except Exception as e:
            weather_info = f"Błąd połączenia: {e}"
    
    return render_template_string(HTML_TEMPLATE, weather=weather_info)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)