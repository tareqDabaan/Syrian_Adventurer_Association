# pricing/utils.py
from activities.models import Activity
import joblib  # if using scikit-learn for model serialization
# import torch  # if using PyTorch models

# Define a function to load your trained AI model
def load_model():
    # Example: Load scikit-learn model
    model_path = '/path/to/your/trained/model.pkl'
    model = joblib.load(model_path)
    return model

# Function to preprocess input data and make predictions
def get_dynamic_price(activity_id):
    try:
        # Load your AI model
        model = load_model()

        # Fetch activity details from database (assuming Activity model exists)
        activity = Activity.objects.get(id=activity_id)

        # Example: Prepare input features (adjust according to your model requirements)
        features = [
            activity.activity_type.id,  # Example: categorical feature
            activity.start_at.timestamp(),  # Example: numerical feature
            activity.max_participants  # Example: numerical feature
        ]

        # Reshape features as needed by your model
        input_data = [features]  # Example: convert to numpy array or torch tensor if using PyTorch

        # Perform prediction
        predicted_price = model.predict(input_data)

        # Return predicted price (adjust this based on your model output)
        return float(predicted_price)  # Example: convert to float if necessary

    except Exception as e:
        # Handle exceptions (e.g., model loading failure, database errors)
        print(f"Error predicting price: {str(e)}")
        return None
