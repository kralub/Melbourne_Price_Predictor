#!/usr/bin/env python
# Caleb Bayles
# March 19, 2021
# Computer Science Capstone

# -- Libraries
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# -- Regression runner:
# This is a function to run the regression, it returns the Random Tree Regression model that is used to predict cost.
def run_regressor():
    print('REGRESSION STARTING...')

    # -- data import:
    data_path = 'data/melb_data.csv'
    realty_data = pd.read_csv(data_path)
    # drop null values
    realty_data = realty_data.dropna(axis=0)
    # get dummy values
    #  converting columns to dummies
    type_dummy = pd.get_dummies(realty_data.Type, columns=['Type'], prefix='type')
    # assigning new dummy values
    realty_data = pd.concat([realty_data, type_dummy], axis=1)
    # remove outliers
    #  now to remove them, anything over 3 standard deviations is considered an outlier
    realty_data = realty_data[realty_data['Price'] < realty_data['Price'].std() * 3]

    # -- Select target prediction value:
    y = realty_data.Price
    # features:
    realty_data_features = ['Rooms', 'Distance', 'BuildingArea',
                            'Bedroom2', 'Landsize',
                            'Lattitude', 'Longtitude', 'type_h',
                            'type_t', 'type_u']
    X = realty_data[realty_data_features]

    # -- Train model:
    #  define model
    realty_price_model = RandomForestRegressor()
    #  fit model
    realty_price_model.fit(X, y)
    print('REGRESSION FINISHED, RETURNING MODEL TO APPLICATION...')
    # return model for prediction based on input
    return realty_price_model


# Makes the regression model at the start of the program to avoid errors and repetitive creation.
prediction_model = run_regressor()


# -- Functions for inserting values into predictor.
#  Gets string value from radio box and returns the binary number list for the prediction function so that it can be
#  inputted into the predictor.
def get_house_type(bedroom_string):
    # print('GETTING HOUSE BINARY TYPE...')
    # binary_house_type = [0, 0, 0]
    if bedroom_string == 'House':
        return [1, 0, 0]
    if bedroom_string == 'Townhouse':
        return [0, 1, 0]
    if bedroom_string == 'Unit':
        return [0, 0, 1]


# This is where the values are fed into the model to return a prediction that is a string format.
def predict_cost(num_rooms, distance_to_cbd, building_area_meters, num_bedrooms, land_size, latitude,
                 longitude, house_type_string):
    # print('STARTING PREDICTION')
    # This inserts the binary house type values based on what house type it is.
    binary_house_type = get_house_type(house_type_string)
    house_1 = binary_house_type[0]
    house_2 = binary_house_type[1]
    house_3 = binary_house_type[2]
    # This will make the array based on the input values to be fed into the prediction model.
    predict_values = np.array(
        [[num_rooms, distance_to_cbd, building_area_meters, num_bedrooms, land_size, latitude, longitude,
          house_1, house_2, house_3]])
    # Prediction is returned into the prediction variable.
    prediction = prediction_model.predict(predict_values)
    # It is then converted to a string value.
    prediction = np.array2string(prediction)
    # Then we strip the period and brackets.
    prediction_stripped = prediction.strip('[].')
    # Then we will format it with commas and a dollar sign for readability.
    prediction_stripped = '$' + ("{:,}".format(float(prediction_stripped)))
    # Return the prediction string for the monetary value of the house.
    return str(prediction_stripped)


