import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

fname = "bp.csv"
def read(fname):
    df = pd.read_csv(fname, skiprows=1, infer_datetime_format=True, index_col="dt",keep_default_na=False, parse_dates=True,dayfirst=True)
                
    df["pulse"] = pd.to_numeric(df["pulse"])
    df.index = pd.to_datetime(df.index)
    print(df.describe())
    print(df.head())
    return df
def hist(df):
    fig,ax = plt.subplots()
    sns.pairplot(df,hue=df.index)
    plt.show()
def group_data(df,how=""):

        #group the dataframe given by the chosen time frame.
        if how.lower() == "day":
            grouped = df.groupby(df.index.weekday)
        elif how.lower() == "week":
            grouped = df.groupby(df.index.week)
        elif how.lower() == "hour":
            grouped = df.groupby(df.index.hour)
        elif how.lower() == "month":
            grouped = df.groupby(df.index.month)
        elif how.lower() == "year":
            grouped = df.groupby(df.index.year)
        else:
            print("Not given correct timeframe. Try 'hour','day','week','month','year'.")
            return
        
        #convert the 'groupby' pandas class into list of dataframes
        grouped_dfs = [grouped.get_group(x) for x in grouped.groups]

        #merge the list of dataframes into one dataframe, using the time as the index
        grouped_df = pd.DataFrame()
        for x in range(len(grouped_dfs)):
            grouped_df = grouped_df.merge(grouped_dfs[x],left_index=True,right_index=True,how="outer",suffixes=("",(x+1)))
            grouped_df = grouped_df.rename(columns={grouped_df.columns[x]:(x+1)})
        

        return grouped_df
def box(df,how="",savefile=None,by=""):
        """Creates a box and whisker plot of every range of time given a time interval. For example,
        a box plot is made for every day of the week if how="week"

        IN:
            self - Data object

            how - string ("hour","day","week","month","year")
                time interval to group each objects data into. For example, how="hour" will group every objects data into
                24 dataframes, 1 for each hour.
            savefile - string (optional, default None)
                Path to save the created box plot to.
        
        OUT:
            'savefile'.png - image, optional
                Image of the graph created if given a path in 'savefile'
        """
        #take data from self and group it by chosen time frame
        grouped_df = group_data(df,how)
        
        #plot graph
        fig,ax = plt.subplots()
        ax.set_title(by)
        sns.boxplot(data=grouped_df,ax=ax)
        ax.set_xlabel(how.title())
        if how.lower() == "week":
            ax.set_xticks(np.arange(1,52,2))
        plt.show()
        
def time(df):
    fig,ax = plt.subplots()
    plt.plot(df.index,df["pulse"])
    plt.show()
df = read(fname)
box(df["dia"],"day")