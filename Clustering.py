import sys
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, filedialog, messagebox, PhotoImage
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import chart_studio.plotly as py
import plotly.express as px


class Clustering:

    def __init__(self, master):
        self.master = master
        master.title("K Means Clustering")

        self.path = ""
        self.clusters = None
        self.runs = None
        self.final_df = None

        self.path_label = Label(master, text="Select File:")
        self.clusters_label = Label(master, text="Number of clusters k:")
        self.runs_label = Label(master, text="Number of runs:")

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

        self.browse_button.grid(row=0, column=10, sticky=E)
        self.pre_process_button.grid(row=10, column=1)
        self.kmeans_button.grid(row=10, column=2)
        self.reset_button.grid(row=10, column=3, sticky=W+E)

    def read_file(self):
        try:
            df = pd.read_excel(self.path)
            return df
        except OSError:
            return False

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
        if not new_text:  # the field is being cleared
            self.clusters = None
            return True
        try:
            self.clusters = int(new_text)
            if (self.clusters >= 1) and (self.clusters < 10):
                return True
            return False
        except ValueError:
            return False

    def validate_runs(self, new_text):
        if not new_text:  # the field is being cleared
            self.runs = None
            return True
        try:
            self.runs = int(new_text)
            if self.runs > 0:
                return True
            return False
        except ValueError:
            return False

    def select_file(self):
        self.path = filedialog.askopenfilename()
        self.path_entry.insert(0, self.path)

    def reset_entry(self):
        self.path_entry.delete(0, END)
        self.clusters_entry.delete(0, END)
        self.runs_entry.delete(0, END)
        self.path = ""
        self.clusters = None
        self.runs = None
        self.final_df = None

    def pre_process(self):
        if self.path == "":
            messagebox.showwarning("K Means Clustering", "Missing values: file path is required")
            return False
        if type(self.clusters) is not int:
            messagebox.showwarning("K Means Clustering", "Missing values: 'Number of clusters k' is required")
            return False
        if type(self.runs) is not int:
            messagebox.showwarning("K Means Clustering", "Missing values: 'Number of runs' is required")
            return False
        df = self.read_file()
        df.apply(lambda x: sum(x.isnull()), axis=0)
        df.fillna(df.mean(), inplace=True)
        df[df.columns.difference(['country', 'year'])] = preprocessing.StandardScaler().fit_transform(df[df.columns.difference(['country', 'year'])])
        new_df = df[df.columns.difference(['year'])].groupby(['country'], as_index=False).mean()
        messagebox.showinfo("K Means Clustering", "Preprocessing completed successfully!")
        self.final_df = new_df

    def kmeans(self):
        if self.final_df is None:
            messagebox.showwarning("K Means Clustering", "Preprocessing is required before clustering!")
            return False
        df = self.final_df
        k_means = KMeans(n_clusters=self.clusters, init='random', n_init=self.runs).fit(df[df.columns.difference(['country'])])
        df['labels'] = k_means.labels_
        messagebox.showinfo("K Means Clustering", "Clustering completed successfully!")
        df.to_excel('clean_data.xlsx', index=False)
        self.plot_clusters(df)

    def plot_clusters(self, df):
        plt.figure(1)
        plt.clf()
        plt.scatter(df['Social support'], df['Generosity'], c=df['labels'])
        plt.title('K Means Clustering')
        plt.xlabel('Social support')
        plt.ylabel('Generosity')
        plt.colorbar()
        plt.savefig("plot.png")
        photo = PhotoImage(file="plot.png")
        photo = photo.subsample(1, 1)
        img = Label(root, image=photo)
        img.image = photo
        img.place(x=10, y=100)
        py.sign_in("yoni93", "X5hK2SJ7Nv94S0kmafup")
        fig = px.choropleth(df, locations='country', color='labels', color_continuous_scale="Viridis", scope="world", locationmode='country names', width=600, height=400,)
        py.image.save_as(fig, filename='name.png')
        world_photo = PhotoImage(file="name.png")
        world_photo = world_photo.subsample(1, 1)
        world_img = Label(root, image=world_photo)
        world_img.image = world_photo
        world_img.place(x=660, y=100)


def _quit():
    root.quit()
    root.destroy()

root = Tk()
root.protocol("WM_DELETE_WINDOW", _quit)
my_gui = Clustering(root)
root.geometry("1280x720")
root.mainloop()
sys.exit()

