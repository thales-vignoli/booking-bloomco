# BloomCo Booking Dashboard

## Overview
The **BloomCo Booking Dashboard** is a Streamlit-based web application designed to provide insights into booking trends, service popularity, customer engagement, and sentiment analysis for BloomCo. The dashboard retrieves data from a Supabase database and visualizes it using interactive Plotly charts. It features a dark-themed, user-friendly interface with filters for date ranges and services, key performance indicators (KPIs), and detailed visualizations.

## Features
- **Interactive Filters**: Select date ranges and specific services to filter data dynamically.
- **Key Metrics**: Displays total bookings, success rate, unique customers, and average call duration.
- **Visualizations**:
  - Pie chart for service popularity.
  - Line chart for daily booking trends.
  - Bar chart for top customers by booking count.
  - Pie chart for sentiment analysis (positive vs. negative).
- **Failed Bookings Table**: Lists details of unsuccessful bookings for further analysis.
- **Interesting Fact**: Highlights the most popular service based on booking data.
- **Dark Mode Styling**: Custom CSS for a modern, dark-themed dashboard.

## Tech Stack
- **Python**: Core programming language.
- **Streamlit**: Framework for building the web application.
- **Pandas**: Data manipulation and analysis.
- **Plotly**: Interactive data visualizations.
- **Supabase**: Cloud-based PostgreSQL database for data storage.
- **python-dotenv**: Environment variable management.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.8+ installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add your Supabase credentials:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

4. **Run the Application**:
   Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
   The dashboard will be accessible at `http://localhost:8501`.

## Project Structure
```
├── app.py                # Main Streamlit application script
├── .env                  # Environment variables (not tracked in git)
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
```

## Usage
1. **Access the Dashboard**: Open the app in your browser after running the Streamlit command.
2. **Filter Data**: Use the date range picker and service dropdown to filter bookings.
3. **Explore Visualizations**: Interact with charts to analyze booking trends, service popularity, and customer behavior.
4. **Review Failed Bookings**: Check the failed bookings table for insights into unsuccessful transactions.
5. **Monitor KPIs**: View real-time metrics like total bookings and success rate.

## Data Requirements
The dashboard expects a Supabase table named `Booking-BloomCo` with the following columns:
- `created_at`: Timestamp of booking creation.
- `date`: Booking date.
- `service`: Name of the service booked.
- `Answer`: Boolean indicating booking success (`true`/`false`).
- `email`: Customer email.
- `name`: Customer name.
- `call_duration`: Call duration in seconds.
- `sentiment_analysis`: Sentiment label (e.g., Positive, Negative).
- `transcript`: Transcript of the booking interaction.

Ensure the table is populated with data before running the dashboard.

## Troubleshooting
- **No Data Displayed**: Verify your Supabase URL and key in the `.env` file. Check if the `Booking-BloomCo` table exists and contains data.
- **Visualization Issues**: Ensure all dependencies (e.g., Plotly, Pandas) are installed correctly.
- **Styling Problems**: Clear the Streamlit cache (`streamlit cache clear`) if custom CSS does not render properly.
