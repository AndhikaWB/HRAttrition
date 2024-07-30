import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from predict import preprocess, predict

# This backend is not production ready and may bottleneck on large amount of requests
# For production ready example, see below or use the search keyword: "run keras fastapi"
# https://medium.com/analytics-vidhya/4940df614ece

# There is also other alternative such as by using TFX
# https://www.tensorflow.org/tfx/tutorials/serving/rest_simple
# https://github.com/JeConn-Bangkit-2023/Machine-Learning/blob/main/fast-api-backend/main.py

app = FastAPI()

@app.get('/')
def get_root():
    # 404 not found
    raise HTTPException(404, 'Use POST /predict instead of root!')

# To post Pandas dataframe to FastAPI
# https://github.com/tiangolo/fastapi/issues/1616

class DFInput(BaseModel):
    # index: list[int]
    columns: list[str]
    data: list[list]

    model_config = {
        'json_schema_extra': {
            'examples': [
                pd.read_csv(
                    'data/employee_data.csv'
                ).head(3).to_dict(orient = 'split', index = False)
            ]
        }
    }

# Response model (optional, for documentation)
# Will work even without defining the "response_model"

class DFOutput(BaseModel):
    # index: list[int]
    columns: list[str]
    data: list[list]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'columns': ['EmployeeId', 'Confidence', 'IsAttrition'],
                    'data': [
                        # If there are 3 rows from input
                        [774, 99, 'Most_Likely'],
                        [1006, 99, 'Most_Likely'],
                        [505, 99, 'Most_Likely']
                    ]
                }
            ]
        }
    }

# We can't handle JSON data and file upload simultaneously (HTTP limitation)
# But we can make it as form data and file upload, however...
# The problem with form is that it can't handle list, so we can't use that
# As workaround, I'm separating the endpoint for JSON and file upload

# Related issues
# https://fastapi.tiangolo.com/tutorial/request-forms-and-files/
# https://stackoverflow.com/q/68884287/fastapi-error-when-uploading-file-with-json-data
# https://github.com/fastapi/fastapi/issues/854

@app.post('/predict', response_model = DFOutput)
async def post_predict(data: DFInput):
    try:
        df = pd.DataFrame(data.data, columns = data.columns)
        df = preprocess(df)
        return predict(df)
    except Exception as e:
        # 500 internal server error
        raise HTTPException(500, str(e))

@app.post('/predict_file', response_model = DFOutput)
async def post_predict_file(file: UploadFile):
    try:
        df = pd.read_csv(file.file)
        df = preprocess(df)
        return predict(df)
    except Exception as e:
        raise HTTPException(500, str(e))