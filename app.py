from flask import Flask, render_template, request, redirect, url_for
from predict import predict_water_requirement
from pump_time_converter import calculate_pump_time
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/farmer', methods=['GET', 'POST'])
def farmer():
    if request.method == 'POST':
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        crop = request.form['crop']
        length = float(request.form['length'])
        width = float(request.form['width'])
        flow_rate = float(request.form['flow_rate'])

        # Predict Rainfall
        rainfall_mm = predict_water_requirement(temperature, humidity, crop)

        # Calculate Pump Time
        area, volume_ml, run_time = calculate_pump_time(
            rainfall_mm=rainfall_mm, 
            length_cm=length, 
            width_cm=width, 
            flow_rate_ml_per_sec=flow_rate
        )

        result = {
            'rainfall': round(rainfall_mm, 2),
            'area': round(area, 4),
            'volume_ml': round(volume_ml, 2),
            'volume_l': round(volume_ml / 1000, 2),
            'run_time': round(run_time, 2)
        }
        return render_template('farmer.html', result=result)

    return render_template('farmer.html')

@app.route('/researcher')
def researcher():
    # Provide the list of image files to display
    images = [
        {'file': 'actual_vs_predicted_matrix.png', 'title': 'Actual vs. Predicted Matrix'},
        {'file': 'correlation_matrix.png', 'title': 'Feature Correlation Matrix'},
        {'file': 'residual_error_matrix.png', 'title': 'Residual Error Distribution'},
        {'file': 'model_comparison.png', 'title': 'IoT Sensor Trade-off Analysis'}
    ]
    return render_template('researcher.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
