# dashboard/app.py (Using Streamlit for quick dashboard)

import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Path to your log file
LOG_FILE = "../neuradrive_alerts.log"

def load_data():
    """Log file se data load aur parse karta hai."""
    try:
        data = pd.read_csv(LOG_FILE, sep=' ', header=None, names=['Timestamp_Date', 'Timestamp_Time', 'Type', 'Alert_Type', 'Message'])
        # Timestamp ko combine karna
        data['Timestamp'] = data['Timestamp_Date'].str.replace('[', '', regex=False) + ' ' + data['Timestamp_Time'].str.replace(']', '', regex=False)
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        
        # Latest alert nikalna
        latest_alert = data.iloc[-1]['Alert_Type'] if not data.empty else "None"
        
        return data, latest_alert
        
    except FileNotFoundError:
        return pd.DataFrame(), "Log file not found."
    except Exception as e:
        # Jab file half-written ho
        return pd.DataFrame(), f"Error reading log: {e}"

st.title("🚦 Neuradrive AI Driver Wellness Dashboard")

# Real-time data refresh (Har 2 seconds mein refresh)
col1, col2 = st.columns(2)
placeholder = st.empty()

while True:
    data, latest_alert = load_data()
    
    with placeholder.container():
        st.header("Driver State Summary")
        
        # Wellness Meter (Color coding)
        if "DROWSINESS" in latest_alert or "NO_FACE" in latest_alert:
            color = "red"
            emoji = "🔴"
        elif "DISTRACTION" in latest_alert:
            color = "orange"
            emoji = "🟠"
        else:
            color = "green"
            emoji = "🟢"

        st.markdown(f"**Latest Status:** <span style='color:{color}; font-size: 24px;'>{emoji} **{latest_alert}**</span>", unsafe_allow_html=True)
        
        st.subheader("Recent Alerts Log")
        if not data.empty:
            st.dataframe(data[['Timestamp', 'Alert_Type', 'Message']].tail(10)) # Last 10 alerts
        else:
            st.info("System is starting up or no alerts yet.")

    time.sleep(2) # Refresh every 2 seconds