# ==========================================
# Singapore Job Market Intelligence Dashboard
# ==========================================
from pathlib import Path

# Import Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
#=====================================================

# ------------------------------------------
# Page Configuration
# ------------------------------------------
st.set_page_config(
    page_title="Singapore Job Market Data Product",
    page_icon="📊",
    layout="wide"
)

##### To change red tabs  fileters at the left to Blue#

st.markdown("""
<style>

/* Sidebar background */
section[data-testid="stSidebar"]{
    background-color:#102A43;
}

/* Sidebar labels */
section[data-testid="stSidebar"] label{
    color:white !important;
    font-size:17px;
    font-weight:bold;
}

/* Selected items (chips/tags) */
span[data-baseweb="tag"]{
    background-color:#2E86DE !important;
    color:white !important;
    border-radius:8px !important;
    font-weight:bold;
}

/* Hover effect */
span[data-baseweb="tag"]:hover{
    background-color:#1B4F72 !important;
}

</style>
""", unsafe_allow_html=True)






# ------------------------------------------
# Dashboard Title
# ------------------------------------------
st.title("📊 Singapore Job Market Intelligence Data Product")

st.markdown("""
This interactive dashboard analyzes **Singapore's job market** using over **1 million job postings**.

Use the filters on the left to explore salary trends, hiring demand, competition, and application insights across industries.

**Business Questions Answered**
1. Which industries pay the highest salaries?
2. Which industries have the greatest hiring demand?
3. Which industries receive the most applications?
4. Which industries are hardest to fill?
5. How has hiring changed over time?
""")

# ------------------------------------------
# Load Dataset
# ------------------------------------------
from pathlib import Path

@st.cache_data
def load_data():

    BASE_DIR = Path(__file__).parent

    csv_path = BASE_DIR / "SGJobs_Cleaned_01.csv"

    df = pd.read_csv(csv_path)

    df["metadata_originalPostingDate"] = pd.to_datetime(
        df["metadata_originalPostingDate"],
        errors="coerce"
    )

    return df

df = load_data()

# ------------------------------------------
# Sidebar Filters
# ------------------------------------------

st.sidebar.header("Dashboard Filters")

industry = st.sidebar.multiselect(
    "Select Industry",
    sorted(df["Industry"].dropna().unique()),
    default=sorted(df["Industry"].dropna().unique())
)

employment = st.sidebar.multiselect(
    "Employment Type",
    sorted(df["employmentTypes"].dropna().unique()),
    default=sorted(df["employmentTypes"].dropna().unique())
)

position = st.sidebar.multiselect(
    "Position Level",
    sorted(df["positionLevels"].dropna().unique()),
    default=sorted(df["positionLevels"].dropna().unique())
)

year = st.sidebar.multiselect(
    "Posting Year",
    sorted(df["PostingYear"].dropna().unique()),
    default=sorted(df["PostingYear"].dropna().unique())
)

# Apply Filters
filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["employmentTypes"].isin(employment)) &
    (df["positionLevels"].isin(position)) &
    (df["PostingYear"].isin(year))
]
#==============================================================

# =====================================================
# APPLY FILTERS
# =====================================================

if industry:
    df = df[df["Industry"].isin(industry)]

if employment:
    df = df[df["employmentTypes"].isin(employment)]

