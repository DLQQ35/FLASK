from flask import Flask, render_template, request
import json
import urlib.parse
import urlib.request

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def details():
    if request.method == 'GET':
        return render_template('index.html')
    
    location = request.form['location', ''].strip()
    if not location:
        return render_template('index.html', error = 'Please give correct location')
    
    try:
        q = urlib.parse.quote(location)

        url =  f"https://photon.komoot.io/api/?q={q}&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "FlaskGeocoder/1.0"})

        source = urllib.request.urlopen(req).read()
        responseData = json.loads(source)

        features = responseData.get('features', [])
        if not features:
            return render_template('index.html', error = 'Please give correct location')
        
        lon, lat = features[0]['geometry']['coordinates']

        data = {
            'latitude': str(lat),
            'longitude': str(lon)
        }

        return render_template('index.html', data = data)
    
    except Exception:
        return render_template('index.html', error = 'Please give correct location')
    
if __name__ == '__main__':
    app.run(host=0.0.0.0, port=8800, debug = True)