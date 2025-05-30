# datafun-04-eda

## Exploratory Data Analysis

This project contians jupyter notebook jordan_eda.ipynb and module stats_jordan.py.  The notebook file comprises of descriptive statistics on seaborn's iris dataset through computation and visualization.  The notebook follows standard EDA format and utilizes widgets and a local module for visualizations.

The module stats_jordan.py contains two functions, pretty_df() and is_norm_small().  The function pretty_df() takes in a pandas dataframe and itterates through all column names and elements of ojbect type columns replacing underscores with spaces and uppercasing all words then returns a pandas dataframe.  The function is_norm_small() is a function intended to aid in the assessment of the normality of a given data set.  is_norm_small() take in a pandas dataframe and plots a qqplot and runs the Shapiro-Wilk normality test for all columns in the dataframe.  The function also has optional input arg 'by' which will plot all columns by an added cattegorical column. (i.e. by = 'categorical_colname'). For a demonstration run stats_jordan.py to see qqplots of iris_length by species for the seaborn iris data set. 
