# train_model.py
"""

Numerical representations are typically more efficient in terms of storage and computation compared to string representations. 
This can lead to faster processing and less memory usage, especially when dealing with large datasets
"""


"""
Naive bayes::
Consider the MultinomialNB classifier used in the code. 
This algorithm works by computing probabilities and making decisions based on numerical values

Training: During training, the algorithm needs to compute the likelihood of a message being spam or not spam based on the features (words in the message). 
It calculates probabilities for each class (spam or not spam). Prediction: During prediction, it uses these probabilities to assign a class to new messages. This process relies on numerical computations, which are facilitated by numeric labels.
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import zipfile
import requests
import io

# Download the dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
response = requests.get(url)
zip_file = zipfile.ZipFile(io.BytesIO(response.content))
zip_file.extractall()

# Load the dataset
df = pd.read_csv("SMSSpamCollection", sep='\t', header=None, names=['label', 'message'])

# Preprocess the dataset
# Mapping Labels: Converts the 'label' column from categorical labels ('ham' and 'spam') to numerical labels (0 for 'ham' and 1 for 'spam').
# Features and Labels: Sets X to the messages and y to the labels
df['label'] = df['label'].map({'ham': 0, 'spam': 1})
X = df['message']
y = df['label']

# Split the dataset into training and testing sets
#30% of the data is used for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Vectorize the text data
# CountVectorizer: Converts text data into a matrix of token counts.
# fit_transform(X_train): Learns the vocabulary from the training data and transforms it into a numerical format.
# transform(X_test): Transforms the test data into the same numerical format using the learned vocabulary
vectorizer = CountVectorizer()
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)


# Train the model
#MultinomialNB: Initializes the Naive Bayes classifier.
model = MultinomialNB()
model.fit(X_train_vect, y_train)


# Test the model
y_pred = model.predict(X_test_vect)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save the vectorizer and model
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('spam_model.pkl', 'wb') as f:
    pickle.dump(model, f)
