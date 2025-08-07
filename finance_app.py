import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")

st.title("💰 Personal Finance Tracker")
st.markdown("Upload your monthly expense CSV file to track spending and visualize trends.")

# --- 1. File Upload ---
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=['Date'])

    st.success("File successfully uploaded!")
    st.write("📄 Sample Data:", df.head())

    # --- 2. Summary Stats ---
    st.subheader("📊 Expense Summary")
    total = df["Amount"].sum()
    st.metric(label="Total Expense", value=f"₹{total:,.2f}")

    category_summary = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    st.write("### Category-wise Summary")
    st.dataframe(category_summary)

    # --- 3. Pie Chart ---
    st.write("### 🥧 Expense Breakdown by Category")
    fig1, ax1 = plt.subplots()
    category_summary.plot.pie(autopct='%1.1f%%', ax=ax1)
    ax1.set_ylabel("")
    st.pyplot(fig1)

    # --- 4. Trend Line Chart ---
    st.write("### 📈 Daily Expense Trend")
    daily_expense = df.groupby("Date")["Amount"].sum()
    moving_avg = daily_expense.rolling(window=3).mean()

    fig2, ax2 = plt.subplots()
    daily_expense.plot(marker='o', label="Daily Expense", ax=ax2)
    moving_avg.plot(label="3-Day Moving Avg", ax=ax2, linestyle='--')
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Amount (₹)")
    ax2.set_title("Daily Spending with Trend")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

else:
    st.info("👈 Upload a CSV file to get started. Example format:")
    sample_data = {
        "Date": ["2025-07-01", "2025-07-01", "2025-07-02"],
        "Category": ["Groceries", "Rent", "Utilities"],
        "Amount": [1200, 10000, 1500],
        "Note": ["Bought veggies", "Monthly rent", "Electric bill"]
    }
    st.dataframe(pd.DataFrame(sample_data))
