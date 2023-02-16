import os
import pandas as pd
import json

with open("config.json") as file:
    config = json.load(file)
data_dir = config['save_dir']
files = os.listdir(data_dir)
print(files)
df_list = []
for file_name in files:
    df = pd.read_pickle(os.path.join(data_dir, file_name))
    df = pd.DataFrame(df)
    coin1, coin2 = file_name.split("_")
    if coin1 != 'BTC':
        df['coin'] = coin1[:-4]
    else:
        df['coin'] = coin2[:-4]
    df.drop_duplicates(inplace=True)
    df_list.append(df)
df = pd.concat(df_list)
df.date = df.date.apply(lambda x:int(str(x)[:-3]))
df.to_csv(config['save_path'])