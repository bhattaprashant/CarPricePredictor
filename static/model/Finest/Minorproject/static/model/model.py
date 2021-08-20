import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
import pickle
car=pd.read_csv('ScrappedData.csv')
car=car[['Brand','Model','Model_year','Transmission','Engine_size(cc)',
 'Drivetrain','Fuel_type','Lot_no','Kilometer','Price']]
car.dropna(inplace=True)
car.info()
car["Kilometer"] = pd.to_numeric(car.Kilometer, errors='coerce')
car['Price'] = car['Price'].apply(lambda x: float(x.replace('Rs.','')))
car['Drivetrain'] = car['Drivetrain'].apply(lambda x: float(x.replace('WD','')))
car.info()
car.dropna(inplace=True)
X=car.drop(columns='Price')
y=car['Price']
X
y
car.isnull().sum()
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2, random_state=230)
list1=[]
for col in X_train.columns:
  if X_train[col].dtypes!='O':
   list1.append(col)
list2=[]
for col in X_train.columns:
  if X_train[col].dtypes=='O':
   list2.append(col)
   
ohe=OneHotEncoder()
ohe.fit(X[list2])
column_trans=make_column_transformer((OneHotEncoder(categories=ohe.categories_),list2),remainder='passthrough')
column_trans.fit_transform(X)
lr = LinearRegression()
pipe=make_pipeline(column_trans,lr)
pipe.fit(X_train ,y_train)
y_pred=pipe.predict(X_test)
print(r2_score(y_test,y_pred))
y=pipe.predict(pd.DataFrame([['Chevrolet','aveo',2018,' Automatic',2000, 4,' Petrol',8,100]],columns=['Brand','Model','Model_year','Transmission','Engine_size(cc)','Drivetrain','Fuel_type','Lot_no','Kilometer']))
print(y)
rms = mean_squared_error(y_test,y_pred, squared=False)
with open('used_car_price_model.pickle','wb') as f:
    pickle.dump(pipe,f)

