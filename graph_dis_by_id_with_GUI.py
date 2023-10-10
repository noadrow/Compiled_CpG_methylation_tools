import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5, 5))

def count_FTP(self):
    FP = (self.dataList['TEST'] == 'FP').sum()
    TP = (self.dataList['TEST'] == 'TP').sum()

    return [FP, TP]
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

Tk().withdraw()
print('waiting for data')
print('...')
t0 = time.time()
df = load_pickle_to_df()
print(f'data loaded in {time.time() - t0} seconds')
print('...')
def barplot_range_count(df, group, cgs):
    # cgs = df.index.to_list()[:len(df) - 4]
    plt.clf()

    for cg in cgs:
        cg = cg.replace(" ", "")
        if (cg in df.index):
            working_df = df.loc[cg]
            new_pd = pd.DataFrame({
                'range': pd.cut(working_df, np.arange(0, 1, 0.01)),
                'val': working_df,
                'index': working_df.index,
                'counter': [1] * len(working_df)
            })

            plt.ion()
            range_count = new_pd.groupby('range')['counter'].count()
            x_labels = [float(str(label).split(',')[0].replace("(", "")) for label in range_count.index]
            ax.set_xticks(range(len(x_labels)))
            ax.set_xticklabels(x_labels, rotation=90)
            ax.set_xticks([0.01, 0.5, 1])
            ax.set_xlabel('Beta-val')
            ax.set_ylabel('Frequency')
            ax.set_title(f"{cg}_{group}_barh")
            plt.bar(x_labels, list(range_count.values),width=0.005)
            plt.draw()
            plt.show()

            #range_count.plot.bar(rot=90, figsize=(5, 5))
            #fig.savefig(f"{cg}_{group}_barh.png")
            #plt.ioff()
            #plt.close(fig)
        else:
            print("CpG not found")

class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.dataList = pd.DataFrame()
        self.currentIndex = 0

        self.layout = QVBoxLayout(self)

        self.textEdit = QTextEdit(self)
        self.layout.addWidget(self.textEdit)

        self.loadButton = QPushButton("Load", self)
        self.layout.addWidget(self.loadButton)

        self.graphView = QLabel(self)
        self.layout.addWidget(self.graphView)

        self.tpButton = QPushButton("TP", self)
        self.tnButton = QPushButton("FP", self)
        self.prevButton = QPushButton("Previous", self)
        self.nextButton = QPushButton("Next", self)
        self.layout.addWidget(self.tpButton)
        self.layout.addWidget(self.tnButton)
        self.layout.addWidget(self.prevButton)
        self.layout.addWidget(self.nextButton)

        self.loadButton.clicked.connect(self.load_data)
        self.tpButton.clicked.connect(lambda: self.label_graph("TP"))
        self.tnButton.clicked.connect(lambda: self.label_graph("FP"))
        self.prevButton.clicked.connect(self.show_previous_graph)
        self.nextButton.clicked.connect(self.show_next_graph)

        self.setLayout(self.layout)

    def load_data(self):
        input_data = self.textEdit.toPlainText()
        cg_list = input_data.split('\n')
        self.dataList.index = cg_list
        self.dataList['TEST'] = None
        self.currentIndex = 0
        if not self.dataList.empty:
            self.show_graph()
    def label_graph(self, label):
        if not self.dataList.empty:
            current_item = self.dataList.index[self.currentIndex]
            self.dataList.loc[current_item] = label
            FP, TP = count_FTP(self)
            print(f"FP:{FP},TP:{TP}")

    def show_previous_graph(self):
        if not self.dataList.empty:
            self.currentIndex = (self.currentIndex - 1 + len(self.dataList)) % len(self.dataList)
            self.show_graph()

    def show_next_graph(self):
        if not self.dataList.empty:
            self.currentIndex = (self.currentIndex + 1) % len(self.dataList)
            self.show_graph()

    def show_graph(self):
        current_item = self.dataList.index[self.currentIndex]
        self.plot_graph(current_item)

        FP,TP = count_FTP(self)
        self.graphView.setText(f"current CpG site: {current_item},FP:{FP},TP:{TP}")

    def plot_graph(self, data):
        # Replace this function with your actual graph plotting logic
        # For the sake of example, we're just printing the data
        print("Plotting graph for:", data)
        barplot_range_count(df, "chosen_cgs", [data])

def main():


    app = QApplication(sys.argv)

    widget = GraphWidget()
    widget.setGeometry(100, 100, 800, 600)
    widget.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()