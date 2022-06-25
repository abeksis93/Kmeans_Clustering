from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, filedialog, messagebox
import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib as plt
from sklearn.cluster import KMeans


class Clustering:

    def __init__(self, master):
        self.master = master
        master.title("Clustering")

        # self.total = 0
        self.path = ""

        # self.total_label_text = IntVar()
        # self.total_label_text.set(self.total)
        # self.total_label = Label(master, textvariable=self.total_label_text)

        self.path_label = Label(master, text="Select File: ")
        self.clusters_label = Label(master, text="Number of clusters k: ")
        self.runs_label = Label(master, text="Number of runs: ")

        vcmd_path = master.register(self.validate_path) # we have to wrap the command
        vcmd_clusters = master.register(self.validate_clusters) # we have to wrap the command
        vcmd_runs = master.register(self.validate_runs)  # we have to wrap the command

        self.path_entry = Entry(master, validate="key", validatecommand=(vcmd_path, '%P'))
        self.clusters_entry = Entry(master, validate="key", validatecommand=(vcmd_clusters, '%P'))
        self.runs_entry = Entry(master, validate="key", validatecommand=(vcmd_runs, '%P'))

        self.browse_button = Button(master, text="Browse", command=lambda: self.select_file())
        self.reset_button = Button(master, text="Reset", command=lambda: self.reset_entry())
        self.pre_process_button = Button(master, text="Pre-process", command=lambda: self.pre_process())
        self.kmeans_button = Button(master, text="Cluster", command=lambda: self.kmeans())

        # LAYOUT

        self.path_label.grid(row=0, column=0, sticky=W)
        self.path_entry.grid(row=0, column=1, columnspan=3, sticky=W+E)

        self.clusters_label.grid(row=1, column=0, sticky=W)
        self.clusters_entry.grid(row=1, column=1, columnspan=3, sticky=W + E)

        self.runs_label.grid(row=2, column=0, sticky=W)
        self.runs_entry.grid(row=2, column=1, columnspan=3, sticky=W + E)

        self.browse_button.grid(row=10, column=0, sticky=E)
        self.pre_process_button.grid(row=10, column=1)
        self.kmeans_button.grid(row=10, column=2)
        self.reset_button.grid(row=10, column=3, sticky=W+E)

    def validate_path(self, new_text):
        if not new_text:  # the field is being cleared
            self.path = ""
            return True
        try:
            self.path = str(new_text)
            return True
        except FileNotFoundError:
            return False

    def validate_clusters(self, new_text):
        print("clusters new text:  " + new_text)
        if not new_text:  # the field is being cleared
            self.clusters_entry = 1
            return True
        try:
            self.clusters_entry = int(new_text)
            if (self.clusters_entry >= 1) and (self.clusters_entry < 10):
                return True
            return False
        except ValueError:
            return False

    def validate_runs(self, new_text):
        if not new_text:  # the field is being cleared
            self.runs_entry = 0
            return True
        try:
            self.runs_entry = int(new_text)
            if self.runs_entry >= 0:
                return True
            return False
        except ValueError:
            return False

    def select_file(self):
        self.path = filedialog.askopenfilename()
        self.path_entry.insert(0, self.path)

    def reset_entry(self):
        self.path = ""
        self.path_entry.delete(0, END)
        self.clusters_entry.delete(0, END)
        self.runs_entry.delete(0, END)

    def pre_process(self):
        df = self.read_file()
        df.apply(lambda x: sum(x.isnull()), axis=0)
        df.fillna(df.mean(), inplace=True)
        df[df.columns.difference(['country', 'year'])] = preprocessing.StandardScaler().fit_transform(df[df.columns.difference(['country', 'year'])])
        new_df = df[df.columns.difference(['year'])].groupby(['country'], as_index=False).mean()
        # print(new_df)
        messagebox.showinfo("Preprocessing", "Preprocessing completed successfully!")
        self.kmeans(new_df)

    def kmeans(self, df):
        # if self.clusters_entry == "" or self.clusters_entry is None:
        #     self.clusters_entry = 1
        # if self.runs_entry == "" or self.runs_entry is None:
        #     self.runs_entry = 0
        # print("in kmeans")
        k_means = KMeans(n_clusters=self.clusters_entry, init='random', n_init=self.runs_entry).fit(df[df.columns.difference(['country'])])
        print(k_means)
        # pass

    def read_file(self):
        try:
            df = pd.read_excel(self.path)
            return df
        except OSError:
            return False


root = Tk()
my_gui = Clustering(root)
root.geometry("600x400")
root.mainloop()
