import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Bank Customer Churn Analytics",
    page_icon="🏦",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🏦 Bank Customer Churn Analytics")
st.write("Interactive analysis of customer engagement | product utilization | and high-value disengaged customers.")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

uploaded_file = st.sidebar.file_uploader(
    "Upload Bank Churn CSV",
    type=["csv"]
    
)

if uploaded_file is None:
    st.info("Please upload your Bank Churn CSV file from the sidebar.")
    st.stop()

data = pd.read_csv(uploaded_file)

st.sidebar.success("Dataset loaded successfully!")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Analysis Modules")

module = st.sidebar.selectbox(
    "Choose Analysis",
    [
        "Engagement vs Churn",
        "Product Utilization Impact",
        "High-Value Disengaged Customers"
    ]
)

# 
# CREATE ENGAGEMENT LEVEL


data["Engagement_Score"] = (
    data["IsActiveMember"] +
    (data["NumOfProducts"] >= 2).astype(int)
)

data["Engagement_Tier"] = data["Engagement_Score"].map({
    0: "Low Engagement",
    1: "Medium Engagement",
    2: "High Engagement"
})


# MODULE 1: ENGAGEMENT VS CHURN


if module == "Engagement vs Churn":

    st.header("📊 Engagement vs Churn")

    # Create engagement score
    data["Engagement_Score"] = (
        data["IsActiveMember"] +
        (data["NumOfProducts"] >= 2).astype(int)
    )

    # Create engagement tier
    data["Engagement_Tier"] = data["Engagement_Score"].map({
        0: "Low Engagement",
        1: "Medium Engagement",
        2: "High Engagement"
    })

    # Calculate churn
    threshold = (
        data.groupby("Engagement_Tier")["Exited"]
        .mean() * 100
    )

    # Keep correct order
    order = [
        "Low Engagement",
        "Medium Engagement",
        "High Engagement"
    ]

    threshold = threshold.reindex(order)

    # KPI cards
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Low Engagement Churn",
        f"{threshold['Low Engagement']:.1f}%"
    )

    col2.metric(
        "Medium Engagement Churn",
        f"{threshold['Medium Engagement']:.1f}%"
    )

    col3.metric(
        "High Engagement Churn",
        f"{threshold['High Engagement']:.1f}%"
    )

    # Chart
    st.subheader("Churn Rate by Engagement Level")

    fig, ax = plt.subplots()

    ax.bar(
        threshold.index,
        threshold.values
    )

    ax.set_ylabel("Churn Rate (%)")
    ax.set_xlabel("Engagement Level")
    ax.set_title("Engagement vs Churn")

    plt.xticks(rotation=15)

    st.pyplot(fig)

    # Threshold comparison
    low = threshold["Low Engagement"]
    medium = threshold["Medium Engagement"]
    high = threshold["High Engagement"]

    st.subheader("Retention Threshold")

    st.write(
        f"Low → Medium engagement reduces churn by "
        f"**{low - medium:.1f} percentage points**."
    )

    st.write(
        f"Medium → High engagement reduces churn by "
        f"**{medium - high:.1f} percentage points**."
    )

    st.success(
        "Medium engagement appears to be an important retention threshold."
    )



# MODULE 2: PRODUCT UTILIZATION


elif module == "Product Utilization Impact":

    st.header("📦 Product Utilization Impact Analysis")

    # Churn by number of products
    product_result = (
        data.groupby("NumOfProducts")["Exited"]
        .agg(["count", "sum", "mean"])
        .reset_index()
    )

    product_result.columns = [
        "Number of Products",
        "Customers",
        "Churned",
        "Churn Rate"
    ]

    product_result["Churn Rate"] = (
        product_result["Churn Rate"] * 100
    )

    # KPI
    st.metric(
        "Number of Product Categories",
        len(product_result)
    )

    # Table
    st.subheader("Product Utilization Summary")

    st.dataframe(
        product_result,
        use_container_width=True
    )

    # Chart
    st.subheader("Churn Rate by Number of Products")

    fig, ax = plt.subplots()

    ax.bar(
        product_result["Number of Products"],
        product_result["Churn Rate"]
    )

    ax.set_xlabel("Number of Products")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_title("Product Utilization vs Churn")

    st.pyplot(fig)

    # Find lowest and highest churn
    lowest = product_result.loc[
        product_result["Churn Rate"].idxmin()
    ]

    highest = product_result.loc[
        product_result["Churn Rate"].idxmax()
    ]

    st.subheader("Business Insight")

    st.write(
        f"Customers using **{int(highest['Number of Products'])} "
        f"product(s)** have the highest observed churn rate of "
        f"**{highest['Churn Rate']:.1f}%**."
    )

    st.write(
        f"Customers using **{int(lowest['Number of Products'])} "
        f"product(s)** have the lowest observed churn rate of "
        f"**{lowest['Churn Rate']:.1f}%**."
    )



