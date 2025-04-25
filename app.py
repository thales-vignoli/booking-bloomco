import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Set page configuration
st.set_page_config(page_title="BloomCo Booking Dashboard", layout="wide")

# Custom CSS for dark mode dashboard styling
st.markdown("""
    <style>
        /* General dashboard styling (dark mode) */
        body {
            background-color: #1a1a1a;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .stApp {
            background-color: #1a1a1a;
        }
        h1 {
            color: #ffffff;
            font-weight: 600;
            text-align: center;
            margin-bottom: 10px;
        }
        h3 {
            color: #ffffff;
            font-weight: 500;
            margin-top: 20px;
        }
        /* Top filter bar */
        .filter-bar {
            background-color: #2c2c2c;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            display: flex;
            gap: 20px;
            align-items: center;
            margin-bottom: 20px;
        }
        .filter-bar label {
            font-weight: 500;
            color: #d1d1d1;
        }
        /* Metric cards */
        .stMetric {
            background-color: #2c2c2c;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            text-align: center;
        }
        .stMetric label {
            color: #d1d1d1;
            font-size: 16px;
            font-weight: 500;
        }
        .stMetric value {
            color: #ffffff;
            font-size: 24px;
            font-weight: 600;
        }
        /* Plotly chart containers */
        .plotly-chart {
            background-color: #2c2c2c;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        /* Dataframe styling */
        .stDataFrame {
            background-color: #2c2c2c;
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        /* Dataframe text */
        .stDataFrame table {
            color: #d1d1d1;
        }
        /* Interesting fact section */
        .interesting-fact {
            background-color: #333333;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4a90e2;
            color: #d1d1d1;
        }
        /* Selectbox and date picker text */
        .stSelectbox, .stDateInput {
            color: #d1d1d1 !important;
        }
        .stSelectbox div[data-baseweb="select"] > div, .stDateInput div[data-baseweb="base-input"] > div {
            background-color: #2c2c2c !important;
            color: #d1d1d1 !important;
        }
        /* Ensure text in inputs is visible */
        input, select {
            color: #d1d1d1 !important;
            background-color: #2c2c2c !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("BloomCo Booking Dashboard")
st.markdown("Analyze booking trends, service popularity, and customer engagement for BloomCo.", unsafe_allow_html=True)

# Load data from Supabase
@st.cache_data
def load_data():
    try:
        response = supabase.table("Booking-BloomCo").select("*").execute()
        data = pd.DataFrame(response.data)
        data['created_at'] = pd.to_datetime(data['created_at'], errors='coerce')
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data['Answer'] = data['Answer'].map({'true': True, 'false': False, True: True, False: False})
        data['service'] = data['service'].fillna('Unknown')
        data['sentiment_analysis'] = data['sentiment_analysis'].fillna('Unknown')
        # Convert call_duration from seconds to minutes
        data['call_duration'] = pd.to_numeric(data['call_duration'], errors='coerce').fillna(0) / 60
        return data
    except Exception as e:
        st.error(f"Error fetching data from Supabase: {str(e)}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data available. Please check your Supabase connection or table.")
else:
    # Top horizontal filter bar
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    col_date, col_service = st.columns([2, 1])

    with col_date:
        date_range_input = st.date_input(
            "Select Date Range",
            [df['created_at'].min().date(), df['created_at'].max().date()],
            key="date_range"
        )

    with col_service:
        service_options = ['All'] + sorted(df['service'].unique().tolist())
        selected_service = st.selectbox("Select Service", service_options, key="service_filter")

    st.markdown('</div>', unsafe_allow_html=True)

    # Handle single date or date range
    if isinstance(date_range_input, (list, tuple)) and len(date_range_input) == 2:
        date_range = date_range_input
    else:
        # If a single date is selected, use it as both start and end date
        date_range = (date_range_input, date_range_input)

    # Filter data based on date range and service
    filtered_df = df[
        (df['created_at'].dt.date >= pd.to_datetime(date_range[0]).date()) &
        (df['created_at'].dt.date <= pd.to_datetime(date_range[1]).date())
    ]
    if selected_service != 'All':
        filtered_df = filtered_df[filtered_df['service'] == selected_service]

    # KPIs
    total_bookings = len(filtered_df)
    success_rate = (filtered_df['Answer'].sum() / len(filtered_df[filtered_df['Answer'].notna()]) * 100) if len(filtered_df[filtered_df['Answer'].notna()]) > 0 else 0
    unique_customers = filtered_df['email'].nunique()
    avg_call_duration = filtered_df['call_duration'].mean() if not filtered_df['call_duration'].empty else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Bookings", total_bookings)
    col2.metric("Success Rate", f"{success_rate:.1f}%")
    col3.metric("Unique Customers", unique_customers)
    col4.metric("Average Call Duration", f"{avg_call_duration:.1f} min")

    # Visualizations
    st.subheader("Service Popularity")
    service_counts = filtered_df['service'].value_counts().reset_index()
    service_counts.columns = ['Service', 'Count']
    fig_pie = px.pie(service_counts, names='Service', values='Count', title="Bookings by Service")
    fig_pie.update_layout(
        plot_bgcolor="#2c2c2c",
        paper_bgcolor="#2c2c2c",
        font=dict(color="#d1d1d1"),
        title_font_color="#ffffff",
        legend_font_color="#d1d1d1"
    )
    st.plotly_chart(fig_pie, use_container_width=True, theme=None)

    st.subheader("Booking Trends Over Time")
    daily_bookings = filtered_df.groupby(filtered_df['created_at'].dt.date).size().reset_index(name='Bookings')
    fig_line = px.line(daily_bookings, x='created_at', y='Bookings', title="Daily Booking Trends")
    fig_line.update_xaxes(title="Date", title_font_color="#d1d1d1", tickfont_color="#d1d1d1")
    fig_line.update_yaxes(title="Number of Bookings", title_font_color="#d1d1d1", tickfont_color="#d1d1d1")
    fig_line.update_layout(
        plot_bgcolor="#2c2c2c",
        paper_bgcolor="#2c2c2c",
        font=dict(color="#d1d1d1"),
        title_font_color="#ffffff"
    )
    st.plotly_chart(fig_line, use_container_width=True, theme=None)

    st.subheader("Top Customers by Booking Count")
    customer_bookings = filtered_df.groupby('name').size().reset_index(name='Bookings').sort_values('Bookings', ascending=False).head(5)
    fig_bar = px.bar(customer_bookings, x='name', y='Bookings', title="Top 5 Customers")
    fig_bar.update_xaxes(title="Customer Name", title_font_color="#d1d1d1", tickfont_color="#d1d1d1")
    fig_bar.update_yaxes(title="Number of Bookings", title_font_color="#d1d1d1", tickfont_color="#d1d1d1")
    fig_bar.update_layout(
        plot_bgcolor="#2c2c2c",
        paper_bgcolor="#2c2c2c",
        font=dict(color="#d1d1d1"),
        title_font_color="#ffffff"
    )
    st.plotly_chart(fig_bar, use_container_width=True, theme=None)

    # Sentiment Analysis Distribution (Positive vs Negative)
    st.subheader("Sentiment Analysis Distribution")
    sentiment_counts = filtered_df['sentiment_analysis'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    if sentiment_counts.empty or sentiment_counts['Count'].sum() == 0:
        st.warning("No sentiment analysis data available for the selected filters.")
    else:
        fig_sentiment = px.pie(sentiment_counts, names='Sentiment', values='Count', title="Sentiment Analysis: Positive vs Negative")
        fig_sentiment.update_layout(
            plot_bgcolor="#2c2c2c",
            paper_bgcolor="#2c2c2c",
            font=dict(color="#d1d1d1"),
            title_font_color="#ffffff",
            legend_font_color="#d1d1d1"
        )
        st.plotly_chart(fig_sentiment, use_container_width=True, theme=None)

    st.subheader("Failed Bookings")
    failed_bookings = filtered_df[filtered_df['Answer'] == False][['created_at', 'service', 'transcript']]
    st.dataframe(failed_bookings, use_container_width=True)

    # Interesting Fact
    st.subheader("Interesting Fact")
    if not service_counts.empty:
        most_popular_service = service_counts.iloc[0]['Service']
        most_popular_count = service_counts.iloc[0]['Count']
        st.markdown(
            f'<div class="interesting-fact">Did you know? <b>{most_popular_service}</b> is the most popular service with <b>{most_popular_count}</b> bookings, indicating strong demand for this offering!</div>',
            unsafe_allow_html=True
        )