import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
#Reading File
df = pd.read_excel('House_Price.xlsx')
df.head()
#Checking Duplicated Values
for i in df.columns:
    duplicate = df[i].duplicated().sum()
    print(f'Number of Duplicate Values in column {i}: {duplicate}')
df = df[['Place_Name', 'Bedroom','Price (in Million)', 'Kecamatan', 'Kota','Area (m2)',
       'Price per Area', 'Date Posted', 'Month', 'Year']]
df = df.sort_values(by = ['Date Posted'], ascending= True)
#Finding Number of House on Sale by City
group_city = df.groupby(['Kota'])['Price (in Million)'].nunique().reset_index().rename(columns = {'Price (in Million)':'Number of House'})\
    .sort_values(by = ['Number of House'], ascending=False)
px.bar(group_city, x = 'Kota', y ='Number of House', title = 'Number of House by City', labels={'Kota':'City'})
#Number of House Sold by Year
group_year = df.groupby(['Year'])['Place_Name'].count().reset_index().rename(columns={'Place_Name':'Number of House'})
px.line(group_year, x = 'Year', y='Number of House', title='Number of House on Sale by Year')
#The Median House Price Trend
df_year = df.groupby(['Year'])['Price (in Million)'].median().reset_index().rename(columns={'Price (in Million)':'Median of House Price'})
px.line(df_year, x = 'Year', y = 'Median of House Price', title= 'Median of House Price Each Year')
#Median of House Price Each City by Year
pivot = df.pivot_table(index='Year', values='Price (in Million)', columns='Kota', aggfunc='median').reset_index()
px.bar(pivot, x = 'Year', y=df.Kota.unique().tolist(), title='House Price Median by City per Year', labels={'value':'Number of House'})
#2022 Analysis
df_2022_group = df[df.Year == 2022].groupby(['Kota'])['Price (in Million)'].median().reset_index()\
    .rename(columns={'Price (in Million)':'House Price Median'}).sort_values(by = ['House Price Median'], ascending=False)

px.bar(df_2022_group, x = 'Kota', y = 'House Price Median', labels= {'House Price Median':'Median (in Million)',
                                                                     'Kota':'City'}, 
       title = 'House Price Median by City in 2022')
#Analyzing Area
#Checking the area by each Year
year_area = df.groupby(['Year'])['Area (m2)'].mean().reset_index().rename(columns={'Area (m2)':'Average Area'})
px.line(year_area, x = 'Year', y = 'Average Area', title='Average Area by Year')
#Area by City
group_year_area = df.groupby(['Kota'])['Area (m2)'].mean().reset_index().rename(columns={'Area (m2)':'Area'})
group_year_area = group_year_area.sort_values(by=['Area'], ascending=False)
px.bar(group_year_area, x='Kota', y='Area', title='Average of House Price Area by City')
group_year_area_2022 = df[df.Year == 2022].groupby(['Kota'])['Area (m2)'].mean().reset_index()\
    .rename(columns={'Area (m2)': 'Area'}).sort_values(by = ['Area'], ascending = False)
px.bar(group_year_area_2022, x = 'Kota', y='Area', title= 'House Area by City')
city_price_area = df.groupby(['Kota'])['Price per Area'].median().reset_index().sort_values(by = ['Price per Area'], ascending=False)
px.bar(city_price_area, x= 'Kota', y='Price per Area', title='Median of House Price per Area')
Number of Bedroom
#Finding Number of Bedroom in Each City
df_bedroom = df.groupby(['Kota'])['Bedroom'].mean().reset_index().sort_values(by = ['Bedroom'], ascending=False)
px.bar(df_bedroom, x='Kota', y='Bedroom', title='Number of Bedroom of House in City', labels={'Bedroom':'Number of Bedroom'})
#Correlation of Area and Price
px.scatter(df, x = 'Area (m2)', y= 'Price (in Million)', color='Kota', title = 'Area x Price (in Million)')
#Correlation of Number of Bedroom and Price
px.scatter(df, x='Bedroom', y='Price (in Million)', color = 'Kota', title='Number of Bedroom x Price')
df_corr = df[['Area (m2)', 'Price (in Million)', 'Bedroom']]
corr = df_corr.corr()
plt.title('Correlation Values')
heatmap = sns.heatmap(corr, vmin=-1, vmax=1, annot = True,cmap='BrBG')
#Distribution of Data
px.histogram(df['Price (in Million)'], title='Distribution of Price')
#Distribution of Bedroom
px.histogram(df['Bedroom'], title='Distribution of Bedroom')
#Price Box
px.box(df, y = 'Price (in Million)', title='Price Boxplot')
#Bedroom Box
px.box(df, y = 'Bedroom', title='Bedroom Boxplot')
px.box(df, y='Area (m2)', title='Area Boxplot')
#Checking How Many Outliers in the data
def outlier(df):
    q1 = df.quantile(0.25)
    q3 = df.quantile(0.75)
    iqr = q3-q1
    outlier = df[(df < (q1-iqr*1.5)) | (df> (q3+1.5*iqr))]
    return outlier
