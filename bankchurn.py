import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

data =pd.read_csv('European_Bank.csv')

#validate the data
# print(data.head())
print(data.shape)
print(data.isnull().sum())
data.dropna(inplace=True, axis=0)
data.drop_duplicates(inplace=True)
data['Exited'] = data['Exited'].astype('int')

#ensure the binary variable consistency
binarycolomn  =['HasCrCard','IsActiveMember','Exited']
for col in binarycolomn:
    print(col ,data[col].unique()) 
    
# churn level accuracy

# data['Exited'] = data['Exited'].unique()
print("The number of people exited =",data['Exited'].value_counts()[0])
print("The number of people not exited =",data['Exited'].value_counts()[1])

#engangement classification

print("--"*35, "Engangement Classification","--"*35)
print("__"*35, "Active customer","__"*35)
# active and inactive customer
enganged_customer = data['IsActiveMember'].value_counts()[1]
print("Active enganged customer are :",enganged_customer)

unenganged_customer = data['IsActiveMember'].value_counts()[0]
print("Inactive unenganged customer are :",unenganged_customer)
# active but low product customer
count_low_active = data.groupby(['IsActiveMember'])['NumOfProducts'].value_counts()[0,1]
print("The number of active of low product customer : ",count_low_active)

# Inactive high balance customer

count_high_inactive = data[data['Balance']>=1000].groupby(['IsActiveMember']).size()[1]
print("The number of inactive of high Balance customer: ",count_high_inactive)

#Product utilization analysis
print("--"*35,"Product utilization","--"*35)
churn_rate =data['Exited'].mean()*100
print("Churn rate:",int(churn_rate),"%")

#  Churn rate by number of products
cr_pd =data.groupby(['NumOfProducts'])['Exited'].mean()*100
print(cr_pd)

print("--"*35,"","--"*35)

# Single-product vs multi-product retention
total_customers = len(data)
single_product_customers = (data['NumOfProducts'] == 1).sum()
multi_product_customers = (data['NumOfProducts'] > 1).sum()
single_product_retention = data[data['NumOfProducts'] == 1]['Exited'].eq(0).mean() * 100
multi_product_retention = data[data['NumOfProducts'] > 1]['Exited'].eq(0).mean() * 100

print("Total customers:", total_customers)
print("Single-product customers:", single_product_customers)
print("Multi-product customers:", multi_product_customers)
print("Single-product retention:", round(single_product_retention, 2), "%")
print("Multi-product retention:", round(multi_product_retention, 2), "%")

product_dept=data.groupby('NumOfProducts')['Exited'].agg(['count', 'sum', 'mean'])
print(product_dept)
# Financial Commitment vs Engagement Analysis
# Create Low / High Balance groups using median
print("--"*35,"Blanace vs Cross analysis","--"*35)

median_balance = data["Balance"].median()

data["Balance_Group"] = data["Balance"].apply(
    lambda x: "High Balance" if x >= median_balance else "Low Balance"
)

# Convert activity into readable names
data["Activity"] = data["IsActiveMember"].map({
    0: "Inactive",
    1: "Active"
})

# Cross-analysis
result = data.groupby(
    ["Balance_Group", "Activity"]
).agg(
    Customers=("Exited", "count"),
    Churned=("Exited", "sum"),
    Avg_Balance=("Balance", "mean")
).reset_index()

# Calculate churn rate
result["Churn_Rate_%"] = (
    result["Churned"] / result["Customers"] * 100
)

print(result)

print("--"*35,"Salary–balance mismatch detection","--"*35)
# Find median salary and balance
median_salary = data["EstimatedSalary"].median()
median_balance = data["Balance"].median()

# Create salary group
data["Salary_Group"] = data["EstimatedSalary"].apply(
    lambda x: "High Salary" if x >= median_salary else "Low Salary"
)

# Create balance group
data["Balance_Group"] = data["Balance"].apply(
    lambda x: "High Balance" if x >= median_balance else "Low Balance"
)

# Create mismatch category
data["Mismatch"] = data.apply(
    lambda row:
        "High Salary - Low Balance"
        if row["Salary_Group"] == "High Salary"
        and row["Balance_Group"] == "Low Balance"
        else
        "Low Salary - High Balance"
        if row["Salary_Group"] == "Low Salary"
        and row["Balance_Group"] == "High Balance"
        else
        "Normal",
    axis=1
)

