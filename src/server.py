from flask import Flask, render_template, request, make_response, jsonify
from weather import get_current_weather
from waitress import serve
from werkzeug.middleware.proxy_fix import ProxyFix
from loggingmiddleware import LoggingMiddleware

app = Flask(__name__)
app.wsgi_app = LoggingMiddleware(ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_prefix=1))


@app.route('/')
@app.route('/index')
def index():
    print(request.head)
    return render_template('index.html')

@app.route('/health')
def get_health():
    print("HEALTH check")
    data = {'status': 'OK'}
    return make_response(jsonify(data), 200)
    
@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if not bool(city.strip()):
        print("Empty city")
        city = "Dresden"

    weather_data = get_current_weather(city)
    print(weather_data)
    if not weather_data['cod']  == 200:
        return render_template('city-not-found.html')

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    # serve(app, host="0.0.0.0", port=8000)