#----------------------------------------------
# =====================================================
# KPI SECTION
# =====================================================
st.markdown("""
<style>
.kpi-container {
    background-color: #EAF4FF;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #B3D9FF;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


st.markdown("---")
st.subheader("📊 Singapore Job Market Snapshot")

total_jobs = len(df)
avg_salary = df["average_salary"].fillna(0).mean()

total_companies = df["postedCompany_name"].nunique()

avg_competition = df["CompetitionIndex"].fillna(0).mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💼 Total Job Postings", f"{total_jobs:,}")

col2.metric("💰 Avg Monthly Salary", f"S${avg_salary:,.0f}")
col3.metric("🏢 Companies Hiring", f"{total_companies:,}")
col4.metric("📈 Competition Index", f"{avg_competition:.2f}")

# =====================================================
# Business Question 1:  TOP PAYING INDUSTRIES
# =====================================================

st.markdown("---")
st.subheader("💰 Business Question 1")
st.markdown("""
### Which industries offer the highest average salaries?

This visualization compares the **average monthly salary** across industries
to identify the highest-paying sectors in Singapore.
""")

salary_by_industry = (
    df.groupby("Industry")["average_salary"]
      .mean()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig = px.bar(
    salary_by_industry,
    x="average_salary",
    y="Industry",
    orientation="h",
    color="average_salary",
    color_continuous_scale="Blues",
    text="average_salary",
    title="Top 10 Industries by Average Monthly Salary"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(

    height=600,

    xaxis_title="Average Monthly Salary (SGD)",

    yaxis_title="Industry",

    yaxis=dict(categoryorder="total ascending"),

    title_x=0.15,

    margin=dict(l=20, r=20, t=60, b=20),

    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)

#Biz insights for Biz Question 1

highest = salary_by_industry.iloc[0]
second = salary_by_industry.iloc[1]
third = salary_by_industry.iloc[2]

st.markdown(f"""
<div style="
background-color:#184d2b;
padding:20px;
border-radius:10px;
border-left:6px solid #4CAF50;
">

<h3 style="color:#7CFC98;">📊 Business Insight</h3>

<p style="font-size:19px; color:white;">

The <b>{highest['Industry']}</b> industry offers the highest average monthly salary at approximately
<span style="font-size:24px; font-weight:bold; color:#FFD54F;">
S${highest['average_salary']:,.0f}
</span>

</p>

<p style="font-size:18px; color:white;">
The next highest-paying industries are
<b>{second['Industry']}</b>
(<span style="font-size:18px; font-weight:bold; color:#FFD54F;">
S${second['average_salary']:,.0f}
</span>)
and
<b>{third['Industry']}</b>
(<span style="font-size:18px; font-weight:bold; color:#FFD54F;">
S${third['average_salary']:,.0f}
</span>)

</div>
""", unsafe_allow_html=True)

#=================
# Biz Qn 2: Hiring Demand Analysis
#=================

st.markdown("---")
st.subheader("💼 Business Question 2")
st.markdown("""
### 2. Which industries have the greatest hiring demand?

This visualization compares the **number of job postings** across industries
to identify the sectors with the highest hiring activity in Singapore based on the number of job postings..
""")
st.subheader("💼 Hiring Demand by Industry")

# Hiring demand by industry
hiring_by_industry = (
    df.groupby("Industry")
      .size()
      .reset_index(name="JobCount")
      .sort_values("JobCount", ascending=False)
      .head(10)
)
fig = px.bar(
    hiring_by_industry,
    x="JobCount",
    y="Industry",
    orientation="h",
    text="JobCount",
    color="JobCount",
    color_continuous_scale="Blues",
    title="Top 10 Industries by Hiring Demand"
)

fig.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Number of Job Postings",
    yaxis_title="Industry",
    template="plotly_dark",
    height=600
)

fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)

#Biz insights for  biz Question 2

highest = hiring_by_industry.iloc[0]
second = hiring_by_industry.iloc[1]
third = hiring_by_industry.iloc[2]

st.markdown(f"""
<div style="
background-color:#184d2b;
padding:20px;
border-radius:10px;
border-left:6px solid #4CAF50;
">
<h3 style="color:#7CFC98;">📈 Business Insight</h3>
<p style="font-size:19px; color:white;">
The <b>{highest['Industry']}</b> industry has the highest hiring demand with
<span style="font-size:24px; font-weight:bold; color:#FFD54F;">
{highest['JobCount']:,}
</span>
job postings.
</p>
<p style="font-size:18px; color:white;">
It is followed by
<b>{second['Industry']}</b>
<span style="font-size:18px; font-weight:bold; color:#FFD54F;">
{second['JobCount']:,}
</span> jobs and
<b>{third['Industry']}</b>
<span style="font-size:18px; font-weight:bold; color:#FFD54F;">
{third['JobCount']:,}
</span> jobs.

</p>

</div>
""", unsafe_allow_html=True)

#============================
# Biz Question 3: Application Trends: Which industries receive the most applications?
#===========================

st.markdown("---")
st.subheader("📥 Business Question 3")
st.markdown("""
### 3. Which industries receive the most applications? """)

st.write(
    "This visualization compares the average number of applications received per job posting across industries."
)
st.subheader("Application Trend 📥")

#Prepare Data for Application Trend
application_by_industry = (
    df.groupby("Industry", as_index=False)["metadata_totalNumberJobApplication"]
      .mean()
      .sort_values("metadata_totalNumberJobApplication", ascending=False)
      .head(10)
)
fig = px.bar(
    application_by_industry,
    x="metadata_totalNumberJobApplication",
    y="Industry",
    orientation="h",
    color="metadata_totalNumberJobApplication",
    color_continuous_scale="Purples",
    text="metadata_totalNumberJobApplication",
    title="Top 10 Industries by Average Job Applications"
)

fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")

fig.update_layout(
    template="plotly_dark",
    height=600,
    coloraxis_showscale=False,
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Average Applications per Job",
    yaxis_title="Industry"
)

st.plotly_chart(fig, use_container_width=True)

# Biz Insights- Application Trend

highest = application_by_industry.iloc[0]
second = application_by_industry.iloc[1]
third = application_by_industry.iloc[2]

st.markdown(f"""
<div style="
background-color:#184d2b;
padding:20px;
border-radius:10px;
border-left:6px solid #4CAF50;
">
<h3 style="color:#7CFC98;">📈 Business Insight</h3>
<p style="font-size:19px; color:white;">
The <b>{highest['Industry']}</b> industry attracts the highest average number of job applications
<span style="font-size:24px; font-weight:bold; color:#FFD54F;">
{highest['metadata_totalNumberJobApplication']:.0f}
</span> indicating the strongest demand from job seekers.
</p>
<p style="font-size:18px; color:white;">
It is followed by
<b>{second['Industry']}</b>
<span style="font-size:18px; font-weight:bold; color:#FFD54F;">
{second['metadata_totalNumberJobApplication']:.0f}
</span> jobs and
<b>{third['Industry']}</b>
<span style="font-size:18px; font-weight:bold; color:#FFD54F;">
{third['metadata_totalNumberJobApplication']:.0f}
</span> jobs.

</p>

</div>
""", unsafe_allow_html=True)

#=============
# Biz Question 4: Competition Index: Which industries are hardest to fill?
#=============

st.markdown("---")
st.subheader("🔍 Business Question 4")
st.markdown("""
### 4. Which industries are hardest to fill?
""")

st.write(
    "This visualization compares the competition index across industries to identify the most challenging sectors to hire in."
)
st.subheader("Competition Index 🔍")

#Data Preparation for Competition Index
competition = (
    df.groupby("Industry", as_index=False)["CompetitionIndex"]
      .mean()
      .sort_values("CompetitionIndex", ascending=False)
      .head(10)
)

fig = px.bar(
    competition,
    x="CompetitionIndex",
    y="Industry",
    orientation="h",
    color="CompetitionIndex",
    color_continuous_scale="Reds",
    text="CompetitionIndex",
    title="Top 10 Most Competitive Industries"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_dark",
    height=600,
    coloraxis_showscale=False,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig, use_container_width=True)


# Biz Insights- Competition Index

highest = competition.iloc[0]
second = competition.iloc[1]
third = competition.iloc[2]

st.markdown(f"""
<div style="
background-color:#184d2b;
padding:20px;
border-radius:10px;
border-left:6px solid #4CAF50;
">
<h3 style="color:#7CFC98;">📈 Business Insight</h3>
<p style="font-size:19px; color:white;">
The <b>{highest['Industry']}</b> industry has the highest competition index  
<span style="font-size:24px; font-weight:bold; color:#FFD54F;">
{highest['CompetitionIndex']:.2f}
</span> indicating that each vacancy receives comparatively more applications than other industries.
</p>
<p style="font-size:18px; color:white;">
It is followed by
<b>{second['Industry']}</b>
<span style="font-size:18px; font-weight:bold; color:#FFD54F;">
{second['CompetitionIndex']:.2f}
</span> and
<b>{third['Industry']}</b>
<span style="font-size:18px; font-weight:bold; color:#FFD54F;">
{third['CompetitionIndex']:.2f}
</span> jobs.

</p>

</div>
""", unsafe_allow_html=True)

#=============
# Biz Question 5: Hiring Trend: How has hiring changed over time?
#=============

st.markdown("---")
st.subheader("🔍 Business Question 5")
st.markdown("""
### 5. How has hiring changed over time?
""")

st.write(
    "This visualization checks the hiring trend over time."
)
st.subheader("Hiring Trend 🔍")

#Data Preparation for Hiring Trend

# Create YearMonth for trend analysis
# Create YearMonth
df["YearMonth"] = (
    pd.to_datetime(df["metadata_originalPostingDate"])
      .dt.to_period("M")
      .astype(str)
)

# Monthly hiring trend
hiring_trend = (
    df.groupby("YearMonth")
      .size()
      .reset_index(name="Jobs")
)

fig = px.line(
    hiring_trend,
    x="YearMonth",
    y="Jobs",
    markers=True,
    title="Hiring Trend"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Number of Job Postings"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="trend_chart"
)
fig.update_traces(
    line=dict(color="#00B4D8", width=4),
    marker=dict(size=8)
)
# Biz Insights- Hiring Trend

highest = hiring_trend.sort_values("Jobs", ascending=False).iloc[0]
second = hiring_trend.sort_values("Jobs", ascending=False).iloc[1]
third = hiring_trend.sort_values("Jobs", ascending=False).iloc[2]

st.markdown(f"""
<div style="
background-color:#184d2b;
padding:20px;
border-radius:10px;
border-left:6px solid #4CAF50;
">

<h3 style="color:#7CFC98;">📈 Business Insight</h3>

<p style="font-size:19px; color:white;">
Hiring activity <b>peaked in {highest['YearMonth']}</b> with
<span style="font-size:24px; font-weight:bold; color:#FFD54F;">
{highest['Jobs']:,}
</span>
job postings.
</p>

<p style="font-size:18px; color:white;">
The next strongest hiring months were
<b>{second['YearMonth']}</b>
(<span style="color:#FFD54F;">{second['Jobs']:,}</span>)
and
<b>{third['YearMonth']}</b>
(<span style="color:#FFD54F;">{third['Jobs']:,}</span>),
indicating sustained recruitment demand during this period.
</p>

</div>
""", unsafe_allow_html=True)


##### Conclusion ###
st.markdown("""
<div style="
background-color:#153B73;
padding:25px;
border-radius:10px;
border-left:8px solid #5DADE2;
">

<h2 style="color:#A9D6FF; font-size:34px;">
📌 Key Business Conclusions:
</h2>

<div style="font-size:24px; color:white; line-height:2.0;">
💰<b>Legal, Risk Management and Banking & Finance</b> offer the highest average monthly salaries.
</div>

<div style="font-size:24px; color:white; line-height:2.0; margin-top:15px;">
💼 Hiring demand remains strong across key industries, with sustained recruitment activity over time.
</div>

<div style="font-size:24px; color:white; line-height:2.0; margin-top:15px;">
📥Competition differs significantly across industries, indicating varying levels of job seeker interest.
</div>

<div style="font-size:24px; color:white; line-height:2.0; margin-top:15px;">
🔍This dashboard enables interactive exploration of salary, hiring demand, competition, and employment patterns to support informed career and business decisions.
</div>

</div>
""", unsafe_allow_html=True)