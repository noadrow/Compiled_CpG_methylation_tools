import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog  import askstring
from time import time
import json
from tkinter import messagebox
import os
import pickle

Tk().withdraw()
def read_cgs(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file]
    return lines
def graph_cg_to_beta_dist(df, batch,path):
    for i in range(0, df.shape[0] - 2):
        cg = df.index[i]
        ages = df.loc['age']
        genders = df.loc['gender']
        new_df = pd.DataFrame({cg: df.iloc[i], 'age': ages, 'gender': genders})
        fig = sns.catplot(data=new_df, x="age", y=cg, hue="gender", jitter=False).fig
        fig.savefig(f'{path}/{cg}_{batch}.png')
        plt.clf()
        plt.close(fig)

def barplot_range_count(df,group,relative_path):
    cgs = df.index.to_list()
    for cg in cgs:
        working_df = df.loc[cg]
        keyList = pd.cut(working_df.values,np.arange(0, 1, 0.01)).categories.values
        new_pd = pd.DataFrame({
            'range': pd.cut(working_df.values,np.arange(0, 1, 0.01)),
            'val': working_df,
            'index': working_df.index,
            'counter': [1] * len(working_df)
        })
        range_count = new_pd.groupby('range')['counter'].count()

        ax = range_count.plot.bar(rot=90,figsize=(15,10))
        fig = ax.figure
        fig.savefig(f"{relative_path}/{cg}_{group}_barh.png")
        plt.clf()
        plt.close(fig)
def filter_data_1(df_info,tissue_col,ID_col,tissue_type):
    df_filt = df_info[df_info[tissue_col] == tissue_type]
    gsms = df_filt[ID_col].values.tolist()
    return gsms

def manual_loading():
    print("choose a pickle ...")
    beta_path = askopenfilename(title="choose beta-value dataset",filetypes=[("Pickle File", "*.pickle")])
    print("data file entered V")
    print("wating for info file input...")
    info_path = askopenfilename(title="choose info\meta dataset",filetypes=[("csv table File", "*.csv")])
    print("info file entered V")
    print("waiting for cpg list input...")
    cg_path = askopenfilename(title="choose cg list",filetypes=[("cg text File", "*.txt")])
    print("cpg list entered V")
    print('waiting for type of tissue input...')
    tissue_type = askstring(title='tissue type', prompt='Choose the type of tissue to examine.')
    print('type of tissue input entered V')
    print('waiting for gse name input...')
    gse = askstring(title='cohort', prompt='name the cohort (gse)')
    print('cohort name (gse) input entered V')
    print("waiting for saving folder input...")
    relative_path = filedialog.askdirectory(initialdir=os.getcwd(),title="choose where to save graphs")
    print("folder picked V")
    print(f"saving configuration as a json file...")
    parm_list = [beta_path,info_path,cg_path,tissue_type,gse,relative_path]
    create_json_config(parm_list)
    print(f"json configuration file saved at  {relative_path}...")
    return parm_list

def json_config_loading():
    js_config_path = askopenfilename(title="load a jason configuration file",filetypes=[("Json File", "*.json")])
    with open(js_config_path, 'r') as j:
        contents = json.loads(j.read())
    return [contents['data_path'],contents['info_path'],contents['cg_path'],contents['tissue_type'],contents['gse'],contents['save_folder_path']]

def create_json_config(parm_list):
    json_dict_confg= {
        'data_path': parm_list[0],
        'info_path': parm_list[1],
        'cg_path': parm_list[2],
        'tissue_type': parm_list[3],
        'gse': parm_list[4],
        'save_folder_path': parm_list[5]
        }
    with open(f"{parm_list[5]}/{time()}.json", 'w') as fp:
        json.dump(json_dict_confg, fp)
def yes_no_dialog():
    result = messagebox.askyesno("yes for manual configuration?", "Do you want manual configuration?")
    if result:
        return manual_loading()
    else:
        return json_config_loading()

# let the user choose if they want to manually choosing the parameter or using a configuration file
# If they chose manual configuration the configuration saved as a json file
print("waiting for configuration decision...")
beta_path,info_path,cg_path,tissue_type,gse,relative_path = yes_no_dialog()
print("configuration stage finished V")

print("waiting for data to load...")
time0 = time()
file = open(beta_path, 'rb')
df = pickle.load(file)
file.close()
print(f"dataset loaded as a dataframe in {time()-time0} sec V")

time0 = time()
print("loading info dataset...")
df_info = pd.read_csv(info_path)
print(f"info dataset loaded as a dataframe in {time()-time0} sec V")

print("filtering samples by tissue and selected CpG sites...")
time0 = time()
# names of the needed columns
tissue_col, ID_col, age_col= 'tissue', 'GSM', 'age'
# extract samples(GSM) that match tissue type as a list
selected_gsms = filter_data_1(df_info,tissue_col,ID_col,tissue_type)
# extract CpG sites of interest
cgs = read_cgs(cg_path)

# index fixing
print("fixing index for info and data datasets...")
df.index = df.iloc[:, 0]
df_info.index = df_info[ID_col]
print("finished fixing indexes V")

print("selecting CpG and samples(GSMs) of interest...")
#pick fit CpGs out of the list
time0 = time()
fit_cgs = list(set(df.index).intersection(cgs))
df_cg_filtered = df.loc[fit_cgs]
#pick Gsms out of the list
df_gsm_filtered = df_cg_filtered[selected_gsms]
print(f"finished filtering of CpG and samples(GSMs) of interest in {time()-time0} sec V")

print("merging info and data into merged dataframe...")
time0 = time()
merged_df = pd.merge(df_gsm_filtered.T, df_info, left_index=True, right_index=True)
print(f"finished merging in {time()-time0} sec V")

print("plotting beta-values to age...")
time0 = time()
graph_cg_to_beta_dist(merged_df.T,gse,relative_path)
#barplot_range_count(df_filt,gse,relative_path)
print(f"finished plotting process successfully in {time()-time0} sec")
