import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import glob
import os
import plotly.express as px
from scipy import stats
import datetime


with st.echo(code_location="below"):
    @st.cache
    def get_kcal():
        return pd.read_csv("https://github.com/5htplife/firstproject/raw/master/Food_Supply_kcal_Data.csv")
    @st.cache
    def get_iso():
        return pd.read_csv("https://github.com/5htplife/firstproject/raw/master/continents2%202.csv")
    st.set_page_config(
        page_title="COVID-19, Obesity and Food Habits",
        page_icon="🧊",
        layout="centered"
    )
    st.sidebar.markdown('''
    # Contents
    - [COVID situation in the world](#covid-situation-in-the-world)
    - [Obesity and Coronavirus](#obesity-and-coronavirus)
    - [Obesity and Food Habits](#obesity-and-food-habits)
    - [Remark](#remark)
    ''', unsafe_allow_html=True)
    kcal = get_kcal()
    iso = get_iso().rename(columns={'name': 'Country'})
    iso_adj = iso.replace({'United States': 'United States of America'
                                ,'Congo (Democratic Republic Of The)': 'Congo', 'Russia': 'Russian Federation', 'Iran': 'Iran (Islamic Republic of)'
                                ,"Korea, Republic of": "Korea, North", "South Korea": "Korea, South", "Moldova": "Republic of Moldova"
                                ,"Macedonia": "North Macedonia",
                             'Venezuela': 'Venezuela (Bolivarian Republic of)'})
    kcal_adj = kcal.drop(["Unit (all except Population)", "Active"], axis = 1).dropna()#we don't need units and I drop "Active" because 1) I'm not planning to use this column 2) Also, "Active" column has some NAs for countries I want to keep, then I also drop all countries where we cannot estimate the values
    kcal_adj['Mortality'] = kcal_adj['Deaths']/kcal_adj['Confirmed'] #I find mortality as it is one of the main indicators of COVID situation in the country
    st.markdown('# COVID-19, Obesity and Food Habits')
    st.write("The coronavirus pandemic incentivized many people to reconsider their lifestyle habits, including their consumption habits.")
    st.write("This project aims to offer an insight in aggregate food habits of people in countries all over the globe.")
    st.write("## COVID situation in the world")
    st.write("The map shows COVID-19 situation in the world based on confirmed cases in the middle of 2021.")
    kcal_adj_merged=kcal_adj.merge(iso_adj, left_on='Country', right_on='Country', how="inner")
    fig_general=px.scatter_geo(kcal_adj_merged, locations='alpha-3', color='Country',
                         hover_name='Country', hover_data = ['Confirmed', 'Deaths', 'Population'], size='Confirmed', labels={'Confirmed': 'Confirmed Cases (%)', 'Deaths': 'Death Rate (%)', 'Mortality': 'Mortality Rate (%)'},
                         projection='natural earth', title='COVID-19 Situation In the World')
    st.plotly_chart(fig_general)
    kcal_adj['Mortality'] = kcal_adj['Deaths']/kcal_adj['Confirmed']
    covid_options = st.selectbox('What in particular would you like to see?', ['COVID Deaths', 'Confirmed Cases', 'COVID Mortality Rate'])
    if covid_options == 'COVID Mortality Rate':
        kcal_adj_sorted = kcal_adj.sort_values(by='Mortality', ascending=False)
        fig_bar_mortality = px.bar(kcal_adj_sorted, x='Country', y='Mortality', title='COVID Mortality by Country',
                                   labels={'Mortality': 'Mortality Rate (%)'}, height=400)
        st.plotly_chart(fig_bar_mortality)
    elif covid_options == 'Confirmed Cases':
        kcal_adj_sorted = kcal_adj.sort_values(by='Confirmed', ascending=False)
        fig_bar_confirmed = px.bar(kcal_adj_sorted, x='Country', y='Confirmed', hover_data=['Confirmed'],
                                   color='Confirmed',
                                   title='COVID Confirmed Cases by Country',
                                   labels={'Confirmed': 'Confirmed COVID-19 Cases (%)'})
        st.plotly_chart(fig_bar_confirmed)
    else:
        kcal_adj_sorted = kcal_adj.sort_values(by='Deaths', ascending=False)
        fig_bar_deaths = px.bar(kcal_adj_sorted, x='Country', y='Deaths', hover_data=['Deaths'], color='Deaths',
                                title='COVID Deaths by Country', labels={'Deaths': 'Death Rate (%)'})
        st.plotly_chart(fig_bar_deaths)
    st.write("## Obesity and Coronavirus")
    st.write("Let's look how obesity and COVID-19 are correlated around the globe")
    kcal_covid = kcal_adj[['Obesity','Deaths', 'Confirmed', 'Mortality']]
    obesity_covid_correlation_options = st.selectbox('How do you prefer to view correlation?', ['Heatmap, please', 'I prefer multiple plots'])
    if obesity_covid_correlation_options == 'I prefer multiple plots':
        fig1, ax1 = plt.subplots()
        sns.regplot(data=kcal_adj, x='Obesity', y='Deaths', color='darkolivegreen', marker='+', ax=ax1)
        ax1.set(xlabel='Obesity (%)', ylabel='Death Rate (%)')
        ax1.set_title('Correlation between Obesity and Death Rate')
        st.pyplot(fig1)
        fig2, ax2 = plt.subplots()
        sns.regplot(data=kcal_adj, x='Obesity', y='Confirmed', color='cadetblue', marker='2', ax=ax2)
        ax2.set(xlabel='Obesity (%)', ylabel='Confirmed Cases (%)')
        ax2.set_title('Correlation between Obesity and Confirmed Cases')
        st.pyplot(fig2)
        fig3, ax3 = plt.subplots()
        sns.regplot(data=kcal_adj, x='Obesity', y='Mortality', color='palevioletred', marker='x', ax=ax3)
        ax3.set(xlabel='Obesity (%)', ylabel='Mortality Rate (%)')
        ax3.set_title('Correlation between Obesity and Mortality Rate')
        st.pyplot(fig3)
    else:
        corr_covid = kcal_covid.corr(method='pearson')
        fig4, ax4 = plt.subplots()
        sns.heatmap(corr_covid, annot=True, cmap='cubehelix', linewidths=.5)
        ax4.set_title('Correlation Matrix for Obesity, Death Rate, Confirmed Cases, and Mortality Rate')
        st.pyplot(fig4)
    corr_obesity_death = stats.pearsonr(kcal_covid['Obesity'], kcal_covid['Deaths'])[0]
    corr_obesity_confirmed = stats.pearsonr(kcal_covid['Obesity'], kcal_covid['Confirmed'])[0]
    corr_obesity_mort = stats.pearsonr(kcal_covid['Obesity'], kcal_covid['Mortality'])[0]
    st.write('Correlation between obesity and deaths is {:.2f}.'.format(corr_obesity_death))
    st.write('Correlation between obesity and confirmed cases is {:.2f}.'.format(corr_obesity_confirmed))
    st.write('Surprisingly, correlation between is obesity and mortality is very low, {:.2f}.'.format(corr_obesity_mort))
    st.write('Notwithstanding the latter counterintuitive result, it is still very important to analyze the dietary habits so that we can protect ourselves from COVID-19 and other diseases')
    st.write('## Food Habits')
    st.write('You may want to see the dietary habits of particular countries.')
    countries = kcal_adj['Country']
    country_options = st.selectbox('Choose a country', countries)
    country = kcal_adj[kcal_adj['Country'] == country_options]
    country1 = country.drop(
        columns=['Country', 'Obesity', 'Undernourished', 'Confirmed', 'Deaths', 'Recovered', 'Population', 'Mortality',
                 'Animal Products', 'Miscellaneous', 'Oilcrops', 'Spices', 'Sugar Crops', 'Vegetal Products'])
    country2 = country1.columns
    country1 = country1.T
    country1.columns = ["food"]
    fig_nutrition_each_country = px.pie(country1, values='food', color='food', hover_name='food', names=country2,
                                        labels={'index': 'Type of Food', 'food': 'Per cent of Calorie Intake'},
                                        title='Food Habits in the Country')
    st.plotly_chart(fig_nutrition_each_country)
    st.write("It might be interesting to analyze dietary habits of countries with the highest and lowest obesity and COVID-19 death levels. So let's check it")
    meat_products = kcal_adj['Animal fats'] + kcal_adj['Meat'] + kcal_adj['Offals'] #I combine them because it's easier to assess this group together
    seafood = kcal_adj['Aquatic Products, Other'] + kcal_adj['Fish, Seafood'] #I do it for the same reason
    kcal_adj['Meat Products'] = meat_products
    kcal_adj['Fish and Seafood'] = seafood
    high_death_rate = (kcal_adj.sort_values('Deaths', ascending=False).head(10)
        .drop(columns=['Obesity', 'Undernourished', 'Confirmed', 'Deaths', 'Recovered', 'Population', 'Mortality', 'Animal Products', 'Miscellaneous', 'Oilcrops', 'Spices', 'Sugar Crops', 'Vegetal Products', 'Animal fats', 'Meat', 'Offals', 'Aquatic Products, Other', 'Fish, Seafood'])
                       )
    high_obesity_rate = (kcal_adj.sort_values('Obesity', ascending=False).head(10)
        .drop(columns=['Country', 'Obesity', 'Undernourished', 'Confirmed', 'Deaths', 'Recovered', 'Population', 'Mortality', 'Animal Products', 'Miscellaneous', 'Oilcrops', 'Spices', 'Sugar Crops', 'Vegetal Products', 'Animal fats', 'Meat', 'Offals', 'Aquatic Products, Other', 'Fish, Seafood'])
                         )
    low_death_rate = (kcal_adj.sort_values('Deaths', ascending=True).head(10)
        .drop(columns=['Country', 'Obesity', 'Undernourished', 'Confirmed', 'Deaths', 'Recovered', 'Population', 'Mortality', 'Animal Products', 'Miscellaneous', 'Oilcrops', 'Spices', 'Sugar Crops', 'Vegetal Products', 'Animal fats', 'Meat', 'Offals', 'Aquatic Products, Other', 'Fish, Seafood'])
                      )
    low_obesity_rate = (kcal_adj.sort_values('Obesity', ascending=True).head(10)
        .drop(columns=['Country', 'Obesity', 'Undernourished', 'Confirmed', 'Deaths', 'Recovered', 'Population', 'Mortality', 'Animal Products', 'Miscellaneous', 'Oilcrops', 'Spices', 'Sugar Crops', 'Vegetal Products', 'Animal fats', 'Meat', 'Offals', 'Aquatic Products, Other', 'Fish, Seafood'])
                        )

    def food_obesity_death(df):
        df1 = df.mean()
        df2 = df1.reset_index(level=0)
        df2.columns=["type of food", "per cent of intake"]
        high_deaths = alt.Chart(df2).mark_bar().encode(x=alt.X('per cent of intake', scale=alt.Scale(domain=[0,30])),
                                                                               y='type of food'
                                                       , color=alt.Color('type of food', scale=alt.Scale(scheme='Category20')))
        return st.altair_chart(high_deaths, use_container_width=True)
    st.write('In the following 4 plots I use the average intakes of different types of food in the corresponding groups of countries.')
    st.write('### Top-10 countries with the highest COVID death rate, Average Food Habits')
    food_obesity_death(high_death_rate)
    st.write('### Top-10 countries with the lowest COVID death rate,  Average Food Habits')
    food_obesity_death(low_death_rate)
    st.write("### Top-10 countries with the highest obesity rate,  Average Food Habits")
    food_obesity_death(high_obesity_rate)
    st.write('### Top-10 countries with the lowest obesity rate,  Average Food Habits')
    food_obesity_death(low_obesity_rate)
    st.write("It seems that in countries with the least death and obesity rates people consume more cereals, starchy roots and beans (perhaps, healthy carbs), and they consume much less of other types of food, including conventionally unhealthy ones: alcohol, sugar, meat, and dairy")
    st.write("## Obesity and Food Habits")
    st.write("The results we've seen are interesting, but in top-10 least obesed countries, there may be a high rate of undernourishment, as well.")
    st.write("Thus, I'll try to limit the effect of this factor by sampling only those countries where the undernourishment rate is below average.")
    st.write('Although it does not totally reduce the undernourishment effect, it certainly is more representative.')
    st.write("Also, I use a different type of plot because it may be interesting to analyse not the average numbers but each of top-10 obesed/least obesed country's consumption habits.")
    kcal_adj['Undernourished'] = kcal_adj['Undernourished'].replace('<2.5','2.5')
    kcal_adj['Undernourished'] = kcal_adj["Undernourished"].astype(float)
    kcal_adj_sorted_by_undernourished = kcal_adj[kcal_adj['Undernourished'] < kcal_adj['Undernourished'].mean()]
    high_obesity = (kcal_adj_sorted_by_undernourished.sort_values('Obesity', ascending=False).head(10)
        .drop(columns=['Obesity', 'Undernourished', 'Confirmed', 'Deaths', 'Recovered', 'Population', 'Mortality', "Vegetal Products",'Animal Products', 'Animal fats', 'Meat', 'Offals', 'Aquatic Products, Other', 'Fish, Seafood'])
                         ).replace({'United States of America': 'USA'}) #I get rid of Vegetal Products because they combine things listed in other food categories, thus, I don't need it (check description dataset if needed). Also, I change for USA for shorter width of y-label.
    low_obesity = (kcal_adj_sorted_by_undernourished.sort_values('Obesity', ascending=True).head(10)
        .drop(columns=['Obesity', 'Undernourished', 'Confirmed', 'Deaths', 'Recovered', 'Population', 'Mortality', 'Animal Products',"Vegetal Products", 'Animal fats', 'Meat', 'Offals', 'Aquatic Products, Other', 'Fish, Seafood'])
                         ) #I get rid of Vegetal Products because they combine things listed in other food categories, thus, I don't need it (check description dataset if needed)
    high_obesity_melted=high_obesity.melt(id_vars="Country", var_name="Food")
    high_obesity_melted["value"] = high_obesity_melted["value"] * 2 #I multiply because Vegetal Products (which I get rid of) constitute 50% of consumption
    low_obesity_melted = low_obesity.melt(id_vars="Country", var_name="Food")
    low_obesity_melted["value"] = low_obesity_melted["value"] * 2
    high_obesity_chart = alt.Chart(high_obesity_melted, title='Food Habits of top-10 Most Obesed countries').mark_bar().encode(
        x=alt.X('sum(value)',  title='Total Consumption by Categories (%)', scale=alt.Scale(domain=[0, 100])),
            y='Country',
                color=alt.Color('Food', scale=alt.Scale(scheme='category20'), legend=alt.Legend(title="Food Categories")),
                    order=alt.Order('Food', sort='ascending')).configure_title(fontSize=20)
    st.altair_chart(high_obesity_chart, use_container_width=True)
    low_obesity_chart = alt.Chart(low_obesity_melted, title='Food Habits of Top-10 Least Obesed Countries').mark_bar().encode(
        x=alt.X('sum(value)', title='Total Consumption by Categories (%)', scale=alt.Scale(domain=[0,100])),
            y='Country',
                color=alt.Color('Food', scale=alt.Scale(scheme = 'category20'), legend=alt.Legend(title="Food Categories")),
                    order=alt.Order('Food',sort='ascending')).configure_title(fontSize=20)
    st.altair_chart(low_obesity_chart, use_container_width=True)
    st.write('Still, I want to show the overview, so I will use the same type of plot as before for generalisation.')
    st.write('### Average Food Habits of top-10 Most Obesed countries')
    food_obesity_death(high_obesity)
    st.write("### Average Food Habits of top-10 Least Obesed countries")
    food_obesity_death(low_obesity)
    st.write("The general pattern remains the same: in the least obesed countries people consume much more cereals, starchy roots (both are healthy, complex carbs) and slightly more vegetables and fish, while consuming much less of other types of food compared to the most obesed countries.")
    st.write("Now I suggest we analyze correlation between different types of food and obesity")
    def function_for_food_plots(A):
        fig6, ax6 = plt.subplots()
        sns.regplot(data = kcal_adj_sorted_by_undernourished, x='Obesity', y=A, color='slateblue', marker='*', ax=ax6)
        ax6.set(xlabel='Obesity (%)')
        ax6.set_title('Correlation between Obesity and The Chosen Type of Food')
        return st.pyplot(fig6)
    list_of_products = ['Meat Products', 'Fish and Seafood', 'Alcoholic Beverages', 'Cereals - Excluding Beer', 'Eggs', 'Fruits - Excluding Wine', 'Milk - Excluding Butter', 'Pulses', 'Starchy Roots', 'Stimulants', 'Sugar & Sweeteners', 'Vegetables', 'Treenuts']
    food_options = st.selectbox("Choose a type of food you're interested in", list_of_products)
    for element in list_of_products:
        if food_options == element:
            function_for_food_plots(element)
            correlation_food = stats.pearsonr(kcal_adj_sorted_by_undernourished[element], kcal_adj_sorted_by_undernourished['Obesity'])[0]
            st.write('Correlation between obesity and this type of food is {:.2f}.'.format(correlation_food))
    st.write("Therefore, we can conclude that fish and seafood, cereals (сomplex carbs), beans (pulses) and vegetables positively affect person's health because there is a negative correlation between them and obesity.")
    st.write("## Remark")
    st.write("In the end, I would like to emphasize the importance of maintaining a healthy diet once again.")
    st.write("Obviously, obesity is linked to person's lifestyle: physical activity and food habits. While it is the truth universally acknowledged that unhealthy eating causes obesity, "
             "the whole issue concerning obesity may seem irrelevant and distant in the eye of the reader. Further, I'll try to persuade why this vision is erroneous.")
    @st.cache
    def get_obesity_data():
        return pd.read_csv("https://github.com/5htplife/firstproject/raw/master/obesity-cleaned.csv")
    obesity_data = get_obesity_data() #now we need to 'prettify' it a little bit
    obesity_data_adj = obesity_data[obesity_data['Obesity (%)'] != 'No data']
    obesity_data_adj = obesity_data_adj.replace({'Republic of Korea': 'Korea, South', "Democratic People's Republic of Korea": 'Korea, North', 'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom'
                                                    , 'Republic of North Macedonia':'North Macedonia', "Democratic Republic of the Congo": "Congo"
                                                 , 'Viet Nam': 'Vietnam', 'Bolivia (Plurinational State of)': 'Bolivia'})
    obesity_data_adj = obesity_data_adj.rename(columns={'Obesity (%)':'Obesity'})
    obesity_data_adj['Obesity (%)'] = obesity_data_adj['Obesity'].str.extract('(\d+\.\d)').astype(float) #use regex to extract per cent of obesed people
    obesity_data_adj = obesity_data_adj.drop(columns=['Obesity'])
    obesity_data_merged = obesity_data_adj.merge(iso_adj, left_on='Country', right_on='Country', how="inner")
    fig_obesity=px.choropleth(obesity_data_merged[obesity_data_merged['Sex'] == 'Both sexes'], locations='alpha-3', color='Obesity (%)',
                            range_color = (0, 28), hover_name ='Country', hover_data=['Obesity (%)', 'Year'], color_continuous_scale="YlOrRd", animation_frame="Year", projection='equirectangular',
                              animation_group='region', title='The Obesity Rate Around the Globe (1975-2016)', labels={'Obesity (%)': 'Obesity Rate (%)'})
    st.plotly_chart(fig_obesity)
    st.write('As you might notice, the developed world is getting more and more obesed (and Russia is not an exception). Obesity is dangerous because it can lead to serious diseases.')
    st.write()
    st.write('I want to analyze the gender patterns concerning obesity')
    obesity_data_mean = obesity_data_adj.groupby(['Year', 'Sex']).mean().reset_index(level='Sex').reset_index(level='Year')
    obesity_data_mean_adj = obesity_data_mean.drop(columns = obesity_data_mean.columns[2])
    fig8, ax8 = plt.subplots()
    sns.scatterplot(data=obesity_data_mean_adj, x='Year', y='Obesity (%)', hue = 'Sex',
                    palette="cubehelix",
                    style = 'Sex', markers=['o', '^', 'v'], ax=ax8)
    ax8.set(ylabel='Obesity Rate, Average (%)')
    ax8.legend(loc='center right', bbox_to_anchor=(1, .25), title=None)
    ax8.set_title('The Average Obesity Rate by Gender (1975-2016)')
    st.pyplot(fig8)
    st.write('This finding may contribute to the answer as to why women are more into dieting than men are.')
    st.write('Anyway, I hope this project was helpful and gave you some insights about health!')
    st.write('### An ounce of prevention is worth a pound of cure')