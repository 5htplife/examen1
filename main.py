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
    def get_nutrition_obesity_by_gender():
        return pd.read_csv("https://github.com/5htplife/dataforexamen1/raw/main/nutrition_and_obesity_food_reg.csv")
    @st.cache(allow_output_mutation=True)
    def get_obesity_data():
        return pd.read_csv("https://github.com/5htplife/dataforexamen1/raw/main/Prevalence%20of%20obesity%20(%25%20of%20population%20ages%2018%2B).csv")
    @st.cache(allow_output_mutation=True)
    def get_nutrition_and_covid():
        return pd.read_csv("https://github.com/5htplife/dataforexamen1/raw/main/nutrition_and_covid.csv")
    @st.cache(allow_output_mutation=True)
    def get_macronutrition_and_obesity():
        return pd.read_csv("https://github.com/5htplife/dataforexamen1/raw/main/nutrition_and_obesity_macro.csv")
    @st.cache(allow_output_mutation=True)
    def get_obesity_dynamic():
        return pd.read_csv("")


    st.set_page_config(
        page_title="Food Habits, Obesity, and COVID-19",
        page_icon="🧊",
        layout="centered"
    )
    st.sidebar.markdown('''
    # Contents
    - [Analysis of Food Habits](#covid-situation-in-the-world)
    - [Obesity](#obesity-and-coronavirus)
    - [COVID-19](#obesity-and-food-habits)
    - [Micronutrients and COVID-19]
    ''', unsafe_allow_html=True)
    excess_mortality = get_excess_mortality()

    st.markdown('# Food Habits')
    st.write("Today more and more attention is brought to what people should eat for general health and longevity (see this [link](https://www.youtube.com/watch?v=n9IxomBusuw)).")
    st.write("A lot of renowned scientists urge people to consume more plant-based, less sugary food. Unfortunately, according to Gonzalez-Monroy (2021), food habits during COVID-19 changed drastically: people started opting for more starchy, high-carb foods rather than fiber-rich food such as fruit and vegetables. Such dietary patterns have been proven to worsen health in the long-run so people should be incentivised to reverse this trend. This project aims to offer an insight in aggregate food habits of people in 122 countries, link it to obesity, as well as provide some insights about COVID-19.")
    st.write("This project aims to offer insights about dietary habits to incentivize people maintain health. Also, we provide information about COVID-19 to see how the situation differs across countries. ")
    st.write("## Dietary Habits arounnd the World")
    st.write('We obtain data from Global Dietary Database where dietary patterns of 185 countries are listed. First, we offer insights in the consumption of certain types of food by country. It is interesting to learn what food types people prefer across the globe.')
    nutrition_percent = get_nutrition_percent()
    iso = get_iso()
    nutrition_percent = nutrition_percent.merge(iso, how='inner', left_on='iso3', right_on='iso3c')
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

    st.write(
        "Undoubtedly, nutrition patterns are linked to physical health and especially obesity levels across countries.")
    st.write("Let's look at the obesity levels at top-10 obesed countries")

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
    obesity_top10 = obesity.sort_values(by = 'Value', ascending = False)[:10]
    obesity_female = obesity_top10[obesity_top10['Indicator Name'] == 'Female']
    obesity_male = obesity_top10[obesity_top10['Indicator Name'] == 'Male']
    if gender_option == 'Female':
        fig_obesity = px.bar(obesity_female, y="Value", x="Country Name",
                                     hover_name="Country Name",
                                     text_auto='.2s%', title="Obesity rates among women in top-10 obesed countries")
        fig_obesity.update_traces(textfont_size=12, textangle=0
                                   , textposition="outside", cliponaxis=False)
        fig_obesity.update_yaxes(range=[0, 100], title = "Obesity Rate (%)")
        st.plotly_chart(fig_obesity, width=800, height=800)

    else:
        fig_obesity2 = px.bar(obesity_male, y="Value", x="Country Name",
                                     hover_name="Country Name",
                                     text_auto='.2s', title="Obesity rates among men in top-10 obesed countries")
        fig_obesity2.update_traces(textfont_size=12, textangle=0
                                   , textposition="outside", cliponaxis=False)
        fig_obesity2.update_yaxes(range=[0, 100], title = "Obesity Rate (%)")

        st.plotly_chart(fig_obesity2, width=800, height=800)

    st.write(
        "Obesity is a serious problem nowadays. From the plot above you can see that it wasn't as drastic even half a century ago.")
    st.write("The natural question that occurs is: what to eat to prevent obesity?")
    st.write(
        "This is the question that a lot of medical scientists are concerned wit, and our project certainly can't offer any certain answer to it. ")
    st.write(
        "Yet, what we can do is analyze food habits across countries and obesity rates. We have run the regression on obesity level and different food types.")
    st.write(
        "The results are presented below. You can notice that the adjusted R-squared is not very high, so there is a big part that remains unexplained. However, you can see the relationship between certain foods and obesity.")
    st.write("Important: no causal relationship is claimed, only correlation.")
    image = Image.open('regression.png')
    resized_image = image.resize((400, 400))
    st.image(image, caption='Regression Results Food & Obesity')
    st.write("We can have a closer look on the relationship between each food type and obesity.")
    nutrition_obesity = get_nutrition_obesity_by_gender()


    def function_for_food_plots(A):
        fig6, ax6 = plt.subplots()
        sns.regplot(data=nutrition_obesity, x='Value', y=A, color='blue', marker='*', ax=ax6)
        ax6.set(xlabel='Obesity (%)')
        ax6.set_title('Correlation between Obesity and The Chosen Food Type')
        return st.pyplot(fig6)


    list_of_products = ['Tea', 'Coffee', 'Fruit juices', 'Sugar-sweetened beverages',
                        'Yoghurt (including fermented milk)', 'Cheese', 'Eggs',
                        'Total seafoods', 'Unprocessed red meats', 'Total processed meats',
                        'Whole grains', 'Refined grains', 'nuts and seeds', 'beans and legumes',
                        'potatoes', 'non-starchy vegetables', 'fruits']
    food_options = st.selectbox("Choose a type of food you're interested in", list_of_products)
    for element in list_of_products:
        if food_options == element:
            function_for_food_plots(element)
            correlation_food = stats.pearsonr(nutrition_obesity[element], nutrition_obesity['Value'])[0]
            st.write('Correlation between obesity and this type of food is {:.2f}.'.format(correlation_food))

    st.write('Besides, it may be interesting to look at the relationship between macronutrients and obesity.')
    nutrition_macro = get_macronutrition_and_obesity()
    macronutrients = ['Added sugars', 'Dietary fiber', 'Dietary cholesterol', 'Plant omega-3 fat',
                      'Seafood omega-3 fat',
                      'Total omega-6 fat', 'Monounsaturated fatty acids', 'Saturated fat',
                      'Total protein', 'Total carbohydrates']
    st.write("The analysis below is performed based on female values around the world:")
    macro_option = st.selectbox("Choose a macronutrient", macronutrients)
    nutrition_macro_female = nutrition_macro[nutrition_macro['female'] == 1]
    for element in macronutrients:
        if macro_option == element:
            fig_macronutrient = px.scatter(nutrition_macro_female, x='Value', y=element,
                                           size=element, color='Country Name', hover_name="Country Name")
            fig_macronutrient.update_layout(
                title='Relationship between Obesity and Certain Macronutrient Intake for Women',
                xaxis=dict(
                    title='Obesity Rate (%)',
                    showgrid=False,
                ), yaxis=dict(title='Macronutrient Level', showgrid=False)
            )
            st.plotly_chart(fig_macronutrient, height=800, width=800)
    st.write("For men around the world:")
    macronutrients2 = ['Added sugars', 'Dietary fiber', 'Dietary cholesterol', 'Plant omega-3 fat',
                       'Seafood omega-3 fat',
                       'Total omega-6 fat', 'Monounsaturated fatty acids', 'Saturated fat',
                       'Total protein', 'Total carbohydrates']

    st.write('If you were interested in the average numbers around the world, then this information is for you:')
    st.write('On average, people consume {:.2f}'.format(nutrition_macro['Dietary Sodium'].mean()),
             'mg of dietary sodium per day.')
    st.write('People get {:.2f}'.format(nutrition_macro['Added sugars'].mean()),
             '% of total calorie intake by eating added sugars.')
    st.write('The average amount of dietary fiber is {:.2f}'.format(nutrition_macro['Dietary fiber'].mean()),
             'grams per day.')
    st.write('Usually people get {:.2f}'.format(nutrition_macro['Saturated fat'].mean()),
             '% of total daily calorie intake by consuming saturated fats.')
    st.write('At the same time, protein mean value is {:.2f}'.format(nutrition_macro['Total protein'].mean()),
             'grams per day.')
    st.write('Finally, on average we get {:.2f}'.format(nutrition_macro['Total carbohydrates'].mean()),
             'by eating carbs.')
    st.write("Let's compare these values with the values for top-10 cohorts with the highest obesity rate.")
    st.write(nutrition_macro.sort_values(by='Value', ascending=False)[:10].drop(columns=['female', 'Value']).mean())







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





    st.write("## Dietary Habits and COVID-19")

    st.write("The last step is to analyze whether there is any link with how people and the excess mortality in the country")
    st.write("Although regression analysis didn't produce any robust results, it is still worth looking at some data.")
    st.write("It is interesting to see how micronutrient distribution and excess mortality are related in different countries. During COVID outbreak many doctors advised patients to take supplements such as vitamin C, vitamin B12, vitamin D, and zinc. There is anecdotal evidence that these supplements help immune system during COVID.")
    st.write("That is why we present a scatterplot with micronutrient values and excess mortality in the world")
    micronutrients = ['Vitamin B9',
       'Vitamin B3', 'Vitamin B2', 'Zinc', 'Vitamin E',
       'Vitamin D', 'Vitamin C', 'Vitamin B12', 'Vitamin B6', 'Vitamin A',
       'Selenium', 'Potassium', 'Magnesium', 'Iron', 'Iodine', 'Calcium']
    supplement_option = st.selectbox("Choose a micronutrient", micronutrients)
    nutrition_and_covid = get_nutrition_and_covid()
    for element in micronutrients:
        if supplement_option == element:
            fig_nutrient_death = px.scatter(nutrition_and_covid, x = 'Excess deaths', y = element,
                                            size = element, color = 'Country', hover_name="Country", log_x = True)
            fig_nutrient_death.update_layout(title = 'Relationship between Excess Deaths and Micronutrient Levels in the World',
                                             xaxis=dict(
                                                 title='Excess deaths (log)',
                                                 showgrid = False, type = 'log'
                                             ), yaxis = dict(title='Micronutrient Level', showgrid = False)
                                             )
            st.plotly_chart(fig_nutrient_death, height = 800, width = 800)