for i in df_corr.columns:
    result = outlier(df_corr[i])
    outlier_num = len(result)
    max_outlier = result.max()
    min_outlier = result.min()
    print(f'Number of outlier in column {i} : {outlier_num}')
    print(f'Max outlier value of {i}: {max_outlier}')
    print(f'Min outlier value of {i}: {min_outlier}')
#Handling Outliers
#Capping Outliers price
q1_price = df['Price (in Million)'].quantile(0.25)
q3_price = df['Price (in Million)'].quantile(0.75)
iqr_price = q3_price - q1_price
upper_limit_price = q3_price + (1.5* iqr_price)
lower_limit_price = q1_price - (1.5*iqr_price)
df['Price (in Million)'] = np.where(df['Price (in Million)']>upper_limit_price, upper_limit_price, 
                                    np.where(df['Price (in Million)']<lower_limit_price, lower_limit_price, df['Price (in Million)']))
px.box(df, y='Price (in Million)', title='Price in Million After Capping')
#Handling The Bedroom Outliers
q1_bedroom = df['Bedroom'].quantile(0.25)
q3_bedroom = df['Bedroom'].quantile(0.75)
iqr_bedroom = q3_bedroom - q1_bedroom
upper_limit_bedroom = q3_bedroom+ (1.5*iqr_bedroom)
lower_limit_bedroom = q1_bedroom - (1.5*iqr_bedroom)
df['Bedroom'] = np.where(df['Bedroom']>upper_limit_bedroom, upper_limit_bedroom, 
                                    np.where(df['Bedroom']<lower_limit_bedroom, lower_limit_bedroom, df['Bedroom']))
px.box(df, y = 'Bedroom', title='Bedroom After Capping')
#Handling The Area Outliers
q1_area = df['Area (m2)'].quantile(0.25)
q3_area = df['Area (m2)'].quantile(0.75)
iqr_area = q3_area - q1_area
upper_limit_area = q3_area + (iqr_area*1.5)
lower_limit_area = q1_area - (iqr_area*1.5)
df['Area (m2)'] = np.where(df['Area (m2)']>upper_limit_area, upper_limit_area, 
                                    np.where(df['Area (m2)']<lower_limit_area, lower_limit_area, df['Area (m2)']))
#Handling Price per Area Outliers
q1_price_area = df['Price per Area'].quantile(0.25)
q3_price_area = df['Price per Area'].quantile(0.75)
iqr_price_area = q3_price_area - q1_price_area
upper_limit_price_area = q3_price_area + (iqr_price_area*1.5)
lower_limit_price_area = q1_price_area - (iqr_price_area*1.5)
df['Price per Area'] = np.where(df['Price per Area']>upper_limit_price_area, upper_limit_price_area, 
                                    np.where(df['Price per Area']<lower_limit_price_area, lower_limit_price_area, df['Price per Area']))
#Visualizing Price per Area After Capping
px.box(df, y = 'Price per Area', title='Price per Area After Capping')
#Visualizing Area After Capping
px.box(df, y = 'Area (m2)', title= 'Area After Capping')
#Showing Correlation of Capped Data
df_capped = df[['Price (in Million)', 'Area (m2)', 'Price per Area', 'Bedroom']]
corr_capped = df_capped.corr()
plt.title('Correlation After Capping')
heatmap_capped = sns.heatmap(corr_capped, vmin=-1, vmax=1, annot = True,cmap='BrBG')
#Removing outliers
df_cleaned = df[(df['Price (in Million)']<upper_limit_price) & (df['Price (in Million)']>lower_limit_price) & (df['Bedroom']<upper_limit_bedroom)
                & (df['Bedroom']>lower_limit_bedroom) & (df['Area (m2)']<upper_limit_area) & (df['Price (in Million)']>lower_limit_area) &
                (df['Price per Area']<upper_limit_price_area) & (df['Price per Area']>lower_limit_price_area)]
#Correlation of Removed Outliers
df_cleaned = df_cleaned[['Price (in Million)', 'Area (m2)', 'Price per Area', 'Bedroom']]
corr_cleaned = df_cleaned.corr()
plt.title('Correlation of Removed Outliers')
heatmap_cleaned = sns.heatmap(corr_cleaned, vmin=-1, vmax=1, annot = True,cmap='BrBG')
