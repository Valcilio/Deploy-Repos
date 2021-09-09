import pickle
import pandas as pd
from sklearn.preprocessing  import RobustScaler, MinMaxScaler
from flask import Flask, request, Response
from insuranceAll.InsuranceAll import InsuranceAll

model = pickle.load(open('model.pkl','rb'))

app = Flask(__name__)
@app.route('/', methods=['POST'])

def insurance_all_predict():
    test_json= request.get_json()
    
    if test_json:
        if isinstance(test_json,dict):
            test_raw=pd.DataFrame(test_json,index=[0])
        else:
            test_raw=pd.DataFrame(test_json,columns=test_json[0].keys())
               
        pipeline = InsuranceAll()
        df = test_raw.copy()
        df = pipeline.data_cleaning(df)
        df = pipeline.feature_engieneering(df)
        df = pipeline.feature_filtering(df)
        df = pipeline.data_rescaling(df)
        df = pipeline.data_encoding(df)
        df_response = pipeline.get_prediction(model, test_raw, df)
        return df_response
    
    else:
        return Response('{}', status=200, mimetype='application/json')

    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
