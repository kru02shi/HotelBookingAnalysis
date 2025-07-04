import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Hotel Booking Dashboard", layout="wide")

df = pd.read_csv('data/hotel_bookings_cleaned.csv')
month_mapping = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}
df['arrival_month'] = df['arrival_date_month'].map(month_mapping)

st.title("Hotel Bookings Dashboard")

st.sidebar.header("Filter Bookings")
hotel_filter = st.sidebar.selectbox("Select Hotel Type", options=["All"] + df["hotel"].unique().tolist())
month_filter = st.sidebar.selectbox("Select Arrival Month", options=["All"] + sorted(df["arrival_month"].unique().tolist()))

filtered_df = df.copy()

if hotel_filter != "All":
    filtered_df = filtered_df[filtered_df["hotel"] == hotel_filter]
if month_filter != "All":
    filtered_df = filtered_df[filtered_df["arrival_month"] == month_filter]


total_bookings = len(filtered_df)
cancellation_rate = round(filtered_df["is_canceled"].mean() * 100, 2)
avg_lead_time = round(filtered_df["lead_time"].mean(), 1)

col1, col2, col3 = st.columns(3)
col1.metric("Total Bookings", total_bookings)
col2.metric("Cancellation Rate", f"{cancellation_rate}%")
col3.metric("Avg. Lead Time", avg_lead_time)

# Charts
st.subheader("Visualizations")

hotel_counts = filtered_df["hotel"].value_counts().reset_index()
hotel_counts.columns = ['hotel', 'count']
fig1 = px.bar(hotel_counts, x="hotel", y="count", 
              labels={"hotel": "Hotel", "count": "Total Bookings"},
              title="Total Bookings by Hotel Type", 
              color="hotel", 
              color_discrete_sequence=["#A04009", "#12149C"])

monthly_trends = filtered_df.groupby("arrival_month").size().reset_index(name="bookings")
fig2 = px.line(monthly_trends, x="arrival_month", y="bookings", title="Monthly Booking Trends", color_discrete_sequence=["#0A0C85"],
               labels={"arrival_month": "Month", "bookings": "Number of Bookings"})

cancel_data = {
    "Canceled": filtered_df["is_canceled"].sum(),
    "Not Canceled": len(filtered_df) - filtered_df["is_canceled"].sum()
}
fig3 = px.pie(names=cancel_data.keys(), values=cancel_data.values(), title="Cancellation Rate", color_discrete_sequence=["#0B90C5", "#129C4B"])

fig4 = px.histogram(filtered_df, x="lead_time", nbins=30, title="Lead Time Distribution", color_discrete_sequence=["#0C6A86"])

col_1, col_2 = st.columns(2)
with col_1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)
with col_2:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)