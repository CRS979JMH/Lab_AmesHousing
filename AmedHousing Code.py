import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import openpyxl

# Load the data
def load_data():
    df = pd.read_excel('AmesHousing.xlsx')
    return df

df = load_data()

# Selecting features and target
features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath', 'YearBuilt']
target = 'SalePrice'
X = df[features]
y = df[target]

# Handle missing values
X = X.fillna(X.median())

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Multiple Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)

# Create the Streamlit web-based app
st.title('Ames Housing Price Prediction')

# Sidebar for user inputs
st.sidebar.header('Input Parameters')

def user_input_features():
    OverallQual = st.sidebar.slider('Overall Quality', 1, 10, 5)
    GrLivArea = st.sidebar.number_input('Above Ground Living Area (sq ft)', min_value=500, max_value=5000, value=1500)
    GarageCars = st.sidebar.slider('Garage Cars', 0, 4, 2)
    TotalBsmtSF = st.sidebar.number_input('Total Basement Area (sq ft)', min_value=0, max_value=3000, value=1000)
    FullBath = st.sidebar.slider('Number of Full Bathrooms', 1, 5, 2)
    YearBuilt = st.sidebar.number_input('Year Built', min_value=1800, max_value=2025, value=2000)
    
    data = {
        'OverallQual': OverallQual,
        'GrLivArea': GrLivArea,
        'GarageCars': GarageCars,
        'TotalBsmtSF': TotalBsmtSF,
        'FullBath': FullBath,
        'YearBuilt': YearBuilt
    }
    
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Display user inputs
st.subheader('User Input Parameters')
st.write(input_df)

# Predict housing price
prediction = model.predict(input_df)

# Display the prediction
st.subheader('Predicted Housing Price ($)')
st.write(f"${prediction[0]:,.2f}")
