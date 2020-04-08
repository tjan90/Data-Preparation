import pandas as pd

train_df = pd.read_csv("train.csv")

train_df['FamilySize'] = train_df['SibSp'] + train_df['Parch'] + 1
print(train_df)
