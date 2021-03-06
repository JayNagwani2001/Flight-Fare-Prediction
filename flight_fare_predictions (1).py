# -*- coding: utf-8 -*-
"""Flight Fare Predictions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vvtMS0ahAloJSqLAPc3o0mu5f0bo8RHT
"""

#Importing Required Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Importing train Dataset
train_data=pd.read_excel("/content/Data_Train.xlsx")

pd.set_option('display.max_columns',None)
train_data.head()

train_data.shape

train_data.nunique()

#For Cleaning data if values like nan,inf,-inf present
def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)

"""## **EDA**

###Lest take columns one by one

For 'date_of_Journey' column we need to convert it form object type to timestamps so that it can be used for prediction with to_datetime function

---



---


'.dt.day' only extract date and 
'.dt.month' only extract month


---
"""

train_data["Journey_day"]=pd.to_datetime(train_data.Date_of_Journey, format="%d/%m/%Y").dt.day
train_data["Journey_month"]=pd.to_datetime(train_data["Date_of_Journey"], format="%d/%m/%Y").dt.month

#Days and Months are taken so need of "Date_of_Journey" column
train_data.drop(["Date_of_Journey"],axis=1,inplace=True)

#Departure hours and mins are taken from "Dep_Time" column
train_data["Dep_hour"]=pd.to_datetime(train_data["Dep_Time"]).dt.hour
train_data["Dep_min"]=pd.to_datetime(train_data["Dep_Time"]).dt.minute
train_data.drop('Dep_Time', axis=1,inplace=True)

#Arrival hours and mins are taken from 'Arrival_Time' column
train_data["Arrival_hour"]=pd.to_datetime(train_data["Arrival_Time"]).dt.hour
train_data["Arrival_min"]=pd.to_datetime(train_data["Arrival_Time"]).dt.minute
train_data.drop('Arrival_Time', axis=1,inplace=True)

#for "Duration" column we need to convert it in hours and mins
duration=list(train_data["Duration"])
durationhr=[]
durationmin=[]

for time in duration:
  if(len(time.split()) !=2):
    if("h" in time):
      time= time + " 0m"
    else:
      time= "0h " + time
  durationhr.append(int(time.split(sep="h")[0]))
  durationmin.append(int(time.split(sep="m")[0].split(" ")[-1]))

train_data["Duration_hour"]=pd.DataFrame(durationhr);
train_data["Duration_min"]=pd.DataFrame(durationmin);

#Now no need of "Duration" column
train_data.drop("Duration", axis=1,inplace=True)

"""## **Encoding Categorical Variables**

---

Nominal data: There is no ordering in data, OneHotEncoding is used.

---



---


Ordinal data:There is ordering in data, Label encoding is used.
"""

#Airline
#There is no Ordering in data ie no one is more or less than other so
#One Hot Encoding

train_data["Airline"].value_counts()

#from the figure we can see "jet Airways" have price median much more than others.
#Others have almost same median.
#If there is a trend we will use LabelEncoding 
sns.catplot(y="Price",x="Airline", data=train_data.sort_values("Price",ascending=False),kind="boxen",height=6, aspect=3)
plt.show()

#Airline OneHotEncoding
Airline=pd.get_dummies(train_data["Airline"], drop_first=True)
Airline

#Source
#There is no Ordering in data ie no one is more or less than other so
#One Hot Encoding
train_data["Source"].value_counts()

#All have almost same median.
#If there is a trend we will use LabelEncoding 
sns.catplot(y="Price",x="Source", data=train_data.sort_values("Price",ascending=False),kind="boxen",height=6, aspect=3)
plt.show()

#Source OneHotEncoding
Source=pd.get_dummies(train_data["Source"], drop_first=True)
Source

#Destination
#There is no Ordering in data ie no one is more or less than other so
#One Hot Encoding
train_data["Destination"].value_counts()

#All have almost same median.
#If there is a trend we will use LabelEncoding 
sns.catplot(y="Price",x="Destination", data=train_data.sort_values("Price",ascending=False),kind="boxen",height=6, aspect=3)
plt.show()

#Destination OneHotEncoding
Destination=pd.get_dummies(train_data["Destination"], drop_first=True)
Destination

#joining dummies of "Destination", "Source", "Airline" with train_data.
train_data=pd.concat([train_data,Destination, Source,Airline],axis=1)

