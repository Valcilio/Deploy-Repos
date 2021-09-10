import pickle
import pandas as pd
import os

from sklearn.preprocessing  import RobustScaler, MinMaxScaler
from flask import Flask, request, Response
from insuranceAll.InsuranceAll import InsuranceAll

model = pickle.load(open('model.pkl','rb'))

app = Flask(__name__)
@app.route('/predict', methods=['POST'])

def insurance_all_predict():
    test_json= request.get_json()
    
    if test_json:
        
        if isinstance(test_json,dict):
            test_raw=pd.DataFrame(test_json,index=[0])
        else:
            test_raw=pd.DataFrame(test_json,columns=test_json[0].keys())
               
        pipeline = InsuranceAll()
        df = test_raw.copy()
        df = pipeline.feature_engineering(df)
        
        # Scalers
        home_path = 'scalers/'
        aps = pickle.load(open(home_path + 'annual_premium_scaler.pkl', 'rb'))
        age = pickle.load(open(home_path + 'age_scaler.pkl', 'rb'))
        vs = pickle.load(open(home_path + 'vintage_scaler.pkl', 'rb'))
        pscs = pickle.load(open(home_path + 'policy_sales_channel_scaler.pkl', 'rb'))
        rrrs = pickle.load(open(home_path + 'risk_region_rate_scaler.pkl', 'rb'))
        rcs = pickle.load(open(home_path + 'region_code_scaler.pkl', 'rb'))
        
        # Rescaling
        df['annual_premium'] = aps.transform(df[['annual_premium']].values)
        df['age'] = age.transform(df[['age']].values)
        df['vintage'] = vs.transform(df[['vintage']].values)
        df['policy_sales_channel'] = pscs.transform(df[['policy_sales_channel']].values)
        df['risk_region_rate'] = rrrs.transform(df[['risk_region_rate']].values)
        df['region_code'] = rcs.transform(df[['region_code']].values)
        
        df = pipeline.data_encoding(df)
        df_response = pipeline.get_prediction(model, test_raw, df)
        
        return df_response
    
    else:
        return Response('{}', status=200, mimetype='application/json')

    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