# MODULE 3: HIGH-VALUE DISENGAGED CUSTOMERS


elif module == "High-Value Disengaged Customers":

    st.header("🚨 High-Value Disengaged Customer Detector")

    # Median thresholds
    median_balance = data["Balance"].median()
    median_salary = data["EstimatedSalary"].median()

    # Detect high-value disengaged customers
    high_value = data[
        (data["Balance"] >= median_balance) &
        (data["EstimatedSalary"] >= median_salary) &
        (data["Tenure"] >= 6) &
        (data["IsActiveMember"] == 0)
    ].copy()

    # KPIs
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "High-Value Disengaged",
        len(high_value)
    )

    col2.metric(
        "Average Balance",
        f"₹{high_value['Balance'].mean():,.0f}"
        if len(high_value) > 0
        else "₹0"
    )

    col3.metric(
        "Churn Rate",
        f"{high_value['Exited'].mean() * 100:.1f}%"
        if len(high_value) > 0
        else "0%"
    )

    # Customer table
    st.subheader("Detected Customers")

    if len(high_value) > 0:

        columns_to_show = [
            "Balance",
            "EstimatedSalary",
            "Tenure",
            "NumOfProducts",
            "IsActiveMember",
            "Exited"
        ]

        # Only show CustomerId if it exists
        if "CustomerId" in high_value.columns:
            columns_to_show.insert(0, "CustomerId")

        st.dataframe(
            high_value[columns_to_show],
            use_container_width=True
        )

        st.warning(
            "These customers have relatively high financial value "
            "but are currently inactive."
        )

    else:

        st.info(
            "No high-value disengaged customers were detected "
            "using the current thresholds."
        )
        
        
elif module == "Retention Strength Scoring":
    
    st.header("💪 Retention Strength Scoring")

    # Median balance
    median_balance = data["Balance"].median()

    # Create retention score
    data["Retention_Score"] = (
        (data["IsActiveMember"] == 1).astype(int)
        + (data["NumOfProducts"] >= 2).astype(int)
        + (data["Balance"] >= median_balance).astype(int)
        + (data["Tenure"] >= 6).astype(int)
    )

    # Create retention category
    data["Retention_Strength"] = data["Retention_Score"].map({
        0: "Weak",
        1: "Weak",
        2: "Moderate",
        3: "Moderate",
        4: "Strong"
    })

    # Score distribution
    score_result = data.groupby("Retention_Strength").agg(
        Customers=("Exited", "count"),
        Churned=("Exited", "sum")
    ).reset_index()

    score_result["Churn_Rate_%"] = (
        score_result["Churned"] /
        score_result["Customers"] * 100
    )

    st.subheader("Retention Strength Overview")

    st.dataframe(
        score_result,
        use_container_width=True
    )

    # KPIs
    strong = len(data[data["Retention_Strength"] == "Strong"])
    moderate = len(data[data["Retention_Strength"] == "Moderate"])
    weak = len(data[data["Retention_Strength"] == "Weak"])

    col1, col2, col3 = st.columns(3)

    col1.metric("🟢 Strong", strong)
    col2.metric("🟡 Moderate", moderate)
    col3.metric("🔴 Weak", weak)

    # Chart
    st.subheader("Churn Rate by Retention Strength")

    chart_data = score_result.set_index(
        "Retention_Strength"
    )["Churn_Rate_%"]

    st.bar_chart(chart_data)

    # Insight
    st.subheader("Business Insight")

    st.write(
        "Customers with stronger retention characteristics "
        "should generally have lower churn. Weak-retention "
        "customers can be prioritized for retention campaigns."
    )
    

# INTERACTIVE FILTERS


st.sidebar.header("🎛️ Customer Filters")


# 1. ENGAGEMENT FILTER


