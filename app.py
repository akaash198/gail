#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import altair as alt
from sklearn.decomposition import PCA
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
st.title("ANOMALY DETECTION")
data=st.file_uploader('upload a file',type="xlsx")
if data is not None:   
    df=pd.read_excel(data)
    st.write(df)
    
if data==True:
    st.df.head()
numerics = ["int16", "int32", "int64", "float16", "float32", "float64"]
def main():
    st.header("project Dataset explorer")
    st.sidebar.header("OPTIONS") 
    all_cols = df.columns.values
    numeric_cols = df.select_dtypes(include=numerics).columns.values
    obj_cols = df.select_dtypes(include=["object"]).columns.values

    if st.sidebar.checkbox("Data preview", True):
        st.subheader("Data preview")
        st.markdown(f"Shape of dataset : {df.shape[0]} rows, {df.shape[1]} columns")
        if st.checkbox("Data types"):
            st.dataframe(df.dtypes)
        if st.checkbox("Data Summary"):
            st.write(df.describe())
         

    if st.sidebar.checkbox("Pattern distribution", False):
        st.subheader("Plot numeric column distribution")
        with st.echo():
            col = st.selectbox("Choose a column to display", numeric_cols)
            n_bins = st.number_input("Max number of bins ?", 5, 100, 10)
            chart = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    alt.X(f"{col}:Q", bin=alt.Bin(maxbins=n_bins)), alt.Y("count()")
                )
            )
            st.altair_chart(chart)
        st.markdown("---")

    if st.sidebar.checkbox("Scatterplot", False):
        st.subheader("Scatterplot")
        selected_cols = st.multiselect("Choose 2 columns :", numeric_cols)
        if len(selected_cols) == 2:
            color_by = st.selectbox(
                "Color by column:", all_cols, index=len(all_cols) - 1
            )
            col1, col2 = selected_cols
            chart = (
                alt.Chart(df)
                .mark_circle(size=20)
                .encode(
                    alt.X(f"{col1}:Q"), alt.Y(f"{col2}:Q"), alt.Color(f"{color_by}")
                )
                .interactive()
            )
            st.altair_chart(chart)
        st.markdown("---")

  # seaborn plot
    if st.sidebar.checkbox("Correlation plot"):
        st.subheader("Correlation plot")
        cor = df.corr()
        mask = np.zeros_like(cor)
        mask[np.triu_indices_from(mask)] = True
        plt.figure(figsize=(12,10))
        with sns.axes_style("white"):
            st.write(sns.heatmap(cor,annot=True,linewidth=2,
            mask = mask,cmap="magma"))
            st.pyplot()
               # Pie plot
    if st.sidebar.checkbox("pie plot"):
        st.subheader("Pie plot")
        all_columns_names=df.columns.tolist()
        st.success("Generating A pie plot")
        st.write(df.iloc[:,-1].value_counts().plot.pie(autopct="%1.1f%%"))
        st.pyplot()
     
    if st.sidebar.checkbox("plot of value counts"):
        st.subheader("Groupby columns")
        st.text("value counts by target")
        all_columns_name=df.columns.tolist()
        primary_col=st.selectbox("primary columns to groupby",all_columns_name)
        selected_columns_name=st.multiselect("select columns to plot",all_columns_name)
        if st.button("plot"):
            st.text("Generate value plot")
            if selected_columns_name:
                vc_plot=df.groupby(primary_col)[selected_columns_name].count()
        else:
            vc_plot=df.iloc[:,-1].value_counts()
        st.write(vc_plot.plot(kind="bar"))
        st.pyplot()
                   # customizabe plot    
        if st.sidebar.checkbox("customizable plot", False):
            st.subheader("Deviation")
            columns_names=df.columns.tolist()
            type_of_plot=st.selectbox("select type of plot",["area","bar","line","hist","box","kde"])
            selected_columns_names=st.multiselect("select column to plot",columns_names)
            
            if st.button("Show plot"):
                st.success("Generating customizable plot of {} for {}".format(type_of_plot,selected_columns_names))
            
                if type_of_plot=='area':
                    cust_data=df[selected_columns_names]
                    st.area_chart(cust_data)
                elif type_of_plot=='bar':
                    cust_data=df[selected_columns_names]
                    st.bar_chart(cust_data)
                elif type_of_plot=='line':
                    cust_data=df[selected_columns_names]
                    st.line_chart(cust_data)  
                elif type_of_plot:
                    cust_plot=df[selected_columns_names].plot(kind=type_of_plot)
                    st.write(cust_plot)
                    st.pyplot()

            if st.sidebar.checkbox("Deviations"):
                st.subheader("Deviation plot")  
                for feature in ['time', 'measurement','control_mode']:
                    ax = plt.subplot()
                    st.write(sns.distplot(df[feature][df.binary_result == 1], bins=50, label='Anormal',kde_kws={'bw':0.02}))
                    st.write(sns.distplot(df[feature][df.binary_result == 0], bins=50, label='Normal',kde_kws={'bw':0.02}))
                    ax.set_xlabel('')
                    ax.set_title('histogram of feature: ' + str(feature))
                    plt.legend(loc='best')
                    st.pyplot()
                     
                    
                    
            def ztest(feature):
    
                mean = falsepositive[feature].mean()
                std = falsepositive[feature].std()
                zScore = (falsenegative[feature].mean() - mean) / (std/np.sqrt(sample_size))
                return zScore     
            
            columns= df.drop('binary_result', axis=1).columns
            falsepositive= df[df.binary_result==0]
            falsenegative= df[df.binary_result==1]
            sample_size=len(falsepositive)
            significant_features=["measurement"]
            setpoint=70

            for i in columns:
                z_value=ztest(i)
    
                if( abs(z_value) >= setpoint):    
                    st.write(i," is critical alarm")
                    significant_features.append(i)
                    
        st.subheader("Inliers & Outliers of Data")      
        significant_features.append('binary_result')
        y= df[significant_features]

        inliers = df[df.binary_result==0]
        ins = inliers.drop(['binary_result'], axis=1)

        outliers = df[df.binary_result==1]
        outs = outliers.drop(['binary_result'], axis=1)

        ins.shape, outs.shape
        
        def falsepositive_accuracy(values):
    
            tp=list(values).count(1)
            total=values.shape[0]
            accuracy=np.round(tp/total,4)
    
            return accuracy

        def falsenegative_accuracy(values):
    
            tn=list(values).count(-1)
            total=values.shape[0]
            accuracy=np.round(tn/total,4)
    
            return accuracy
    
   
        st.subheader("Accuracy score For Isolation forest")
        ISF = IsolationForest(random_state=42)
        ISF.fit(ins)

        falsepositive_isf = ISF.predict(ins)
        falsenegative_isf = ISF.predict(outs)

        in_accuracy_isf=falsepositive_accuracy(falsepositive_isf)
        out_accuracy_isf=falsenegative_accuracy(falsenegative_isf)
        st.write("Accuracy in Detecting falsepositive Alarm:", in_accuracy_isf)
        st.write("Accuracy in Detecting falsenegative Alarm:", out_accuracy_isf)
        
        
        
        st.subheader("Accuracy score For Local Outlier Factor")
        LOF = LocalOutlierFactor(novelty=True)
        LOF.fit(ins)

        falsepositive_lof = LOF.predict(ins)
        falsenegative_lof = LOF.predict(outs)

        in_accuracy_lof=falsepositive_accuracy(falsepositive_lof)
        out_accuracy_lof=falsenegative_accuracy(falsenegative_lof)
        st.write("Accuracy in Detecting falsepositive Alarm :", in_accuracy_lof)
        st.write("Accuracy in Detecting falsenegative Alarm:", out_accuracy_lof)
        
        
        if st.sidebar.checkbox("Alarm Report", False):
            st.subheader("classification of Alarm")
            fig, (ax1,ax2)= plt.subplots(1,2,figsize=[16,3])
            ax1.set_title("Accuracy of Isolation Forest",fontsize=20)
            st.write(sns.barplot(x=[in_accuracy_isf,out_accuracy_isf], 
            y=['falsepositive Alarm', 'falsenegative Alarm'],
            label="classifiers", 
            color="b", 
            ax=ax1))
            ax1.set(xlim=(0,1))

            ax2.set_title("Accuracy of Local Outlier Factor",fontsize=20)
            st.write(sns.barplot(x=[in_accuracy_lof,out_accuracy_lof], 
            y=['falsepositive Alarm', 'falsenegative Alarm'], 
            label="classifiers", 
            color="r", 
            ax=ax2))
            ax2.set(xlim=(0,1))
            st.pyplot()

        
                    
if __name__ == "__main__":
    main()


 

# In[ ]:




