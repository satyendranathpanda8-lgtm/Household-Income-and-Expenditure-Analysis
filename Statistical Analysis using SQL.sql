SELECT * FROM household;

# Mean
select avg(Total_Household_income) as Mean_income from household;

# Mode
select Total_Household_income, count(*) as freq
from household
group by Total_Household_income
order by freq desc
limit 1;

# Standard Deviation
select stddev(Total_Household_income) as std_dev
from household;

# Variance
select variance(Total_Household_income) as variance
from household;

# Range
select max(Total_Household_income) - min(Total_Household_income) as range_value
from household;


### Data Cleaning 
CREATE TABLE household_cleann AS
SELECT * FROM household;

select * from household_cleann
limit 10;


# Null value check
SELECT COUNT(*) 
FROM household_cleann
WHERE Total_Household_Income IS NULL;

DELETE FROM household_cleann
WHERE Total_Household_Income IS NULL;

## Outlier Detection
SELECT 
MIN(Total_Household_Income),
MAX(Total_Household_Income),
AVG(Total_Household_Income)
FROM household_cleann;

SET SQL_SAFE_UPDATES = 0;

UPDATE household_cleann
SET Total_Household_Income = 50000
WHERE Total_Household_Income > 50000;

# Duplicate check 
SELECT 
Total_Household_Income, Region, Source_of_Income,
COUNT(*) AS freq
FROM household_cleann
GROUP BY 
Total_Household_Income, Region, Source_of_Income
HAVING COUNT(*) > 1;

## Flagged Duplicates
ALTER TABLE household_cleann
ADD COLUMN is_duplicate INT DEFAULT 0;

UPDATE household_cleann 
SET is_duplicate = 1;


## Fixing Text columns
UPDATE household_cleann SET Region = LOWER(TRIM(Region));
UPDATE household_cleann SET Source_of_Income = LOWER(TRIM(Source_of_Income));
UPDATE household_cleann SET Main_Source_of_Water_Supply = LOWER(TRIM(Main_Source_of_Water_Supply));

## Creating Total Expenditure column
ALTER TABLE household_cleann
ADD COLUMN total_expenditure DECIMAL(12,2);

UPDATE household_cleann
SET total_expenditure =
COALESCE(Staple_Food_Expenditure,0) +
COALESCE(Meat_Expenditure,0) +
COALESCE(Seafood_Expenditure,0) +
COALESCE(Leisure_Expenditure,0) +
COALESCE(Alcohol_Expenditure,0) +
COALESCE(Tobacco_Expenditure,0) +
COALESCE(Medical_Expenditure,0) +
COALESCE(Transportation_Expenditure,0) +
COALESCE(Communication_Expenditure,0) +
COALESCE(Utilities_Expenditure,0) +
COALESCE(Education_Expenditure,0) +
COALESCE(Crop_Farming_Expenditure,0);

SELECT total_expenditure, Total_Household_Income 
FROM household_cleann
LIMIT 5;

## Validation
SELECT COUNT(*)
FROM household_cleann
WHERE total_expenditure > Total_Household_Income;

ALTER TABLE household_cleann
ADD COLUMN is_invalid INT DEFAULT 0;

UPDATE household_cleann
SET is_invalid = 1
WHERE total_expenditure > Total_Household_Income;

select * from household_cleann;
