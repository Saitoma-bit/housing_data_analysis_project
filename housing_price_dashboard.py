#import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


#use config page
st.set_page_config(
    page_title="House Pricing Dashboard",
    page_icon="👨‍👩‍👧‍👦",
    layout="wide"
)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/cleaned_nigeria_housing_dataset.csv")
        return df
    except FileNotFoundError as e:
        st.warning(f"An error occured: {e}")

def create_sidebar_filters(df):
    st.subheader("Housing filters")

    Region = st.sidebar.multiselect(
         "Select State(s):", 
        options=df['Region Parent Name'].unique(), 
        default=df['Region Parent Name'].unique()
    )

    price = st.sidebar.multiselect(
        "Select Furnishing",
        options=df['Furnishing'].unique(),
        default=df['Furnishing'].unique()
    )
    boosting = st.sidebar.multiselect(
        'Selected Boost(s)',
        options=df['Is Boost'].unique(),
        default=df['Is Boost'].unique()
    ) 
    return Region, price, boosting

def filter_data(df, Region, price, boosting):
    filtered_df = df[df['Region Parent Name'].isin(Region) & df['Furnishing'].isin(price) & df['Is Boost'].isin(boosting)]
    return filtered_df

def display_metrics(filtered_df):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🏠Total House Listings", len(filtered_df))

    with col2:
        average_price = filtered_df['Price'].mean() if len(filtered_df) > 0 else 0
        if average_price >= 1_000_000:
            formatted_average = f"₦{int(average_price / 1_000_000)} M"
        elif average_price >= 1_000:
            formatted_average = f"₦{int(average_price / 1_000)} K"
        else:
            formatted_average = f"₦{int(average_price)}"

        st.metric("⛪Average Price", formatted_average )

     
    with col3:
        common_region = filtered_df['Region Parent Name'].mode()[0] if not filtered_df.empty else "N/A"
        st.metric("🏣Most Common Region", value=common_region)

    with col4:
        house_pct = (filtered_df['Furnishing'] == 'Furnished').sum() / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.metric("✔️ Furnished House Percentage", f"{house_pct:.1f}%")

    
def display_chart(filtered_df):
    if len(filtered_df) == 0:
      st.warning("No filter data to display. please adjust the data from the sidebar")
      return
    
    col1, col2 = st.columns(2)
    with col1:
       state_counts = filtered_df['Region Parent Name'].value_counts().reset_index()
       state_counts.columns = ['Region Parent Name', 'Listings']
       fig1 = px.bar(
       state_counts,
       x='Region Parent Name',
       y='Listings',
       title='Number of Listings per Region'
       )

       st.plotly_chart(fig1, width='stretch')

    with col2:
        avg_price_state = filtered_df.groupby('Region Parent Name')['Price'].mean().sort_values(ascending=False).reset_index()
        fig2 = px.bar(
        avg_price_state,
        x='Region Parent Name',
        y='Price',
        title='Average Property Price per Region'
        )
        st.plotly_chart(fig2, width='stretch')

    col3, col4 = st.columns(2)
    with col3:
        fig3 = px.histogram(filtered_df,
        x='Price',
        nbins=50,
        title='Distribution of Property Prices'
        )
        st.plotly_chart(fig3, width='stretch')

    with col4:
        fig4 = px.box(filtered_df,
        x='Bedrooms',
        y='Price',
        title='Property Price by Number of Bedrooms',
        labels={
        'Bedrooms':'Bedrooms',
        'Price':'Price (₦)'
        })
        st.plotly_chart(fig4, width='stretch')
        
    col5, col6 = st.columns(2)
    with col5:
        fig5 = px.scatter(
        filtered_df,
        x='Bedrooms',
        y='Price',
        title='Property Size vs Price'
        )
        st.plotly_chart(fig5, width='stretch')

    with col6:
        furnishing_counts = filtered_df['Furnishing'].value_counts().reset_index()
        furnishing_counts.columns = ['Furnishing', 'Count']
        fig6 = px.pie(
        furnishing_counts,
        names='Furnishing',
        values='Count',
        title='Furnishing Type Distribution'
        )
        st.plotly_chart(fig6, width='stretch')

    col7 = st.columns(1)[0]
    with col7:
        corr_df = filtered_df[['Price', 'Property Size', 'Bedrooms', 'Bathrooms']].corr()
        fig7 = ff.create_annotated_heatmap(
        z=corr_df.values,
        x=list(corr_df.columns),
        y=list(corr_df.index),
        annotation_text=round(corr_df, 2).values,
        showscale=True
        )
        fig7.update_layout(title='Correlation Heatmap')
        st.plotly_chart(fig7, width='stretch')

def display_table_data(filtered_df):
   if len(filtered_df) > 0:
      st.dataframe(filtered_df, width='stretch', height=300)
   else:
      st.warning("No employee data to display")










def main():
    #load dataset
    df = load_data()
    #sidebar
    Region, price, boosting = create_sidebar_filters(df)
    #filtered_data
    filtered_df = filter_data(df, Region, price, boosting)
    st.title("JIJI HOUSE PRICING DASHBOARD")
    st.markdown("---")
    #display metrics
    display_metrics(filtered_df)
    #display charts
    display_chart(filtered_df)
    #display_table_data
    st.markdown("---")
    display_table_data(filtered_df)


main()