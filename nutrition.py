import streamlit as st
import pandas as pd
import pymysql
from datetime import date
import matplotlib as plt
import seaborn as sns
import plotly.express as pltly
import requests
import plotly.graph_objects as pg

st.markdown("<h1 style='color:orange;'>NUTRITION PARADOX</h1>", unsafe_allow_html=True)

conn=pymysql.connect(host='127.0.0.1',user='root',passwd='Arahim4199',database='Nutrition_Paradox')
curs=conn.cursor()

with st.sidebar:
    tab=st.radio("Choose A Section",['Visualization','Obesity','Malnutrition','Combined'])
    
if tab== "Obesity":
    st.title ("Obesity Records")
    
    queries ={'1.Top 5 Regions with the highest average obesity levels in the most recent Year (2022)':
              '''select Region, avg(Mean_Estimate) as avg_obesity
              from Obesity
              where Year=2022
              group by Region
              order by avg_obesity desc
              limit 5''',
              '2.Top 5 countries with highest obesity estimates':
              '''select Country_Name, max(Mean_Estimate) as max_obesity
              from obesity
              group by Country_Name 
              order by max_obesity desc
              limit 5''',
              '3.Obesity trend in India over the Years':
              '''select Country_Name ,avg(Mean_Estimate) as avg_obesity
              from obesity
              where Country_Name = 'india'
              group by Year
              order by Year''',
              '4.Average obesity by Gender':
              '''select Gender, avg(Mean_Estimate) as avg_ob_lvl
              from Obesity
              group by Gender''',
              '5.Country_Name count by obesity level catepgry and age group':
              '''SELECT OBESITY_LEVEL,AgeGroup,COUNT(DISTINCT Country_Name) AS Country_Name_COUNT
              from  Obesity
              group by  OBESITY_LEVEL, AgeGroup
              order by OBESITY_LEVEL, AgeGroup;''',
              '6.Top 5 countries least reliable countries(with highest CI_Width) and Top 5 most consistent countries (smallest average CI_Width)':
              '''(SELECT Country_Name,AVG(CI_Width) AS Avg_CI_Width,'Most Consistent' AS Catepgry
              FROM  Obesity
              GROUP BY Country_Name
              ORDER BY  Avg_CI_Width ASC
              LIMIT 5
              )
              UNION ALL
              (
              SELECT Country_Name,AVG(CI_Width) AS Avg_CI_Width,'Least Reliable' AS Catepgry
              FROM Obesity
              GROUP BY Country_Name
              ORDER BY  Avg_CI_Width DESC
              LIMIT 5
              )''',
              '7.Average obesity by age group':
              '''select AgeGroup, avg(Mean_Estimate) as avg_obesity 
              from obesity 
              group by AgeGroup''',
              '8.Top 10 Countries with consistent low obesity (low average + low CI)over the Years':
              '''select Country_Name,avg(Mean_Estimate) as avg_obesity, avg(ci_width) as avg_ci
              from obesity
              group by Country_Name
              order by avg_obesity + avg_ci asc
              limit 10''',
              '9.Countries where female obesity exceeds male by large margin (same Year)':
              '''SELECT f.Country_Name,f.Year,f.Mean_Estimate AS Female_Obesity,
              m.Mean_Estimate AS Male_Obesity,(f.Mean_Estimate - m.Mean_Estimate) AS Difference
              FROM Obesity f
              JOIN Obesity m 
              ON f.Country_Name = m.Country_Name AND f.Year = m.Year AND f.AgeGroup = m.AgeGroup
              WHERE f.Gender = 'Female' AND m.Gender = 'Male' AND (f.Mean_Estimate - m.Mean_Estimate) > 10
              ORDER BY Difference DESC
              LIMIT 10;''',
              '10.Global average obesity percentage per Year':
              '''SELECT Year,AVG(Mean_Estimate) AS Global_Avg_Obesity
              FROM Obesity
              GROUP BY Year
              ORDER BY Year;''',
             }
    selected_query = st.selectbox("CHOOSE AN OPTION", list(queries.keys()),index=None,placeholder="SELECT A QUERY")
    
    if selected_query:
        query = queries[selected_query]
        try:
            df = pd.read_sql(query, conn)
            if 'Year' in df.columns:
                df['Year'] = df['Year'].astype(int)
            st.subheader(selected_query)
            st.dataframe(df)
            
        except Exception as e:
            st.error(f"Error running query: {e}")
