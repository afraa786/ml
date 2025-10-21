import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

dataset = pd.read_csv('customers-100.csv')
X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1].values

numeric_cols = X.select_dtypes(include=[np.number]).columns
categorical_cols = X.select_dtypes(exclude=[np.number]).columns

imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
X[numeric_cols] = imputer.fit_transform(X[numeric_cols])

onehotencoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
X_encoded = onehotencoder.fit_transform(X[categorical_cols])
X = np.concatenate((X_encoded, X[numeric_cols].values), axis=1)

labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

print(dataset)