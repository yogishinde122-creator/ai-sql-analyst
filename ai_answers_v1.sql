as yetay -- Q1
SELECT COUNT(*) FROM customers;
-- Q2
SELECT COUNT(*) FROM customers WHERE Exited = 1;
-- Q3
SELECT AVG(CreditScore) FROM customers;
-- Q4
SELECT Geography, COUNT(*) FROM customers GROUP BY Geography;
-- Q5
SELECT * FROM customers ORDER BY Balance DESC LIMIT 5;
-- Q6
SELECT Gender, AVG(EstimatedSalary) FROM customers GROUP BY Gender;
-- Q7
SELECT "Card Type", (COUNT(CASE WHEN Exited = 1 THEN 1 END) * 100.0) / COUNT(*) AS ChurnRatePercentage FROM customers GROUP BY "Card Type";
-- Q8
SELECT IsActiveMember, (COUNT(CASE WHEN Exited = 1 THEN 1 END) * 100.0) / COUNT(*) AS ChurnRatePercentage FROM customers GROUP BY IsActiveMember;
-- Q9
SELECT COUNT(CASE WHEN Complain = 1 THEN 1 END) AS ComplainedCount, COUNT(CASE WHEN Complain = 1 AND Exited = 1 THEN 1 END) AS ComplainedAndExitedCount FROM customers;
-- Q10
SELECT COUNT(), (COUNT(CASE WHEN Exited = 1 THEN 1 END) * 100.0) / COUNT() AS ChurnRatePercentage FROM customers WHERE Geography = 'Germany' AND Balance > (SELECT AVG(Balance) FROM customers);