# Analyze each group
result = data.groupby("Mismatch").agg(
    Customers=("Exited", "count"),
    Churned=("Exited", "sum"),
    Avg_Salary=("EstimatedSalary", "mean"),
    Avg_Balance=("Balance", "mean")
).reset_index()

# Calculate churn rate
result["Churn_Rate_%"] = (
    result["Churned"] / result["Customers"] * 100
)

print(result)

print("--"*35,"Identification of “at-risk premium customers","--"*35)
# Median values
median_balance = data["Balance"].median()
median_salary = data["EstimatedSalary"].median()

# Create premium customer conditions
data["Premium_Customer"] = (
    (data["Balance"] >= median_balance) &
    (data["EstimatedSalary"] >= median_salary) &
    (data["Tenure"] >= 6) &
    (data["NumOfProducts"] >= 2)
)

# Identify at-risk premium customers
data["At_Risk_Premium"] = (
    data["Premium_Customer"] &
    (data["IsActiveMember"] == 0)
)

# Get only at-risk premium customers
at_risk = data[data["At_Risk_Premium"] == True]

print("Total Premium Customers:",
      data["Premium_Customer"].sum())

print("At-Risk Premium Customers:",
      len(at_risk))

# print("\nAt-Risk Premium Customers:")
# print(at_risk[
#     [
#         "CustomerId",
#         "Balance",
#         "EstimatedSalary",
#         "Tenure",
#         "NumOfProducts",
#         "IsActiveMember",
#         "Exited"
#     ]
# ])

print("--"*35,"Retention Strength Assessment","--"*35)
result = data.groupby("Exited").agg(
    Customers=("Exited", "count"),
    Avg_Balance=("Balance", "mean"),
    Avg_Tenure=("Tenure", "mean"),
    Avg_Products=("NumOfProducts", "mean"),
    Avg_Salary=("EstimatedSalary", "mean"),
    Active_Rate=("IsActiveMember", "mean"),
    Credit_Card_Rate=("HasCrCard", "mean")
).reset_index()

result["Active_Rate"] = result["Active_Rate"] * 100
result["Credit_Card_Rate"] = result["Credit_Card_Rate"] * 100

print(result)
print("\nChurn by Activity:")
print(data.groupby("IsActiveMember")["Exited"].mean() * 100)

print("\nChurn by Tenure:")
print(data.groupby("Tenure")["Exited"].mean() * 100)

print("\nChurn by Number of Products:")
print(data.groupby("NumOfProducts")["Exited"].mean() * 100)

print("\nChurn by Credit Card:")

print(data.groupby("HasCrCard")["Exited"].mean() * 100)
print("Sticky profile:")
print("Sticky customers tend to have longer relationships with the bank, remain actively engaged, use multiple products, and maintain higher balances. These characteristics are associated with lower churn and can be used as a reference profile for improving customer retention.")

# Create engagement tiers
print("--"*25,"Measure churn stability across engagement tiers","--"*25)

data["Engagement_Tier"] = data.apply(
    lambda row:
        "High Engagement"
        if row["IsActiveMember"] == 1 and row["NumOfProducts"] >= 2
        else
        "Medium Engagement"
        if row["IsActiveMember"] == 1 or row["NumOfProducts"] >= 2
        else
        "Low Engagement",
    axis=1
)

# Measure churn across engagement tiers



engagement_result = data.groupby("Engagement_Tier").agg(
    Customers=("Exited", "count"),
    Churned=("Exited", "sum")
).reset_index()

engagement_result["Churn_Rate_%"] = (
    engagement_result["Churned"] /
    engagement_result["Customers"] * 100
)

print(engagement_result)
print("Thus: As customer engagement increases, churn decreases.")

print("--"*25,"Identify Engagement Threshold","--"*25)

threshold = data.groupby("Engagement_Tier")["Exited"].mean() * 100

print("Churn Rate:")
print(threshold)

low = threshold["Low Engagement"]
medium = threshold["Medium Engagement"]
high = threshold["High Engagement"]

print("\nLow → Medium reduction:", low - medium, "%")
print("Medium → High reduction:", medium - high, "%")
print("Low → High reduction:", low - high, "%")