elif tab=='Malnutrition':
    st.title("Malnutrition Records")
    query_mal={'1.Avg. malnutrition by age group':
               '''select AgeGroup, avg(Mean_Estimate) as avg_malnut
               from malnutrition
               group by AgeGroup''',
               '2.Top 5 countries with highest malnutrition(Mean_Estimate)':
               '''select Country_Name, max(Mean_Estimate) as max_malnut
               from malnutrition
               group by Country_Name
               order by max_malnut desc
               limit 5''',
               '3.Malnutrition trend in African Region over the Years':
               '''select Region,Year, avg(Mean_Estimate) as avg_malnut
                from malnutrition
                where Region = "africa"
                group by Year
                order by Year;''',
              '4.Gender-based average malnutrition':
               '''SELECT Gender, avg(Mean_Estimate) as avg_malnut
                from Malnutrition
                group by Gender
                order by avg_malnut desc''',
               '5.Malnutrition level-wise (average CI_Width by age group)':
               '''select  Malnutrition_LEVEL,AgeGroup,avg(ci_width) as avg_ci_level
                from Malnutrition
                group by Malnutrition_LEVEL,AgeGroup
                order by Malnutrition_LEVEL,avg_ci_level desc''',
               '6.Yearly malnutrition change in specific countries(India, Nigeria, Brazil)':
               '''SELECT Country_Name, Year, avg(Mean_Estimate) as avg_malnut
                from Malnutrition
                where Country_Name in ('india','nigeria','brazil')
                group by Country_Name,Year 
                order by Country_Name, Year;''',
               '7.Regions with lowest malnutrition averages':
               '''select Region, avg(Mean_Estimate) as avg_malnut
                from Malnutrition
                group by Region
                order by avg_malnut asc''',
              '8. Countries with increasing malnutrition':
               '''select Country_Name,max(Mean_Estimate) as max_malnut,min(Mean_Estimate) as min_malnut,
               (max(Mean_Estimate)-min(Mean_Estimate)) as increase_malnut
                from Malnutrition
                group by Country_Name
                having increase_malnut>0
                order by increase_malnut desc''',
               '9. Min/Max malnutrition levels Year-wise comparison':
               '''select Year,  min(Mean_Estimate) as min_malnut,max(Mean_Estimate) as max_malnut
                from malnutrition
                group by Year 
                order by Year asc''',
               '10.High CI_Width flags for monitoring(CI_width > 5)':
               '''select Country_Name,Year, ci_width
                from malnutrition
                where ci_width >5
                order by ci_width desc ''',
              }
    selected_query_mal = st.selectbox("CHOOSE AN OPTION", list(query_mal.keys()),index=None,placeholder="SELECT A QUERY")
    
    if selected_query_mal:
        query_malnut = query_mal[selected_query_mal]
        try:
            df = pd.read_sql(query_malnut, conn)
            if 'Year' in df.columns:
                df['Year'] = df['Year'].astype(int)
            st.subheader(selected_query_mal)
            st.dataframe(df)
            
        except Exception as e:
            st.error(f"Error running query: {e}")
elif tab=="Combined":
    st.title("Combined Records")
    query_com={'1.Obesity vs malnutrition comparison by Country_Name':
               '''select o.Country_Name, avg(o.Mean_Estimate) as avg_obesity, avg(m.Mean_Estimate) as avg_malnut
                from obesity o
                join malnutrition m on o.Country_Name = m.Country_Name
                group by o.Country_Name
                order by avg_obesity desc''',
               '2.Gender-based disparity in both obesity and malnutrition':
               '''select o.Country_Name, o.Gender, avg(o.Mean_Estimate) as avg_obesity, avg(m.Mean_Estimate) as avg_malnut
                from obesity o
                join malnutrition m on o.Gender=m.Gender and o.Year=m.Year and o.Country_Name= m.Country_Name
                group by o.Gender,o.Country_Name
                order by o.Gender,o.Country_Name''',
               '3.Region-wise avg estimates side-by-side(Africa and America)':
               '''select o.Region, avg(o.Mean_Estimate) as avg_obesity, avg(m.Mean_Estimate) as avg_malnut
                from obesity o
                join malnutrition m on o.Region = m.Region and o.Country_Name=m.Country_Name and o.Year=m.Year and o.Gender=m.Gender
                where o.Region in ('africa','americas')
                group by o.Region,o.Country_Name
                order by o.Region, o.Country_Name''',
               '4.Countries with obesity up & malnutrition down':
               '''select o.Country_Name, max(o.Mean_Estimate)-min(o.Mean_Estimate) as obesity_rise,
                max(m.Mean_Estimate)-min(m.Mean_Estimate) as malnut_down
                from obesity o
                join malnutrition m on o.Country_Name = m.Country_Name
                group by o.Country_Name
                order by o.Country_Name ''',
               '5.Age-wise trend analysis':
               '''select o.AgeGroup,o.Year,avg(o.Mean_Estimate) as avg_obesity, avg(m.Mean_Estimate) as avg_malnut
                from obesity o
                join Malnutrition m on o.AgeGroup=m.AgeGroup and o.Country_Name = m.Country_Name and o.Region=m.Region
                group by o.AgeGroup,o.Year
                order by o.AgeGroup,o.Year''',
              }
    selected_query_com = st.selectbox("CHOOSE AN OPTION", list(query_com.keys()),index=None,placeholder="SELECT A QUERY")
    
    if selected_query_com:
        query_combined = query_com[selected_query_com]
        try:
            df = pd.read_sql(query_combined, conn)
            if 'Year' in df.columns:
                df['Year'] = df['Year'].astype(int)
            st.subheader(selected_query_com)
            st.dataframe(df)
            
        except Exception as e:
            st.error(f"Error running query: {e}")

