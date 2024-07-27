from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle

app = Flask(__name__)

# Load the model
with open('knn_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the scaler
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    
    parameters = ['sysBP', 'glucose', 'age', 'totChol', 'cigsPerDay', 'diaBP', 'prevalentHyp', 'diabetes', 'BPMeds', 'male']
    
    # Ensure all required parameters are present
    for param in parameters:
        if param not in data:
            return jsonify({"error": f"Missing parameter: {param}"}), 400
    
    # Create DataFrame from input data
    my_df = pd.DataFrame([data], columns=parameters)
    
    # Scale the input data
    my_df_scaled = pd.DataFrame(scaler.transform(my_df), columns=my_df.columns)
    
    # Make prediction
    my_y_pred = model.predict(my_df_scaled)
    
    # Return the result
    result = "The patient will develop a Heart Disease." if my_y_pred[0] == 1 else "The patient will not develop a Heart Disease."
    
    return jsonify({"prediction": result})

if __name__ == '__main__':
    app.run(debug=True)
