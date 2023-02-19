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
from PIL import Image



with st.echo(code_location="below"):
    @st.cache(allow_output_mutation=True)
    def get_excess_mortality():
        return pd.read_csv("https://github.com/5htplife/dataforexamen1/raw/main/excess_mortality.csv")
    @st.cache(allow_output_mutation=True)
    def get_nutrition_percent():
        return pd.read_csv("https://github.com/5htplife/dataforexamen1/raw/main/nutrition_percent.csv")
    @st.cache(allow_output_mutation=True)
    def get_nutrition_total():
        return pd.read_csv("https://github.com/5htplife/dataforexamen1/raw/main/nutrition_total.csv")
    @st.cache(allow_output_mutation=True)
    def get_iso():
        return pd.read_csv("https://github.com/5htplife/dataforexamen1/raw/main/iso.csv")
    @st.cache(allow_output_mutation=True)
    def get_nutrition_by_gender():
        return pd.read_csv("")
    @st.cache(allow_output_mutation=True)
    def get_obesity_data():
        return pd.read_csv("https://github.com/5htplife/dataforexamen1/raw/main/Prevalence%20of%20obesity%20(%25%20of%20population%20ages%2018%2B).csv")

    st.set_page_config(
        page_title="COVID-19, Obesity and Food Habits",
        page_icon="🧊",
        layout="centered"
    )
    st.sidebar.markdown('''
    # Contents
    - [COVID-19 situation in the world](#covid-situation-in-the-world)
    - [Obesity and Coronavirus](#obesity-and-coronavirus)
    - [Obesity and Food Habits](#obesity-and-food-habits)
    - [Remark](#remark)
    ''', unsafe_allow_html=True)
    excess_mortality = get_excess_mortality()

    st.markdown('# COVID-19 and Food Habits')
    st.write("According to Gonzalez-Monroy (2021) food habits during COVID-19 changed drastically: people started opting for more starchy, high-carb foods rather than fiber-rich food such as fruit and vegetables. Such food patterns have been proven to worsen health in the long-run so people should be incentivised to reverse this trend. This project aims to offer an insight in aggregate food habits of people in 122 countries and link it to the COVID-19 situation in those countries.")
    st.write("The project consists of 3 parts: first, we are going to have a look at the COVID-19 situation in 122 countries; second, we will offer insights in food habits of people across the globe; third, we are going to look whether food habits and COVID are related.")
    st.write("## COVID situation in the world")
    st.write("COVID-19 started in the early 2020 and spread rapidly across the globe. We obtain information on the COVID-19 status in 170 countries relevant in the middle of 2021. The 2021 was the pinnacle of COVID-19 with Delta variant, the last potent mutation, peaking exactly in the middle of 2021.")
    st.write("The map shows excess mortality across 122 countries using data obtained by Karlinsky & Kobak (2021).")
    st.write("The countries that are singled out are the ones that have the largest number of excess deaths.")
    excess_mortality['size'] = excess_mortality['Excess deaths']
    excess_mortality.loc[excess_mortality['size'] < 0, 'size'] = 1
    fig_general = px.scatter_geo(excess_mortality, locations='iso3c', color='Country',
                         hover_name='Country',
                         hover_data=['Country', 'COVID-19 deaths', 'Excess deaths', 'Excess per 100k'], size='size',
                         projection='natural earth', title='COVID-19 Excess Mortality around the Globe')
    fig_general.update_layout(width=800,height=800)
    st.plotly_chart(fig_general, width=800,height=800)
    excess_mortality.sort_values(by=['Excess deaths'], ascending=False)
    st.write("Top-5 countries with the greatest number of excess deaths are the US, Russia, Brazil, Mexico, and Egypt.")
    st.write("In our further discussion, we will have a closer look at 3 countries among top-5: the US, Russia, and Mexico.")
    st.write("We can also have a look at other measures such as confirmed COVID-19 deaths, excess deaths per 100'000 people, and undercount ratio (the ratio between excess deaths and confirmed deaths).")
    st.write("Below, you can have a closer look at these measures.")
    covid_options = st.selectbox('Which data would you like to see?', ['COVID-19 Confirmed Deaths', 'Excess Deaths per 100k', 'Undercount Ratio'])
    if covid_options == 'COVID-19 Confirmed Deaths':
        excess_mortality_sorted = excess_mortality.sort_values(by='COVID-19 deaths', ascending=False)
        fig_bar_confirmed = px.bar(excess_mortality_sorted, x='Country', y='COVID-19 deaths', hover_data=['COVID-19 deaths'],
                                   color='COVID-19 deaths',
                                   title='COVID-19 Confirmed Deaths by Country',
                                   labels={'COVID-19 deaths': 'Confirmed COVID-19 Deaths'})
        fig_bar_confirmed.update_layout(width=800, height=800, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        st.plotly_chart(fig_bar_confirmed, width=800, height=600)
    elif covid_options == 'Excess Deaths per 100k':
        excess_mortality_sorted = excess_mortality.sort_values(by='Excess per 100k', ascending=False)
        fig_bar_per100 = px.bar(excess_mortality_sorted, x='Country', y='Excess per 100k',
                                   hover_data=['Excess per 100k'],
                                   color='Excess per 100k',
                                   title='COVID-19 Excess Deaths per 100k by Country',
                                   labels={'Excess per 100k': 'Excess Deaths per 100k'})
        fig_bar_per100.update_layout(width=800, height=800, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False) )
        st.plotly_chart(fig_bar_per100, width=800, height=600)
    else:
        excess_mortality_sorted = excess_mortality.sort_values(by='Undercount ratio', ascending=False)
        fig_bar_undercount = px.bar(excess_mortality_sorted, x='Country', y='Undercount ratio',
                                hover_data=['Undercount ratio'],
                                color='Undercount ratio',
                                title='Undercount ratio by Country',
                                labels={'Undercount ratio': 'Undercount ratio'})
        fig_bar_undercount.update_layout(width=800, height=800, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        st.plotly_chart(fig_bar_undercount, width=800, height=600)

    st.write("Interesting, although not surprising observation from the chart above is that the highest undercount ratio is in the less developed countries such as Tajikistan, Nicaragua, and Uzbekistan.")
    st.write("We will focus on excess deaths alone, as it is the most appropriate metric for the relationship we want to look at.")




    st.write("## Food Habits")

    st.write('We offer insights into dietary habits of people in various countries')
    nutrition_percent = get_nutrition_percent()
    iso = get_iso()
    nutrition_percent = nutrition_percent.merge(iso, how='inner', left_on = 'iso3', right_on = 'iso3c')
    countries = nutrition_percent['country_name'].astype(str)
    country_options = st.selectbox('Choose a country', countries)
    per_country_habits = nutrition_percent[nutrition_percent['country_name'] == country_options]
    country1 = per_country_habits.drop(
        columns=['Unnamed: 0_x', 'Unnamed: 0_y', 'Unnamed: 0.1', 'iso3', 'age', 'female', 'urban', 'edu',
       'year', 'Vitamin B9', 'Vitamin B3', 'Vitamin B2', 'Zinc',
       'Vitamin E', 'Vitamin D', 'Vitamin C', 'Vitamin B12', 'Vitamin B6',
       'Vitamin A', 'Selenium', 'Potassium', 'Magnesium', 'Iron', 'Iodine',
       'Dietary Sodium', 'Calcium', 'Added sugars', 'Dietary fiber',
       'Dietary cholesterol', 'Plant omega-3 fat', 'Seafood omega-3 fat',
       'Total omega-6 fat', 'Monounsaturated fatty acids', 'Saturated fat',
       'Total protein', 'Total carbohydrates', 'sum_food', 'country_name'])
    country2 = country1.columns
    country1 = country1.T
    country1.columns = ["food"]
    fig_nutrition_each_country = px.pie(country1, values='food', color='food', hover_name='food', names=country2,
                                        labels={'index': 'Type of Food', 'food': 'Per cent of Total Food Intake'},
                                        title='Food Habits in the Country')
    st.plotly_chart(fig_nutrition_each_country)

    st.write("### Obesity")

    st.write("Undoubtedly, nutrition patterns are linked to physical health and especially obesity levels across countries.")
    st.write("Let's look how obesity rates changed throughout the years in the world.")

    gender_option = st.selectbox('Choose gender:', ['Female', 'Male'])

    obesity = get_obesity_data()
    obesity['Indicator Name'] = np.where(
        (obesity['Indicator Name'] == 'Prevalence of obesity, female (% of female population ages 18+)'), 'Female',
        obesity['Indicator Name'])
    obesity['Indicator Name'] = np.where(
        (obesity['Indicator Name'] == 'Prevalence of obesity, male (% of male population ages 18+)'), 'Male',
        obesity['Indicator Name'])
    obesity = obesity.drop(columns=['Indicator Code', 'Disaggregation'])
    obesity = obesity[obesity['Country Name'] != 'World']
    obesity = obesity[obesity['Year'] == 2016]
    if gender_option == 'Female':
        obesity_female = obesity[obesity['Indicator Name'] == 'Female']
        fig_obesity = px.scatter_geo(obesity_female, locations="Country Code", color="Country Name",
                             hover_name="Country Name", size="Value",
                             projection="natural earth")
        st.plotly_chart(fig_obesity, width=800, height=800)
    else:
        obesity_male = obesity[obesity['Indicator Name'] == 'Male']
        fig_obesity = px.scatter_geo(obesity_male, locations="Country Code", color="Country Name",
                                     hover_name="Country Name", size="Value",
                                     projection="natural earth")
        st.plotly_chart(fig_obesity, width=800, height=800)

    st.write("Obesity is a serious problem nowadays. From the plot above you can see that it wasn't as drastic even half a century ago.")
    st.write("The natural question that occurs is: what to eat to prevent obesity?")
    st.write("This is the question that a lot of medical scientists are concerned wit, and our project certainly can't offer any certain answer to it. ")
    st.write("Yet, what we can do is analyze food habits across countries and obesity rates. We have run the regression on obesity level and different food types.")
    st.write("The results are presented below. You can notice that the adjusted R-squared is not very high, so there is a big part that remains unexplained. However, you can see the relationship between certain foods and obesity.")
    st.write("Important: no causal relationship is claimed, only correlation.")
    image = Image.open('https://github.com/5htplife/dataforexamen1/raw/main/obesity%20food%20reg.png')
    st.image(image, caption='Regression Results Food & Obesity')
    st.write("We can have a closer look on the relationship between each food type and obesity.")
    nutrition_gender = get_nutrition_gender()
    def function_for_food_plots(A):
        fig6, ax6 = plt.subplots()
        sns.regplot(data = , x='Obesity', y=A, color='slateblue', marker='*', ax=ax6)
        ax6.set(xlabel='Obesity (%)')
        ax6.set_title('Correlation between Obesity and The Chosen Type of Food')
        return st.pyplot(fig6)
    list_of_products = ['Meat Products', 'Fish and Seafood', 'Alcoholic Beverages', 'Cereals - Excluding Beer', 'Eggs', 'Fruits - Excluding Wine', 'Milk - Excluding Butter', 'Pulses', 'Starchy Roots', 'Stimulants', 'Sugar & Sweeteners', 'Vegetables', 'Treenuts']
    food_options = st.selectbox("Choose a type of food you're interested in", list_of_products)
    for element in list_of_products:
        if food_options == element:
            function_for_food_plots(element)
            correlation_food = stats.pearsonr([element], ['Obesity'])[0]
            st.write('Correlation between obesity and this type of food is {:.2f}.'.format(correlation_food))





    st.write("Also, it is interesting to learn about micronutrient distribution in different countries.")
    st.write("It is essential for further analysis of food habits and COVID-19 relationship because during COVID outbreak many doctors advised patients to take supplements such as vitamin C, vitamin B12, vitamin D, and zinc. There is anecdotal evidence that these supplements help immune system during COVID.")
    country_options2 = st.selectbox('Choose a country', countries)




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
            correlation_food = stats.pearsonr([element], ['Obesity'])[0]
            st.write('Correlation between obesity and this type of food is {:.2f}.'.format(correlation_food))
    st.write("Therefore, we can conclude that fish and seafood, cereals (сomplex carbs), beans (pulses) and vegetables positively affect person's health because there is a negative correlation between them and obesity.")





















    st.write("Let's look how obesity and COVID-19 rates are correlated around the globe")
    kcal_covid = kcal_adj[['Obesity','Deaths', 'Confirmed']]
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