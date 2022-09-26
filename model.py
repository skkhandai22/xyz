import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle


diamond_df = pd.read_csv('diamonds.csv', index_col=0)


# print(diamond_df.shape)
# print(diamond_df.isna().sum())
# print(diamond_df.dtypes)

# print(diamond_df.cut.value_counts())
# print(diamond_df.color.value_counts())
# print(diamond_df.clarity.value_counts())

# Encoding
cut_mapping = {'Fair': 0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4}
diamond_df.cut = diamond_df.cut.map(cut_mapping)

# Encoding
color_mapping = {'J': 0, 'I': 1, 'H': 2, 'G': 3, 'F': 4, 'E': 5, 'D': 6}
diamond_df.color = diamond_df.color.map(color_mapping)

# Encoding
clarity_mapping = {'I1': 0, 'SI2': 1, 'SI1': 2, 'VS2': 3, 'VS1': 4, 'VVS2': 5, 'VVS1': 6, 'IF': 7}
diamond_df.clarity = diamond_df.clarity.map(clarity_mapping)


diamond_df = diamond_df.drop(diamond_df[diamond_df["x"]==0].index)
diamond_df = diamond_df.drop(diamond_df[diamond_df["y"]==0].index)
diamond_df = diamond_df.drop(diamond_df[diamond_df["z"]==0].index)

diamond_df = diamond_df[diamond_df['depth'] < diamond_df['depth'].quantile(0.99)]
diamond_df = diamond_df[diamond_df['table'] < diamond_df['table'].quantile(0.99)]
diamond_df = diamond_df[diamond_df['x'] < diamond_df['x'].quantile(0.99)]
diamond_df = diamond_df[diamond_df['y'] < diamond_df['y'].quantile(0.99)]
diamond_df = diamond_df[diamond_df['z'] < diamond_df['z'].quantile(0.99)]

model_df = diamond_df.copy()
X = model_df.drop(['price'], axis=1)
y = model_df['price']

xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=1)


reg1 = DecisionTreeRegressor(max_depth=13)
reg1.fit(xtrain, ytrain)

# Prediction
ypred =  reg1.predict(xtest)

# Checking Accuracy
print(r2_score(ytest, ypred))

pickle.dump(reg1, open('model.pkl', 'wb'))
