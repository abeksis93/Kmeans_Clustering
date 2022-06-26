import sys
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, filedialog, messagebox, PhotoImage
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import chart_studio.plotly as py
import plotly.express as px


class Clustering:

    """
    A class to represent a clustering algorithm.

    ...

    Attributes
    ----------
    path : str
        path to the data file
    clusters : int
        number of clusters for k-means clustering algorithm
    runs : int
        number of runs of the k-means clustering algorithm
    final_df : dataframe
        the final dataframe after cleaning data with classification label
    

    Methods
    -------
    init(master):
        a constructor for the class. 
        recives from a user and initializes all the data for running the clustering algorithm
    
    read_file():
        reads an excel data file and creates a dataframe 
    
    validate_path(new_text):
        validating the file path
        
    validate_clusters(new_text):
         validating the number of clusters

    validate_runs(new_text):
        validating the number of runs
        
    select_file():
        browse the operating system to select a file
        
    reset_entry():
        clear the entries in the frame
        
    pre_process():
        clean the data: includes filling missing values with average, normalizing data and group by country     
    
    kmeans():
         run the clusering algorithm and export the data and labels to excel
         
    plot_clusters(df):
        plot:
            1. scatter plot of generosity as a function of social support
            2. country map colored by the classification
    """
    
    def __init__(self, master):
        """
        a constructor for the class. 
        recives from a user and initializes all the data for running the clustering algorithm

        Parameters
        ----------
            master : tkinter frame
                a frame for a simple GUI program
        """
        
        # setting the frame
        self.master = master
        master.title("K Means Clustering")

        # initializing attributes
        self.path = ""
        self.clusters = None
        self.runs = None
        self.final_df = None

        # labels in frame
        self.path_label = Label(master, text="Select File:")
        self.clusters_label = Label(master, text="Number of clusters k:")
        self.runs_label = Label(master, text="Number of runs:")

        # validation checks when input recived
        vcmd_path = master.register(self.validate_path) # we have to wrap the command
        vcmd_clusters = master.register(self.validate_clusters) # we have to wrap the command
        vcmd_runs = master.register(self.validate_runs)  # we have to wrap the command

        # input boxs in frame
        self.path_entry = Entry(master, validate="key", validatecommand=(vcmd_path, '%P'))
        self.clusters_entry = Entry(master, validate="key", validatecommand=(vcmd_clusters, '%P'))
        self.runs_entry = Entry(master, validate="key", validatecommand=(vcmd_runs, '%P'))

        # buttons in frame
        self.browse_button = Button(master, text="Browse", command=lambda: self.select_file())
        self.reset_button = Button(master, text="Reset", command=lambda: self.reset_entry())
        self.pre_process_button = Button(master, text="Pre-process", command=lambda: self.pre_process())
        self.kmeans_button = Button(master, text="Cluster", command=lambda: self.kmeans())

        
        # frame layout
        
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
        """
        read an excel data file and create a dataframe
        """
        try:
            df = pd.read_excel(self.path)
            return df
        except OSError:
            return False

        
    def validate_path(self, new_text):
        """
         validating the file path
         
         Parameters
        ----------
            new_text : string
                input file path from user
        """
        if not new_text:  # the field is being cleared
            self.path = ""
            return True
        try:
            self.path = str(new_text)
            return True
        except FileNotFoundError:
            return False

        
    def validate_clusters(self, new_text):
        """
         validating the number of clusters
         
         Parameters
        ----------
            new_text : int
                input number of clusters from user
        """
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
        """
         validating the number of runs
         
         Parameters
        ----------
            new_text : int
                input number of runs from user
        """
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
        """
         browse the operating system to select a file
        """
        self.path = filedialog.askopenfilename()
        self.path_entry.insert(0, self.path)

        
    def reset_entry(self):
        """
         clear the entries in the frame
        """
        self.path_entry.delete(0, END)
        self.clusters_entry.delete(0, END)
        self.runs_entry.delete(0, END)
        self.path = ""
        self.clusters = None
        self.runs = None
        self.final_df = None

    def pre_process(self):
        """
         clean the data: includes filling missing values with average, normalizing data and group by country 
        """
        
        # if missing values show warnings
        if self.path == "":
            messagebox.showwarning("K Means Clustering", "Missing values: file path is required")
            return False
        if type(self.clusters) is not int:
            messagebox.showwarning("K Means Clustering", "Missing values: 'Number of clusters k' is required")
            return False
        if type(self.runs) is not int:
            messagebox.showwarning("K Means Clustering", "Missing values: 'Number of runs' is required")
            return False
        
        # clean data
        df = self.read_file()
        df.apply(lambda x: sum(x.isnull()), axis=0)
        df.fillna(df.mean(), inplace=True)
        df[df.columns.difference(['country', 'year'])] = preprocessing.StandardScaler().fit_transform(df[df.columns.difference(['country', 'year'])])
        new_df = df[df.columns.difference(['year'])].groupby(['country'], as_index=False).mean()
        messagebox.showinfo("K Means Clustering", "Preprocessing completed successfully!")
        self.final_df = new_df

        
        
    def kmeans(self):
        """
         run the clusering algorithm and export the data and labels to excel
        """
        
        # if data didn't pre-process show warning
        if self.final_df is None:
            messagebox.showwarning("K Means Clustering", "Preprocessing is required before clustering!")
            return False
        
        # run a k-means clustering
        df = self.final_df
        k_means = KMeans(n_clusters=self.clusters, init='random', n_init=self.runs).fit(df[df.columns.difference(['country'])])
        df['labels'] = k_means.labels_
        messagebox.showinfo("K Means Clustering", "Clustering completed successfully!")
        df.to_excel('clean_data.xlsx', index=False)
        self.plot_clusters(df)

        
    def plot_clusters(self, df):
        """
         plot:
            1. scatter plot of generosity as a function of social support
            2. country map colored by the classification
            
        Parameters
        ----------
            df : dataframe
                the new dataframe after pre-processing with labels
        """
        
        # scatter plot
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
        
        # choropleth plot
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

