def convert_to_pickle_with_gui():
    import pandas as pd
    from tkinter.filedialog import askopenfilename
    from tkinter import filedialog
    import os
    import time

    print("Waiting for path to csv file")
    path = askopenfilename(title="Choose csv file")
    print("Waiting for path to saving folder")
    save_to = filedialog.askdirectory(title="choose saving directory")
    t0 = time.time()
    print("Waiting for path to data to load")
    print(f"Finished loading path {time.time()-t0}")
    t0 = time.time()
    df = pd.read_csv(path)
    file_name = os.path.basename(path)
    print (f"Finished loading data: {time.time()-t0} sec")
    print("Waiting for conversion to pickle")
    t0 = time.time()
    df.to_pickle(os.path.join(save_to,file_name.replace(".csv",".pkl")))
    print (f"Finished converting to pickle: {time.time()-t0} sec")
    print(f"Conversion successeded, saved to {save_to} with the name {file_name}")

def load_pickle_to_df():
    from tkinter.filedialog import askopenfilename
    import pickle
    import time

    print("Waiting for pickle file path")
    path = askopenfilename(title="Choose a pickle")
    print("Waiting for loading the file")
    file = open(path, 'rb')
    print("File load")
    print("Waiting for pickle to convert to dataframe")
    t0 = time.time()
    df = pickle.load(file)
    df.index = df.iloc[:,0]
    df = df.drop(df.columns[0], axis=1)
    print(f"Dataframe loaded: {time.time()-t0} sec")
    file.close()
    return df

#convert_to_pickle_with_gui()
load_pickle_to_df()