import streamlit as st
import pandas as pd 
import os
import datetime



st.title(" 💰💸 Expense Tracker ")
st.caption("Track your daily spending easily 📊")

date = st.date_input("Select Date", datetime.date.today())


col1, col2 = st.columns(2)
with col1:    
    amount = st.number_input("Enter amount")

with col2:
    category = st.selectbox("Category", ["Food","Education", "Medicine","Travel", "Shopping","Hotel_Room","Others"])

if st.button(" ➕ Add Expense"):
    data = pd.DataFrame({
        "Date":[date.strftime("%Y-%m-%d")],
        "Amount": [amount],
        "Category": [category]
    })
    
    file_exists = os.path.isfile("expenses.csv")
    data.to_csv("expenses.csv", mode ='a', header = not file_exists, index = False)
    st.success("Expense Added.✅")
    
st.write("### Reset All Data 🔄 ")

    
confirm = st.checkbox("I am sure to delete all data", key = "confirm_reset")

if confirm:    
    if st.button("Start Fresh 🆕 "):
        if os.path.exists("expenses.csv"):
            os.remove("expenses.csv")
            st.success("All data cleared !  Start fresh ✅ ")
                       
        
st.divider()
st.subheader(" 📊 Dashboard.")
    
try:
    
    df = pd.read_csv("expenses.csv")
    
    st.write("### Your Expenses")
    st.dataframe(df)
    
    selected_row = st.selectbox("Select row to delete", df.index)

    if st.button("Delete Selected"):
        df = df.drop(selected_row)
        df.to_csv("expenses.csv", index=False)
        st.warning("Deleted!")
    
    
    st.write("### Edit Expense ✒️")
    
    selected_row = st.selectbox("Select row to edit", df.index)
    
    new_amount = st.number_input("New amount", key = "edit_amount")
    new_category = st.selectbox("New category", ["Food", "Travel", "Shopping","Hotel_Room","Others"], key = "edit_categoy")
    
    if st.button("Update Expense"):
        df.loc[selected_row, "Amount"] = new_amount
        df.loc[selected_row, "Category"] = new_category
    
        df.to_csv("expenses.csv", index=False)
        st.success("Expense updated successfully! ✅")
    
    st.write("### Total Spending 💸")
    st.success(f"Total: 💵 {df['Amount'].sum()}")
    
    total = df["Amount"].sum()
    st.metric(label = " Total Spending 💰", value = f"💸{total}")
    
    st.subheader("### Category-Wise Spending 📊")
    
    if not df.empty:
        category_data = df.groupby("Category")["Amount"].sum()
        st.bar_chart(category_data)
    else:
        st.write("No Data for chart")
        
    st.write ("### Monthly Spending 🗓️")
    
    df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d", errors = 'coerce')
    df = df.dropna(subset = ["Date"])
    
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    monthly_data = df.groupby("Month")["Amount"].sum()
    st.bar_chart(monthly_data)
    
    selected_category = st.selectbox("Filter by category", ["All"] + list(df["Category"].unique()))
    
    if selected_category != "All":
        filtered_df = df[df["Category"] == selected_category]
        st.dataframe(filtered_df)
    else:
        st.dataframe(df)    
except:
    st.write("No Data yet")