elif tab == "Visualization":
    st.title("📊 Visual Analytics Dashboard")

    url= "https://ghoapi.azureedge.net/api/NCD_BMI_30C"
    response = requests.get(url)
    data1= response.json()
    response
    data1.keys()
    df_ob_ad = pd.DataFrame(data1['value'])
    
    url= "https://ghoapi.azureedge.net/api/NCD_BMI_PLUS2C"
    response = requests.get(url)
    data2 = response.json()
    response
    data2.keys()
    df_ob_ch = pd.DataFrame(data2['value'])
    
    url = "https://ghoapi.azureedge.net/api/NCD_BMI_18C"
    response = requests.get(url)
    data3=response.json()
    response
    data3.keys()
    df_ml_ad = pd.DataFrame(data3['value'])
    
    url = "https://ghoapi.azureedge.net/api/NCD_BMI_MINUS2C"
    response = requests.get(url)
    data4=response.json()
    response
    data4.keys()
    df_ml_ch = pd.DataFrame(data4["value"])
    
    df_obese = pd.concat([df_ob_ad,df_ob_ch],ignore_index=True)
    df_malnut=pd.concat([df_ml_ad,df_ml_ch],ignore_index=True)

    df_malnut =df_malnut[(df_malnut['TimeDim']>=2012)&(df_malnut['TimeDim']<=2022)]
    df_obese=df_obese[(df_obese['TimeDim']>=2012)&(df_obese['TimeDim']<=2022)]

    df_obese.rename(columns={'ParentLocation' : 'Region','Dim1':'Gender','TimeDim':'Year','Low':'Lower_Bound','High':'Upper_bound',
                             'NumericValue':'Mean_Estimate','SpatialDim':'Country_Name'},inplace = True)
    df_obese['Gender']=df_obese['Gender'].replace({'SEX_MLE':'Male','SEX_FMLE':'Female','SEX_BTSX':'Both'})

    df_malnut.rename(columns={'ParentLocation' : 'Region','Dim1':'Gender','TimeDim':'Year','Low':'Lower_Bound','High':'Upper_bound',
                              'NumericValue':'Mean_Estimate','SpatialDim':'Country_Name'},inplace = True)
    df_malnut['Gender']=df_malnut['Gender'].replace({'SEX_MLE':'Male','SEX_FMLE':'Female','SEX_BTSX':'Both'})
    
    df_obese['Year'] = pd.to_numeric(df_obese['Year'], errors='coerce')
    df_plot = df_obese.dropna(subset=['Year', 'Mean_Estimate', 'Region'])
    
    fig1 = pltly.line(df_plot,
              x='Year',
              y='Mean_Estimate',
              color='Region',
              title='Obesity Trends Over Time by Region',
              markers=True,
              width =1000,height=500)

    st.plotly_chart(fig1, use_container_width=True)

    top_obese = (
            df_obese.groupby('Country_Name')['Mean_Estimate']
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
    top_malnut = (
            df_malnut.groupby('Country_Name')['Mean_Estimate']
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        
    col1,col2 =st.columns(2)
    with col1:
        fig2 = pltly.bar(
            top_obese,
            x='Country_Name',
            y='Mean_Estimate',
            title='Top 10 Countries by Average Obesity',
            labels={'Mean_Estimate': 'Average Obesity (%)'},
            color='Mean_Estimate',
            color_continuous_scale='Oranges',
            height=500,
            width=900
        )
        
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        fig3 = pltly.bar(
            top_malnut,
            x='Country_Name',
            y='Mean_Estimate',
            title='Top 10 Countries by Average Malnutrition',
            labels={'Mean_Estimate': 'Average Malnutrition (%)'},
            color='Mean_Estimate',
            color_continuous_scale='Blues',
            height=500,
            width=900
        )
        fig3.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig3, use_container_width=True)

    col3,col4 =st.columns(2)
    with col3:
        fig4 = pltly.box(
            df_obese,
            x='Region',
            y='Mean_Estimate',
            title='Obesity Estimate Variability by Region',
            color='Region',
            height=500,
            width=900
        )
    
        fig4.update_layout(xaxis_title='Region', yaxis_title='Obesity Estimate (%)')
        st.plotly_chart(fig4, use_container_width=True)

    with col4:
        fig5 = pltly.box(
            df_malnut,
            x='Region',
            y='Mean_Estimate',
            title='Malnutrition Estimate Variability by Region',
            color='Region',
            height=500,
            width=900
        )
    
        fig5.update_layout(xaxis_title='Region', yaxis_title='Malnutrition Estimate (%)')
        st.plotly_chart(fig5, use_container_width=True)

    heatmap_data = df_obese.pivot_table(index='Region', columns='Year', values='Mean_Estimate', aggfunc='mean')

    fig6 = pltly.imshow(
    heatmap_data,
    labels=dict(x="Year", y="Region", color="Avg Obesity"),
    x=heatmap_data.columns,
    y=heatmap_data.index,
    color_continuous_scale='OrRd',
    title='Obesity Heatmap by Region & Year',
    aspect='auto'
        )

    fig6.update_layout(height=600, width=900)
    st.plotly_chart(fig6, use_container_width=True)