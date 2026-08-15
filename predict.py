import pandas as pd
import joblib
import argparse

def predict_water_requirement(temperature, humidity, crop_label):
    # Load the trained model pipeline
    try:
        model = joblib.load('crop_water_model.pkl')
    except FileNotFoundError:
        print("Error: Model file 'crop_water_model.pkl' not found. Please run 'train_model.py' first.")
        return

    # Create a DataFrame for the input
    input_data = pd.DataFrame({
        'temperature': [temperature],
        'humidity': [humidity],
        'label': [crop_label]
    })

    # Predict
    predicted_rainfall = model.predict(input_data)[0]

    print("\n--- Crop Water Requirement Prediction ---")
    print(f"Crop: {crop_label.capitalize()}")
    print(f"Environmental Conditions -> Temp: {temperature}°C, Humidity: {humidity}%")
    print(f"\n=> Predicted Water Required (Rainfall Equivalent): {predicted_rainfall:.2f} mm")
    print("-----------------------------------------")
    
    return predicted_rainfall

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict crop water requirement.")
    parser.add_argument('--temperature', type=float, default=30.5, help="Temperature in Celsius (Default: 30.5)")
    parser.add_argument('--humidity', type=float, default=60.0, help="Humidity percentage (Default: 60.0)")
    parser.add_argument('--crop', type=str, default='coffee', help="Crop name e.g., rice, maize, chickpea (Default: rice)")
    
    args = parser.parse_args()
    
    predict_water_requirement(args.temperature, args.humidity, args.crop)
