# import pandas as pd
# from sklearn.linear_model import LinearRegression
# from .models import HistoricalPricingData

# class DynamicPricingModel:
#     def __init__(self):
#         self.model = LinearRegression()

#     def train_model(self):
#         # Fetch historical pricing data from the database
#         data = HistoricalPricingData.objects.all()
#         df = pd.DataFrame(list(data.values('participants', 'price')))
        
#         if df.empty:
#             return None
        
#         # Train the model
#         self.model.fit(df[['participants']], df['price'])

#     def predict_price(self, participants):
#         # Check if the model is fitted, if not, train it
#         if not hasattr(self.model, 'coef_'):
#             self.train_model()

#         # Predict price based on the number of participants
#         predicted_price = self.model.predict([[participants]])
#         return predicted_price[0]