# Removing "Airline", "Source", "Destination" columns.
train_data.drop(["Airline", "Source", "Destination"],axis=1,inplace=True)

""""Additional_Info" column conatin almost 80% 'no_info' so we can remove it

---
"Route" and "Total_Stops" are very related to each other so we can remove one of them.


"""

train_data.drop(["Additional_Info","Route"],axis=1,inplace=True)

train_data["Total_Stops"].value_counts()

#"Total_stops" is Ordinal Data because lesser the stops lower the price will be and vice versa
#Label ENCODING 

train_data.replace({"1 stop": 1,"non-stop": 0,"2 stops": 2,"3 stops": 3,"4 stops": 4}, inplace=True)

#Cleaning train_data
train_data=clean_dataset(train_data)

"""## **Test Data**"""

#To avoid data leakage we will do preprocessing of test data separetly.

test_data=pd.read_excel("Test_set.xlsx")
test_data.head()

#Preprocessing

test_data["Journey_day"]=pd.to_datetime(test_data["Date_of_Journey"], format="%d/%m/%Y").dt.day
test_data["Journey_month"]=pd.to_datetime(test_data["Date_of_Journey"], format="%d/%m/%Y").dt.month
test_data.drop(["Date_of_Journey"],axis=1,inplace=True)

#Departure hours and mins are taken
test_data["Dep_hour"]=pd.to_datetime(test_data["Dep_Time"]).dt.hour
test_data["Dep_min"]=pd.to_datetime(test_data["Dep_Time"]).dt.minute
test_data.drop('Dep_Time', axis=1,inplace=True)

#Arrival hours and mins are taken
test_data["Arrival_hour"]=pd.to_datetime(test_data["Arrival_Time"]).dt.hour
test_data["Arrival_min"]=pd.to_datetime(test_data["Arrival_Time"]).dt.minute
test_data.drop('Arrival_Time', axis=1,inplace=True)

#for Duration column we need to convert it in hours and mins
duration=list(test_data["Duration"])
durationhr=[]
durationmin=[]

for time in duration:
  if(len(time.split()) !=2):
    if("h" in time):
      time= time + " 0m"
    else:
      time= "0h " + time
  durationhr.append(int(time.split(sep="h")[0]))
  durationmin.append(int(time.split(sep="m")[0].split(" ")[-1]))
test_data["Duration_hour"]=pd.DataFrame(durationhr);
test_data["Duration_min"]=pd.DataFrame(durationmin);
test_data.drop("Duration", axis=1,inplace=True)

# Categorical data

print("Airline")
print("-"*75)
print(test_data["Airline"].value_counts())
Airline = pd.get_dummies(test_data["Airline"], drop_first= True)

print()

print("Source")
print("-"*75)
print(test_data["Source"].value_counts())
Source = pd.get_dummies(test_data["Source"], drop_first= True)

print()

print("Destination")
print("-"*75)
print(test_data["Destination"].value_counts())
Destination = pd.get_dummies(test_data["Destination"], drop_first = True)

# Additional_Info contains almost 80% no_info
# Route and Total_Stops are related to each other
test_data.drop(["Route", "Additional_Info"], axis = 1, inplace = True)

# Replacing Total_Stops
test_data.replace({"non-stop": 0, "1 stop": 1, "2 stops": 2, "3 stops": 3, "4 stops": 4}, inplace = True)

# Concatenate dataframe --> test_data + Airline + Source + Destination
test_data = pd.concat([test_data, Airline, Source, Destination], axis = 1)

test_data.drop(["Airline", "Source", "Destination"], axis = 1, inplace = True)
print()
print()

#cleaning test_data
test_data=clean_dataset(test_data)

"""## **Feature Selection**

---
Three best technique to select best festures that are more correlated with Price

---
1.   Heatmap
2.   feature_importance
3.   selectKBest






"""

train_data.columns

#All independent variables
X=train_data.loc[:,['Total_Stops', 'Journey_day', 'Journey_month', 'Dep_hour',
       'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hour',
       'Duration_min', 'Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New Delhi',
       'Chennai', 'Delhi', 'Kolkata', 'Mumbai', 'Air India', 'GoAir', 'IndiGo',
       'Jet Airways', 'Jet Airways Business', 'Multiple carriers',
       'Multiple carriers Premium economy', 'SpiceJet', 'Vistara',
       'Vistara Premium economy']]

#Dependent variable "Price" column       
y=train_data.iloc[:,1]
X.shape
y.shape

