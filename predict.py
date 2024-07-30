import os
import pandas as pd
import keras
import joblib

from sklearn.preprocessing import MinMaxScaler

# CSV used to predict employee attrition (no attrition column)
# Must contain employee data such as age, income, etc to predict
CSV_INPUT = 'data/employee_data.csv'
# Where to save output prediction from the model?
# Output will be employee id and its attrition prediction
MODEL_OUTPUT = 'model/model_output.csv'

# Data scaler object (to avoid unnecessary reinitialization)
SCALER_OBJ = MinMaxScaler()
# Target encoder that is already fitted before
ENCODER_OBJ = joblib.load('model/encoder.lz4')
# The neural network model
MODEL_OBJ = keras.models.load_model('model/model_ensemble.keras')

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    # ===============
    # Convert data types

    df = df.replace(
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

    cat_col = ['Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus']
    for col in cat_col: df[col + 'N'] = pd.factorize(df[col])[0]

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
    # Bin/bucketize continuous values

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
    cat_encoder = ENCODER_OBJ

    new_col = [i + 'N' for i in enc_col]
    df[new_col] = cat_encoder.transform(df[enc_col])

    # ===============
    # Feature removal/selection

    temp = [i[:-1] for i in df.columns if i[-1] == 'N']
    df.drop(temp, axis = 1, inplace = True)

    # From Pearson correlation (r_regression)
    col = ['EmployeeId'] + [
        'TotalWorkingYearsN', 'OverTimeN', 'JobRoleN', 'MonthlyIncomeN', 'AgeN',
        'JobLevelN', 'YearsAtCompanyN', 'StockOptionLevelN', 'MaritalStatusN',
        'YearsInCurrentRoleN', 'YearsWithCurrManagerN', 'JobInvolvementN',
        'BusinessTravelN', 'EnvironmentSatisfactionN', 'DistanceFromHomeN',
        'JobSatisfactionN', 'WorkLifeBalanceN', 'EducationFieldN',
        'TrainingTimesLastYearN'
    ] # + ['IsTest', 'Attrition']

    df = df[col]

    return df

def predict(df: pd.DataFrame, out_csv: bool = False):
    # ===============
    # Data scaling and dividing

    col = [i for i in df.columns if i != 'EmployeeId' and i != 'IsTest']
    x_col = [i for i in col if i != 'Attrition']
    y_col = ['Attrition']

    scaler = SCALER_OBJ
    df[x_col] = scaler.fit_transform(df[x_col])

    # ===============
    # Load model and predict

    x_test = df[x_col]
    model_ensemble = MODEL_OBJ
    y_pred = model_ensemble.predict(x_test)

    df_pred = pd.DataFrame()
    df_pred['EmployeeId'] = df['EmployeeId']
    df_pred['Confidence'] = y_pred * 100

    df_pred.loc[df_pred['Confidence'] >= 60, 'IsAttrition'] = 'Most_Likely'
    df_pred.loc[(df_pred['Confidence'] >= 40) & (df_pred['Confidence'] < 60), 'IsAttrition'] = 'With_Caution'
    df_pred.loc[df_pred['Confidence'] < 40, 'IsAttrition'] = 'Less_Likely'

    df_pred = df_pred.sort_values('Confidence', ascending = False)
    df_pred['Confidence'] = df_pred['Confidence'].astype('int')

    if out_csv:
        df_pred.to_csv(MODEL_OUTPUT, index = False)
        print(f'\nHasil prediksi model disimpan ke: "{MODEL_OUTPUT}"')
        print('PENTING! Prediksi tidak bersifat absolut dan tetap bisa salah')

    return df_pred.to_dict(orient = 'split', index = False)

if __name__ == '__main__':
    if not os.path.isfile(CSV_INPUT):
        print(f'File CSV tidak dapat ditemukan: "{CSV_INPUT}"')
        CSV_INPUT = input('Masukkan lokasi file CSV secara manual: ').strip('\"').strip()
    
    df = pd.read_csv(CSV_INPUT)
    df = preprocess(df)
    predict(df, out_csv = True)