import os
import pandas as pd
import keras

from sklearn.preprocessing import (
    TargetEncoder,
    MinMaxScaler
)

# CSV used to predict employee attrition (no attrition column)
# Must contain employee data such as age, income, etc to predict
CSV_PRED_PATH = 'data/employee_data.csv'

# CSV for target encoding (must have fully filled attrition column!)
#
# Values should be similar between base and pred CSV
# e.g. In order to recognize HR department in pred CSV,
# the HR department must also exist on base CSV
#
# The easiest way is to separate CSV by period (month, year, etc)
# e.g. base CSV = last month data, pred CSV = this month data (to predict)
#
# TODO: Pickle the encoder to remove base CSV requirement
CSV_BASE_PATH = 'data/employee_data_fixed.csv'

# Model used for predicting attrition
MODEL_PATH = 'model/model_ensemble.keras'

# Where to save output prediction from the model?
# Output will be employee id and its attrition prediction
MODEL_PRED_CSV = 'model/model_output.csv'


def data_convert(df: pd.DataFrame) -> pd.DataFrame:
    return df.replace(
        {
            'Attrition': {
                'Yes': 1,
                'No': 0
            },
            'BusinessTravel': {
                'Non-Travel': 0,
                'Travel_Rarely': 1,
                'Travel_Frequently': 2
            },
            'Over18': {
                'Y': 1,
                'N': 0
            },
            'OverTime': {
                'Yes': 1,
                'No': 0
            }
        }
    )

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    # ===============
    # Convert data types

    df = data_convert(df)

    cat_col = ['Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus']

    for col in cat_col:
        df[col + 'N'] = pd.factorize(df[col])[0]

    # ===============
    # Drop unimportant columns
        
    df.drop(['EmployeeCount', 'Over18', 'StandardHours'], axis = 1, inplace = True)

    # ===============
    # Replace income outliers

    col = [i for i in df.columns if 'Rate' in i or 'Income' in i]

    for c in col:
        q1 = df[c].quantile(0.25)
        q3 = df[c].quantile(0.75)

        iqr = q3 - q1
        iqr1 = q1 - 1.5 * iqr
        iqr3 = q3 + 1.5 * iqr
        
        df.loc[ df[c] < iqr1, c ] = 0 if iqr1 < 0 else int(iqr1)
        df.loc[ df[c] > iqr3, c ] = int(iqr3)

    # ===============
    # Bucketize continuous values
        
    bin_arg = {'right': True, 'include_lowest': True}

    temp = [18] + [i * 5 + 20 for i in range(9)] # 18, 20, 25, 30, ..., 60
    df['Age'] = pd.cut(df['Age'], bins = temp, labels = [i for i in range(len(temp) - 1)], **bin_arg)

    temp = [i * 5 for i in range(7)] # 0, 5, 10, 15, ..., 30
    df['DistanceFromHome'] = pd.cut(df['DistanceFromHome'], bins = temp, labels = [i for i in range(len(temp) - 1)], **bin_arg)

    temp = [i * 2000 for i in range(16)] # 0, 2000, 4000, 6000, ..., 30000
    df['MonthlyIncome'] = pd.cut(df['MonthlyIncome'], bins = temp, labels = [i for i in range(len(temp) - 1)], **bin_arg)
    df['MonthlyRate'] = pd.cut(df['MonthlyRate'], bins = temp, labels = [i for i in range(len(temp) - 1)], **bin_arg)

    temp = [0, 1, 2, 5, 10]
    df['NumCompaniesWorked'] = pd.cut(df['NumCompaniesWorked'], bins = temp, labels = [i for i in range(len(temp) - 1)], **bin_arg)

    temp = [i * 5 for i in range(6)] # 0, 5, 10, 15, ..., 25
    df['PercentSalaryHike'] = pd.cut(df['PercentSalaryHike'], bins = temp, labels = [i for i in range(len(temp) - 1)], **bin_arg)

    temp = [0, 2] + [ (i + 1) * 5 for i in range(9)] # 0, 2, 5, 10, 15, ..., 45
    df['YearsAtCompany'] = pd.cut(df['YearsAtCompany'], bins = temp, labels = [i for i in range(len(temp) - 1)], **bin_arg)
    df['YearsInCurrentRole'] = pd.cut(df['YearsInCurrentRole'], bins = temp, labels = [i for i in range(len(temp) - 1)], **bin_arg)
    df['YearsSinceLastPromotion'] = pd.cut(df['YearsSinceLastPromotion'], bins = temp, labels = [i for i in range(len(temp) - 1)], **bin_arg)
    df['YearsWithCurrManager'] = pd.cut(df['YearsWithCurrManager'], bins = temp, labels = [i for i in range(len(temp) - 1)], **bin_arg)
    df['TotalWorkingYears'] = pd.cut(df['TotalWorkingYears'], bins = temp, labels = [i for i in range(len(temp) - 1)], **bin_arg)

    # ===============
    # Encode the rest of the columns

    bin_col = [
        'Age','DistanceFromHome','MonthlyIncome','MonthlyRate','NumCompaniesWorked','PercentSalaryHike',
        'YearsAtCompany','YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager','TotalWorkingYears'
    ]

    cat_col = ['Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus']

    other_col = [
        'BusinessTravel', 'Education', 'EnvironmentSatisfaction', 'JobInvolvement', 'JobLevel', 'JobSatisfaction',
        'OverTime', 'PerformanceRating', 'RelationshipSatisfaction', 'StockOptionLevel', 'TrainingTimesLastYear',
        'WorkLifeBalance'
    ]

    enc_col = bin_col + cat_col + other_col
    cat_encoder = TargetEncoder()
    
    temp = pd.read_csv(CSV_BASE_PATH)
    temp = data_convert(temp)

    for col in enc_col:
        if temp[col].dtype != df[col].dtype:
            temp[col] = temp[col].astype(df[col].dtype)

    new_col = [i + 'N' for i in enc_col]
    cat_encoder.fit(temp[enc_col], temp['Attrition'])
    df[new_col] = cat_encoder.transform(df[enc_col])

    # ===============
    # Feature removal/selection

    temp = [i[:-1] for i in df.columns if i[-1] == 'N']
    df.drop(temp, axis = 1, inplace = True)

    # From Pearson correlation (r_regression)
    col = ['EmployeeId'] + [
        'OverTimeN',
        'JobRoleN',
        'TotalWorkingYearsN',
        'JobLevelN',
        'MonthlyIncomeN',
        'YearsAtCompanyN',
        'AgeN',
        'StockOptionLevelN',
        'MaritalStatusN',
        'YearsInCurrentRoleN',
        'YearsWithCurrManagerN',
        'BusinessTravelN',
        'JobInvolvementN',
        'EnvironmentSatisfactionN'
    ] # + ['IsTest', 'Attrition']

    df = df[col]

    return df

