# Employee Data

The data contains demographic details, work-related metrics, and attrition flag.

* **EmployeeId** / **EmployeeNumber** - Employee Identifier
* **Attrition** - Did the employee leave?
* **Age** - Age of the employee
* **BusinessTravel** - 0-No Travel, 1-Travel Rarely, 2-Travel Frequently
* **DailyRate** - Daily rate
* **Department** - Employee Department
* **DistanceFromHome** - Distance from work to home (in km)
* **Education** - 1-Below College, 2-College, 3-Bachelor, 4-Master, 5-Doctor
* **EducationField** - Field of Education
* **EnvironmentSatisfaction** - 1-Low, 2-Medium, 3-High, 4-Very High
* **Gender** - Employee's gender
* **HourlyRate** - Hourly rate
* **JobInvolvement** - 1-Low, 2-Medium, 3-High, 4-Very High
* **JobLevel** - Level of job (1 to 5)
* **JobRole** - Job Roles
* **JobSatisfaction** - 1-Low, 2-Medium, 3-High, 4-Very High
* **MaritalStatus** - Marital Status
* **MonthlyIncome** - Monthly salary
* **MonthlyRate** - Monthly rate
* **NumCompaniesWorked** - Number of companies worked at
* **Over18** - Over 18 years?
* **OverTime** - Overtime?
* **PercentSalaryHike** - The percentage increase in salary last year
* **PerformanceRating** - 1-Low, 2-Good, 3-Excellent, 4-Outstanding
* **RelationshipSatisfaction** - 1-Low, 2-Medium, 3-High, 4-Very High
* **StandardHours** - Standard Hours
* **StockOptionLevel** - Stock Option Level
* **TotalWorkingYears** - Total years worked
* **TrainingTimesLastYear** - Number of training attended last year
* **WorkLifeBalance** - 1-Low, 2-Good, 3-Excellent, 4-Outstanding
* **YearsAtCompany** - Years at Company
* **YearsInCurrentRole** - Years in the current role
* **YearsSinceLastPromotion** - Years since the last promotion
* **YearsWithCurrManager** - Years with the current manager

## Notes

- **employee_data.csv** - Original employee data provided by IBM and later modified by Dicoding (contains missing attrition values)
- **WA_Fn-UseC_-HR-Employee-Attrition.csv** - Other version from Kaggle that has no missing attrition value
- **employee_data_fixed.csv** - Using Kaggle data, plus "IsTest" column to mark rows that originally had missing attrition value (from Dicoding)

## Acknowledgements
https://www.ibm.com/communities/analytics/watson-analytics-blog/watson-analytics-use-case-for-hr-retaining-valuable-employees/ (mirror: [archive](https://web.archive.org/web/20181120093257/https://www.ibm.com/communities/analytics/watson-analytics-blog/watson-analytics-use-case-for-hr-retaining-valuable-employees/), [kaggle 1](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset/), [kaggle 2](https://www.kaggle.com/competitions/playground-series-s3e3/))