engagement_options = [
    "Low Engagement",
    "Medium Engagement",
    "High Engagement"
]

selected_engagement = st.sidebar.multiselect(
    "Engagement Level",
    engagement_options,
    default=engagement_options
)


# 2. PRODUCT COUNT SLIDER


min_product = int(data["NumOfProducts"].min())
max_product = int(data["NumOfProducts"].max())

selected_products = st.sidebar.slider(
    "Number of Products",
    min_value=min_product,
    max_value=max_product,
    value=(min_product, max_product)
)


# 3. BALANCE THRESHOLD


min_balance = float(data["Balance"].min())
max_balance = float(data["Balance"].max())

selected_balance = st.sidebar.slider(
    "Minimum Balance",
    min_value=min_balance,
    max_value=max_balance,
    value=min_balance,
    step=1000.0
)


# 4. SALARY THRESHOLD


min_salary = float(data["EstimatedSalary"].min())
max_salary = float(data["EstimatedSalary"].max())

selected_salary = st.sidebar.slider(
    "Minimum Salary",
    min_value=min_salary,
    max_value=max_salary,
    value=min_salary,
    step=1000.0
)


# APPLY ALL FILTERS


filtered_data = data[
    (data["Engagement_Tier"].isin(selected_engagement)) &
    (data["NumOfProducts"] >= selected_products[0]) &
    (data["NumOfProducts"] <= selected_products[1]) &
    (data["Balance"] >= selected_balance) &
    (data["EstimatedSalary"] >= selected_salary)
]

# ==========================================
# SHOW FILTERED DATA
# ==========================================

st.subheader("🔎 Filtered Customers")

st.write(
    f"Customers matching your filters: **{len(filtered_data):,}**"
)

st.dataframe(
    filtered_data,
    use_container_width=True
)


# KPI CALCULATIONS


# 1. Engagement Retention Ratio
active_churn = filtered_data[
    filtered_data["IsActiveMember"] == 1
]["Exited"].mean()

inactive_churn = filtered_data[
    filtered_data["IsActiveMember"] == 0
]["Exited"].mean()

if active_churn > 0:
    engagement_retention_ratio = inactive_churn / active_churn
else:
    engagement_retention_ratio = 0


# 2. Product Depth Index
retained_customers = filtered_data[
    filtered_data["Exited"] == 0
]

if len(retained_customers) > 0:
    product_depth_index = retained_customers[
        "NumOfProducts"
    ].mean()
else:
    product_depth_index = 0


# 3. High-Balance Disengagement Rate
median_balance = data["Balance"].median()

high_balance_inactive = filtered_data[
    (filtered_data["Balance"] >= median_balance) &
    (filtered_data["IsActiveMember"] == 0)
]

if len(high_balance_inactive) > 0:
    high_balance_disengagement_rate = (
        high_balance_inactive["Exited"].mean() * 100
    )
else:
    high_balance_disengagement_rate = 0


# 4. Credit Card Stickiness Score
credit_card_customers = filtered_data[
    filtered_data["HasCrCard"] == 1
]

if len(credit_card_customers) > 0:
    credit_card_stickiness = (
        credit_card_customers["Exited"].eq(0).mean() * 100
    )
else:
    credit_card_stickiness = 0


# 5. Relationship Strength Index
filtered_data["Relationship_Strength"] = (
    filtered_data["IsActiveMember"] +
    (filtered_data["NumOfProducts"] >= 2).astype(int)
)

relationship_strength_index = (
    filtered_data["Relationship_Strength"].mean()
)



# DISPLAY KPI CARDS


st.subheader("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Engagement Retention Ratio",
        f"{engagement_retention_ratio:.2f}×"
    )

with col2:
    st.metric(
        "Product Depth Index",
        f"{product_depth_index:.2f}"
    )

with col3:
    st.metric(
        "High-Balance Disengagement",
        f"{high_balance_disengagement_rate:.1f}%"
    )


col4, col5 = st.columns(2)

with col4:
    st.metric(
        "Credit Card Stickiness",
        f"{credit_card_stickiness:.1f}%"
    )

with col5:
    st.metric(
        "Relationship Strength Index",
        f"{relationship_strength_index:.2f} / 2"
    )



# FOOTER


st.sidebar.markdown("---")
st.sidebar.write("Bank Customer Churn Analytics")
st.sidebar.write("Built with Python + Streamlit")