def predict(df: pd.DataFrame):
    # ===============
    # Data scaling and dividing

    col = [i for i in df.columns if i != 'EmployeeId' and i != 'IsTest']
    x_col = [i for i in col if i != 'Attrition']
    y_col = ['Attrition']

    scaler = MinMaxScaler()
    df[x_col] = scaler.fit_transform(df[x_col])

    # ===============
    # Load model and predict

    x_test = df[x_col]
    model_ensemble = keras.models.load_model(MODEL_PATH)
    y_pred = model_ensemble.predict(x_test)

    df_pred = pd.DataFrame()
    df_pred['EmployeeId'] = df['EmployeeId']
    df_pred['Prediction'] = y_pred * 100

    df_pred.loc[df_pred['Prediction'] >= 60, 'IsAttrition'] = 'Most_Likely'
    df_pred.loc[(df_pred['Prediction'] >= 40) & (df_pred['Prediction'] < 60), 'IsAttrition'] = 'With_Caution'
    df_pred.loc[df_pred['Prediction'] < 40, 'IsAttrition'] = 'Less_Likely'

    df_pred = df_pred.sort_values('Prediction', ascending = False)
    df_pred['Prediction'] = df_pred['Prediction'].astype('int')

    df_pred.to_csv(MODEL_PRED_CSV, index = False)

    print(f'\nHasil prediksi model disimpan ke: "{MODEL_PRED_CSV}"')
    print('PENTING! Prediksi tidak bersifat absolut dan tetap bisa salah')

if __name__ == '__main__':
    if not os.path.isfile(CSV_PRED_PATH):
        print(f'File CSV tidak dapat ditemukan: "{CSV_PRED_PATH}"')
        CSV_PRED_PATH = input('Masukkan lokasi file CSV secara manual: ').strip('\"').strip()
    
    df = pd.read_csv(CSV_PRED_PATH)
    df = preprocess(df)
    predict(df)