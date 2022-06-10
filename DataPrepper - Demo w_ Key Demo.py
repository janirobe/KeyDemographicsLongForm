import pandas as pd

### Read csv
#df = demo
#df2 = key demo

df = pd.read_csv("../DataPrep_DemoWithKeyDemo_Python/data.csv", header=0)
df2 = pd.read_excel("../DataPrep_DemoWithKeyDemo_Python/key.xlsx", header=None)

#%% Prep Df1

df = df.drop_duplicates(subset=['AlexID'])

if 'First Name' in df:
    df = df.drop('First Name', 1)
if 'Last Name' in df:
   df = df.drop('Last Name', 1)

#%% df2 Prep
#getting name of questionnaire
name = df2.iloc[0][0]

#deleting first 2 rows
df2 = df2.iloc[2:]

df2.columns = df2.iloc[0]
df2 = df2[1:]

#moving AlexID to front
col = df2.pop("AlexID")
df2.insert(0, col.name, col)

#Dropping from after Alex to Existing Contact
df2 = df2.drop(df2.iloc[:, 1:df2.columns.get_loc("Do you have a Job?")], axis = 1)

if 'datetime - time' in df2:
    df2 = df2.drop('datetime - time', 1)
    
df2['datetime - date'] = pd.to_datetime(df2['datetime - date'])
df2['date'] = df2['datetime - date'].dt.date

## popping date column and putting it where old one is, than dropping old date column
col = df2.pop("date")
df2.insert(df2.columns.get_loc("datetime - date"), col.name, col)
df2 = df2.drop('datetime - date', 1)


#%% merge

df3 = df.merge(df2, left_on='AlexID', right_on="AlexID")

csvName = 'Processed_'+name+'.csv'

df3.to_csv(csvName, index=False)