#to see corretion between different variables/features
from matplotlib import figure
plt.figure(figsize=(20,20))
sns.heatmap(data.corr(), annot=True, cmap="YlGnBu")
plt.show()

#Selecting Important features using ExtraTreeRegressor
from sklearn.ensemble import ExtraTreesRegressor
selection=ExtraTreesRegressor()
selection.fit(X,y)

#Graph for better Visualization
plt.figure(figsize=(12,8))
feature_importance=pd.Series(selection.feature_importances_, index=X.columns)
feature_importance.nlargest(20).plot(kind='barh')
plt.show()

"""# **Fitting model using Random Forest**

---



1.   Split dataset into train and test set in order to prediction w.r.t X_test.
2.   If needed do scaling of data but Scaling is not done in Random forestImport model.
3.   Fit the data and then Predict w.r.t X_test.
4.   In regression check RSME ScorePlot graph.

"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
from sklearn.ensemble import RandomForestRegressor
reg_rf = RandomForestRegressor()
reg_rf.fit(X_train, y_train)

#Prediction of test_set
y_pred = reg_rf.predict(X_test)

"""**without Hyperparameter tunning**"""

#Accuracy With train_data
reg_rf.score(X_train, y_train)

#Accuracy With test_data

reg_rf.score(X_test, y_test)

#Next two graph will show difference in actual value and predicted value of "Price"
sns.distplot(y_test-y_pred)
plt.show()

plt.scatter(y_test, y_pred, alpha = 0.5)
plt.xlabel("y_test")
plt.ylabel("y_pred")
plt.show()

#Evaluation of Model without Hyperparameter tunning
from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(y_test, y_pred))
print('MSE:', metrics.mean_squared_error(y_test, y_pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

metrics.r2_score(y_test, y_pred)

"""#**Hyperparameter Tuning**

---


Choose following method for hyperparameter tuning

*   RandomizedSearchCV --> Fast than GridSearchCV
*   Assign hyperparameters in form of dictionery





Fit the model and
Check best paramters and best score
"""

from sklearn.model_selection import RandomizedSearchCV

#Randomized Search CV

# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(5, 30, num = 6)]
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10, 15, 100]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 5, 10]

# Create the random grid

random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf}
               
# Random search of parameters, using 5 fold cross validation, 
# search across 100 different combinations
rf_random = RandomizedSearchCV(estimator = reg_rf, param_distributions = random_grid,scoring='neg_mean_squared_error', n_iter = 10, cv = 5, verbose=2, random_state=42, n_jobs = 1)
rf_random.fit(X_train,y_train)

rf_random.best_params_

prediction = rf_random.predict(X_test)

"""**After Hyperparameter tunning**"""

plt.figure(figsize = (8,8))
sns.distplot(y_test-prediction)
plt.show()

plt.figure(figsize = (8,8))
plt.scatter(y_test, prediction, alpha = 0.5)
plt.xlabel("y_test")
plt.ylabel("y_pred")
plt.show()

print('MAE:', metrics.mean_absolute_error(y_test, prediction))
print('MSE:', metrics.mean_squared_error(y_test, prediction))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, prediction)))

# Here We can see Accuracy of our Classifier increases with Hyperparameter tunning
y=rf_random.predict(X_test)
metrics.r2_score(y_test, y)

#Prediction on a new case
#Consider a situation Fare prediction for Airline flight from Delhi to Chennai with zero stops
''' [ 'Total_Stops'=0, 'Journey_day'=15, 'Journey_month'=8, 'Dep_hour'=10,
       'Dep_min'=00, 'Arrival_hour'=12, 'Arrival_min'=30, 'Duration_hour'=2,
       'Duration_min'=30, 'Cochin'=0, 'Delhi'=1, 'Hyderabad'=0, 'Kolkata'=0, 'New Delhi'=0,
       'Chennai'=1, 'Delhi'=0, 'Kolkata'=0, 'Mumbai'=0, 'Air India'=1, 'GoAir'=0, 'IndiGo'=0,
       'Jet Airways'=0, 'Jet Airways Business'=0, 'Multiple carriers'=0,
       'Multiple carriers Premium economy'=0, 'SpiceJet'=0, 'Vistara'=0,
       'Vistara Premium economy'=0] '''
rf_random.predict([[0,15,8,10,0,12,30,2,30,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0, 0, 0, 0]])

#Predicted Price is Approx. Rs.4666