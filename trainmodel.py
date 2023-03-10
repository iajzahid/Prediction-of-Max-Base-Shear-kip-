# Import necessary libraries
from sklearn.model_selection import train_test_split
import xgboost as xgb
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np

# Load the dataset from an Excel sheet
df = pd.read_csv('traindscivil.csv')

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13']], df['target'], test_size=0.25)

# Train an XGBoost model on the training data
model = xgb.XGBRegressor()
model.fit(X_train, y_train)

# Test the model on the testing data
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy}")

### build GUI and use the trained model above
def predict(model):
    input_data = []
    for i in range(len(columns)):
        if data[columns[i]].dtype == 'int64':
            input_value = input_entries[i].get()
            if input_value.strip() == '':
                input_data.append(0)
            else:
                input_data.append(int(input_value))
        elif data[columns[i]].dtype == 'float64':
            input_value = input_entries[i].get()
            if input_value.strip() == '':
                input_data.append(0.0)
            else:
                input_data.append(float(input_value))
        else:
            input_data.append(input_entries[i].get())
    # Convert input_data to a 2D array
    input_array = np.array([input_data])
    predictions = model.predict(input_array)
    print(input_data)
    print(sum(input_data))
    c = "Max Base Shear (kip) Prediction using XGboost Trained Model is:  \n \n \n " + str(predictions)
    messagebox.showinfo("Prediction", c)


app = tk.Tk()
app.title("Prediction GUI")
data = pd.read_csv("Allconf - Copy.csv")
columns = data.columns.tolist()
nominal_columns = ["Boundary condition 1=fixed, 0=pin", "# of Bays", "Configuration"]
nominal_values = {}
for col in nominal_columns:
    nominal_values[col] = data[col].unique().tolist()

input_entries = []

# create input widgets for each column
for i in range(len(columns)):
    tk.Label(text=f"{columns[i]} :").grid(row=i, column=0)
    ##
    if columns[i] in nominal_columns:
        var = tk.StringVar(value=nominal_values[columns[i]][0])
        option_menu = tk.OptionMenu(app, var, *nominal_values[columns[i]])
        option_menu.grid(row=i, column=1)
        input_entries.append(var)
    else:
        input_entries.append(tk.Entry())
        input_entries[i].grid(row=i, column=1)
    ##

# create predict button
predict_button = tk.Button(text="Predict", command=lambda: predict(model))
predict_button.grid(row=len(columns)+1, column=1)

app.mainloop()

