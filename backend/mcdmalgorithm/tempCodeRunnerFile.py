

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

def topsis_from_model(model_queryset):
  """
  Performs TOPSIS on data from a Django model queryset.

  Args:
    model_queryset: A Django queryset of Preferences instances.

  Returns:
    Pandas Series containing the TOPSIS scores.
  """

  # Convert queryset to DataFrame
  data = pd.DataFrame(model_queryset.values())

  # Data preprocessing
  # Handle missing values (replace with appropriate strategy)
  data.fillna(0, inplace=True)  # Replace with your preferred method

  # Normalize numeric columns
  numeric_cols = ['preferred_price_min', 'preferred_price_max']
  scaler = MinMaxScaler()
  data[numeric_cols] = scaler.fit_transform(data[numeric_cols])

  # Encode categorical columns
  categorical_cols = ['preferred_month', 'preferred_places', 'preferred_types', 'preferred_difficulity']
  encoder = LabelEncoder()
  for col in categorical_cols:
      data[col] = encoder.fit_transform(data[col])

  # Create decision matrix
  decision_matrix = data[['preferred_price_min', 'preferred_price_max', 'preferred_month', 'preferred_places', 'preferred_types', 'preferred_difficulity']]

  # Assign weights to criteria
  weights = [1/6] * 6  # Equal weights

  # Apply TOPSIS function
  topsis_scores = topsis(decision_matrix, weights)

  return topsis_scores

def topsis(data, weights):
  """
  Performs TOPSIS on the given data with specified weights.

  Args:
    data: Pandas DataFrame containing the decision matrix.
    weights: List of weights for each criterion.

  Returns:
    Pandas Series containing the TOPSIS scores.
  """

  # Calculate weighted normalized decision matrix
  weighted_data = data * weights

  # Determine ideal and negative ideal solutions
  ideal_solution = np.max(weighted_data, axis=0)
  negative_ideal_solution = np.min(weighted_data, axis=0)

  # Calculate Euclidean distance from ideal and negative ideal solutions
  distance_positive = np.sqrt(np.sum((weighted_data - ideal_solution)**2, axis=1))
  distance_negative = np.sqrt(np.sum((weighted_data - negative_ideal_solution)**2, axis=1))

  # Calculate TOPSIS score
  topsis_score = distance_negative / (distance_positive + distance_negative)

  return pd.Series(topsis_score, index=data.index)

# Example usage:
queryset = Dataset.objects.all()  # Replace with your desired query
topsis_results = topsis_from_model(queryset)
print(topsis_results)