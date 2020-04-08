# import sys
# if sys.version_info[0] < 3:
#     from StringIO import StringIO
# else:
#     from io import StringIO
# import pandas as pd
# import numpy as np
# import requests
# import json
# import csv
# import math
#
# # Class Entry:
# #    def __init__(self, idPass, has_survived, pclass, name, gender, age, siblings, parch, ticket, fare, cabin, embarked):
# #        self.id = idPass
# #        self.has_survived = has_survived
# #        self.pclass = pclass
# #        self.name = name
# #        self.gender = gender
# #        self.age = age
# #        self.siblings = siblings
# #        self.parch = parch
# #        self.ticket = ticket
# #        self.fare = fare
# #        self.cabin = cabin
# #        self.embarked = embarked
#
#
#
# def main():
#     col = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
#     df = pd.DataFrame(columns=col)
#     df_unclean = pd.DataFrame(columns=col)
#
#     counters_nulls = {
#             "PassengerId": 0,
#             "Survived": 0,
#             "Pclass": 0,
#             "Name": 0,
#             "Sex": 0,
#             "Age": 0,
#             "SibSp": 0,
#             "Parch": 0,
#             "Ticket": 0,
#             "Fare": 0,
#             "Cabin": 0,
#             "Embarked": 0
#             }
#     current_entry = 0
#
#     while(True):
#         req = requests.get('http://127.0.0.1:5000/survivors')
#         resp = json.loads(req.text)
#         try:
#             data = resp["data"]
#         except KeyError as e:
#             print("The api has exauseted the data")
#             break
#
#         pandadata = StringIO(data)
#         pandadata2 = StringIO(data)
#         df_unclean = df_unclean.append(dict(zip(col, pd.read_csv(pandadata2))), ignore_index=True)
#         df = df.append(dict(zip(col, pd.read_csv(pandadata))), ignore_index=True)
#
#         #df_unclean = df.append(dict(zip(col, pd.read_csv(pandadata))), ignore_index=True)
#         # We change the sex field to a machine readable format
#         df["Sex"].replace({"male": "1", "female": "0"}, inplace=True)
#
#         # We combine the siblings and the family members into a single column
#         df["SibSp"] = pd.to_numeric(df["SibSp"], errors='coerce')
#         df["Parch"] = pd.to_numeric(df["Parch"], errors='coerce')
#         df["FamilyMember"] = df["SibSp"].apply(np.floor) + df["Parch"].apply(np.floor) + 1
#
#
#         # We collect the titles and parse them to numeric values
#         df['Title'] = df['Name'].apply(lambda x: x.split(",")[1].split(".")[0].strip())
#         df["Title"] = df["Title"].replace(['Lady', 'the Countess','Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
#         df['Title'] = df['Title'].replace('Mlle', 'Miss')
#         df['Title'] = df['Title'].replace('Ms', 'Miss')
#         df['Title'] = df['Title'].replace('Mme', 'Mrs')
#
#         df["Title"] = df["Title"].replace({"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5})
#
#         # print('Loop check')
#         for el in col:
#             if df[el].tail(1).isnull().bool():
#                 # print("Loop Check inside")
#                 # print(df[el])
#                 counters_nulls[el] += 1
#         current_entry += 1
#
#         # Parent & Siblings
#         df['withP']=0
#         df['withS']=0
#
#         df.loc[df['SibSp'] > 0, 'withS'] = 1
#         df.loc[df['Parch'] > 0, 'withP'] = 1
#
#         # Fare Check
#         df["Fare_log"] = df["Fare"].fillna(df["Fare"].median())
#         # df['Fare_log'] = df["Fare"].map(lambda i: np.log(i) if i > 0 else 0)
#
#
#
#     df.drop(columns=['SibSp', 'Parch', 'Cabin', 'Name'])
#     print(counters_nulls)
#
#
# if __name__ == '__main__':
#     main()

##### Full Working Code from LUCA

import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
import pandas as pd
import numpy as np
import requests
import json
import csv
import math

def main():
    col = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
    df = pd.DataFrame(columns=col)
    df_unclean = pd.DataFrame(columns=col)

    counters_nulls = {
        "PassengerId": 0,
        "Survived": 0,
        "Pclass": 0,
        "Name": 0,
        "Sex": 0,
        "Age": 0,
        "SibSp": 0,
        "Parch": 0,
        "Ticket": 0,
        "Fare": 0,
        "Cabin": 0,
        "Embarked": 0
    }
    current_entry = 0

    while(True):
        req = requests.get('http://127.0.0.1:5000/survivors')
        resp = json.loads(req.text)
        try:
            data = resp["data"]
        except KeyError as e:
            print("The api has exauseted the data")
            break

        pandadata = StringIO(data)
        pandadata2 = StringIO(data)
        df_unclean = df_unclean.append(dict(zip(col, pd.read_csv(pandadata2))), ignore_index=True)

        df = df.append(dict(zip(col, pd.read_csv(pandadata))), ignore_index=True)

        # We change the sex field to a machine readable format
        df["Sex"].replace({"male": "1", "female": "0"}, inplace=True)

        # We combine the siblings and the family members into a single column
        df["SibSp"] = pd.to_numeric(df["SibSp"], errors='coerce')
        df["Parch"] = pd.to_numeric(df["Parch"], errors='coerce')
        df["FamilyMember"] = df["SibSp"].apply(np.floor) + df["Parch"].apply(np.floor) + 1


        # We collect the titles and parse them to numeric values
        df['Title'] = df['Name'].apply(lambda x: x.split(",")[1].split(".")[0].strip())
        df["Title"] = df["Title"].replace(['Lady', 'the Countess','Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
        df['Title'] = df['Title'].replace('Mlle', 'Miss')
        df['Title'] = df['Title'].replace('Ms', 'Miss')
        df['Title'] = df['Title'].replace('Mme', 'Mrs')

        df["Title"] = df["Title"].replace({"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5})


        for el in col:
            try:
                if "Unnamed:" in df[el].tail(1).values[0]:
                    counters_nulls[el] += 1
            except TypeError as e:
                pass

        current_entry += 1

        if current_entry > 150:
            for el in col:
                if (100 * counters_nulls[el] / current_entry) < 2:
                    most_used_value = df[el].value_counts(ascending=False, normalize=True).index[0]
                    try:
                        if "Unnamed:" in df[el].tail(1).values[0]:
                            df[el] = df[el].replace(to_replace=r'^Unnamed:.*$', value=most_used_value, regex=True)
                    except TypeError as e:
                        pass
    df.drop(columns=['SibSp', 'Parch', 'Cabin', 'Name'])
    print(counters_nulls)
    print(df_unclean)
    print(df)
    print("The following colums are not suitable because of the high number of null values: ", [x for x in counters_nulls.keys() if (counters_nulls[x] / current_entry * 100) > 10])


if __name__ == '__main__':
    main()
