import streamlit as st
import json
import pandas as pd
import plotly.express as px

# Load JSON data
with open("habit_report.json", "r") as f:
    data = json.load(f)

st.title("📊 Habit Completion Dashboard")

# Convert JSON → DataFrame
records = []
for user, habits in data.items():
    for habit, details in habits.items():
        if habit == "Number of days practiced":
            continue
        records.append({
            "User": user,
            "Habit": habit,
            "Days Completed": details["days_completed"],
            "Days Skipped": details["days_skipped"],
            "Success Rate": details["success_rate"]
        })

df = pd.DataFrame(records)

# Show table
st.subheader("Raw Data")
st.dataframe(df)

# Heatmap: Users vs Habits
st.subheader("Habit Completion Heatmap (Success Rate %)")

heatmap_data = df.pivot(index="User", columns="Habit", values="Success Rate")
fig = px.imshow(
    heatmap_data,
    text_auto=True,
    color_continuous_scale="RdYlGn",
    aspect="auto",
    title="Success Rate by User & Habit"
)
st.plotly_chart(fig, use_container_width=True)

# Optional: User Filter
st.subheader("📈 User-wise Habit Trends")
user_choice = st.selectbox("Select a user:", df["User"].unique())
user_df = df[df["User"] == user_choice]
fig2 = px.bar(
    user_df,
    x="Habit",
    y="Success Rate",
    color="Success Rate",
    color_continuous_scale="RdYlGn",
    title=f"Success Rate for {user_choice}"
)
st.plotly_chart(fig2, use_container_width=True)
