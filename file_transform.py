import pandas as pd

data = pd.read_csv("train_data.txt")
data = data.astype({'TF':'int'})
print(data)
data.to_csv("train_data_csv_int.txt", sep='\t')