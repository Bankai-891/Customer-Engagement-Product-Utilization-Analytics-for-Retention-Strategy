# 🏦 Customer Engagement & Product Utilization Analytics for Retention Strategy

> An interactive banking analytics application designed to understand customer behavior, identify churn patterns, detect high-value disengaged customers, and support data-driven retention strategies.

---

## 📌 Project Overview

Customer churn is one of the major challenges faced by financial institutions.

A customer may have:

- High account balance
- High estimated salary
- Long banking relationship
- Multiple banking products

and still leave the bank.

This project analyzes customer engagement, product utilization, financial behavior, tenure, and activity patterns to identify characteristics associated with customer churn.

The project combines **Python, Pandas, Matplotlib, and Streamlit** to create an interactive customer retention analytics dashboard.

---

# 🎯 Business Objective

The main objectives of this project are:

- Understand customer churn behavior
- Analyze churn by customer engagement
- Analyze product utilization and churn
- Identify high-value disengaged customers
- Analyze customer retention characteristics
- Identify potentially at-risk customer segments
- Provide actionable business insights for retention strategies

---

# 🧩 Business Questions

This project attempts to answer questions such as:

### 1. Does customer engagement affect churn?

Are inactive customers more likely to leave the bank?

### 2. Does product utilization affect retention?

Do customers using multiple banking products have different churn behavior?

### 3. Which customers are potentially high-value but disengaged?

Can we identify customers with relatively high financial value who are currently inactive?

### 4. Does customer tenure influence churn?

Are newer or long-term customers more likely to leave?

### 5. What customer characteristics are associated with stronger retention?

Can we identify a profile of customers who are more likely to remain with the bank?

---

# 📊 Dataset

The project uses a European bank customer churn dataset containing customer-level information.

### Main Features

| Feature | Description |
|---|---|
| CustomerId | Unique customer identifier |
| CreditScore | Customer credit score |
| Geography | Customer location |
| Gender | Customer gender |
| Age | Customer age |
| Tenure | Years with the bank |
| Balance | Account balance |
| NumOfProducts | Number of bank products used |
| HasCrCard | Whether the customer has a credit card |
| IsActiveMember | Whether the customer is an active member |
| EstimatedSalary | Estimated customer salary |
| Exited | Whether the customer left the bank |

### Target Variable

`Exited`
![Salary Balance Analysis](images/salary_balance_mismatch.png)

```text
0 → Customer retained
1 → Customer churned