# This function is called when the predict button is pressed on the interface.
def handle_predict_button():
    # Now we will try to send values to prediction.
    # The values from inputs will be tested first to see if it can inputted into the predictor with the right values
    #   with the right range. If it isn't in the right range or value it will give an error message
    #   and end this function.
    try:
        num_rooms = num_rooms_input.get()
        distance = float(distance_input.get())
        if distance < 0 or distance > 48:
            tk.messagebox.showerror(title="Distance error:", message="Distance to Melbourne City must "
                                                                     "be within 0 to 48 miles.")
            return
        building_area = float(building_area_input.get())
        if building_area < 5 or building_area > 1600:
            tk.messagebox.showinfo("Building area error:", "Building area must be within 5 to 1,600 square meters.")
            return
        num_bedrooms = num_bedrooms_input.get()
        land_size = float(land_size_input.get())
        if land_size < 5 or land_size > 40000:
            tk.messagebox.showinfo("Land area error:", "Land area must be within 5 to 40,000 square meters.")
            return
        latitude = float(latitude_input.get())
        if latitude < -39 or latitude > -37:
            tk.messagebox.showinfo("Latitude error:", "Latitude must be within -39 to -37 for Melbourne.")
            return
        longitude = float(longitude_input.get())
        if longitude < 144 or longitude > 146:
            tk.messagebox.showinfo("Longitude error:", "Longitude must be within 144 to 146 for Melbourne.")
            return
        house_type = house_type_input.get()
        # Now that all the values have passed the test it is fed into the model using our function from earlier.
        the_prediction = predict_cost(num_rooms, distance,
                                      building_area, num_bedrooms,
                                      land_size, latitude,
                                      longitude, house_type)
        # Now display the cost of the house to the user.
        tk.messagebox.showinfo("This house cost is: ", ("This house is worth: " + the_prediction))
    except Exception as x:
        tk.messagebox.showinfo("Input error:", "There has been an error with your input.")
        return


# -- This is where the User Interface starts.
root = tk.Tk()
root.geometry("490x900")
root.title("Melbourne Housing Cost Predictor")

# Welcome and about labels.

welcome_label = tk.Label(root, text="\nWelcome!", font=("Futura", 25, 'bold')).grid(row=0)


about_label = tk.Label(root, text="Please enter the values respectively to use a \n"
                                  "machine learning algorithm to predict the\n"
                                  "cost of a house with extremely accuracy. \n "
                                  "This prediction works by feeding in vast amounts of \n"
                                  "Melbourne housing data into a Random Tree Regression \n"
                                  "algorithm to create a prediction model.\n\n"
                                  
                                  "Warning: Use light mode, not dark mode, for this app to work\n or the buttons will "
                                  "not show text! \n\n"
                       ).grid(row=1, column=0)

# Input labels are here.
input_width = 10

num_rooms_label = tk.Label(root, text="Number of rooms: ").grid(row=2)
num_rooms_input = ttk.Combobox(root, state="readonly", values=['1', '2', '3', '4', '5', '6', '7', '8', '9'], width=input_width)
num_rooms_input.current(0)
num_rooms_input.grid(row=3)

distance_label = tk.Label(root, text="\nDistance to Melbourne City (0m to 48m): ").grid(row=4)
distance_input = tk.Entry(root, width=input_width)
distance_input.grid(row=5)

building_area_label = tk.Label(root, text="\nBuilding area in square meters (5 m^2 to 1,600 m^2): ").grid(row=6)
building_area_input = tk.Entry(root, width=input_width)
building_area_input.grid(row=7)

num_bedrooms_label = tk.Label(root, text="\nNumber of Bedrooms: ").grid(row=8)

num_bedrooms_input = ttk.Combobox(root, state="readonly", values=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                                  width=input_width)
num_bedrooms_input.current(0)
num_bedrooms_input.grid(row=9)

land_size_label = tk.Label(root, text="\nLand Size in square meters (5 m^2 to 40,000 m^2): ").grid(row=10)
land_size_input = tk.Entry(root, width=input_width)
land_size_input.grid(row=11)

latitude_label = tk.Label(root, text="\nLatitude (a value between -37 and -39): ").grid(row=12)
latitude_input = tk.Entry(root, width=input_width)
latitude_input.grid(row=13)

longitude_label = tk.Label(root, text="\nLongitude (a value between 144 and 146): ").grid(row=14)
longitude_input = tk.Entry(root, width=input_width)
longitude_input.grid(row=15)

house_type_label = tk.Label(root, text="\nHouse type: ").grid(row=16)
house_type_input = ttk.Combobox(root, state="readonly", values=['House', 'Townhouse', 'Unit'], width=(input_width + 5))
house_type_input.current(0)
house_type_input.grid(row=17)

this_whitespace = tk.Label(root, text="\n").grid(row=18)
predict_button = tk.Button(root, text="Predict", width=25, foreground='black', command=handle_predict_button).grid(
    row=19)
this_whitespace_2 = tk.Label(root, text="\n").grid(row=20)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.mainloop()
