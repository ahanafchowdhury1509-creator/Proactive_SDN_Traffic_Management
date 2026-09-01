import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

df = pd.read_csv('ML/dataset.csv')

X = df[['utilization']]
y = df['label']

model = LogisticRegression()
model.fit(X, y)

with open('ML/model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved to ML/model.pkl")
print("Training accuracy:", model.score(X, y))