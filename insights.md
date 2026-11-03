# Insights from the bank customer data

1. The dataset has 10,000 customers across 3 countries.
2. Germany has the highest churn rate: 32.44%.
3. Germany also has the highest average balance: 119,730.12.
4. The age group with the highest churn is 45-59 (49.45%).
5. In France and Spain, customers who left held about 18-22% higher
   average balances than those who stayed.
6. In Germany, churned and retained customers have almost the same
   average balance, so balance alone does not explain its high churn.

Conclusion: Customers with higher balances are more likely to leave
in France and Spain, which means the bank may be losing valuable
customers there. Germany's high churn needs a deeper look at other
factors (for example age, products or activity). These are averages
and show patterns, not proven causes.
7. Complaints and churn: 2,034 of 2,044 customers who complained
   (about 99.5%) left the bank, versus only 4 of 7,956 who did not
   complain. This is almost certainly data leakage (the complaint is
   probably recorded at or after exit), so Complain should not be
   used to predict churn.
8. Inactive members churn at 26.87% versus 14.27% for active members.
9. Card type makes little difference to churn (19-22%).