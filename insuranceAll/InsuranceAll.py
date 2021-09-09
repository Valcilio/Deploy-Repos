import json
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing  import RobustScaler, MinMaxScaler

class InsuranceAll(object):
    
    def __init__(self):
        
        self.aps = pickle.load(open('scalers/annual_premium_scaler.pkl', 'rb'))
        self.age = pickle.load(open('scalers/age_scaler.pkl', 'rb'))
        self.vs = pickle.load(open('scalers/vintage_scaler.pkl', 'rb'))
        self.pscs = pickle.load(open('scalers/policy_sales_channel_scaler.pkl', 'rb'))
        self.rrrs = pickle.load(open('scalers/risk_region_rate_scaler.pkl', 'rb'))
        self.rcs = pickle.load(open('scalers/region_code_scaler.pkl', 'rb'))
        
    def df_cleaning(df, self):
    
        # creating old columns variable
        cols_old = ['id', 'Gender', 'Age', 'Driving_License', 'Region_Code',
               'Previously_Insured', 'Vehicle_Age', 'Vehicle_Damage', 'Annual_Premium',
               'Policy_Sales_Channel', 'Vintage', 'Response']

        # creating sknakecase variable
        snakecase = lambda x: inflection.underscore(x)

        # creting snakecase columns
        cols_new = list(map(snakecase, cols_old))

        # renaming
        df.columns = cols_new

        # region_code to int64
        df['region_code'] = df['region_code'].astype(int)

        # policy_sales_channel
        df['policy_sales_channel'] = df['policy_sales_channel'].astype(int)

        return df
        
        
    def feature_engineering(df, self):
    
        risk_regions = [0,  1,  4,  5,  7, 19, 20, 23, 24, 26, 28, 31, 34, 37, 38, 39, 40,
           42, 43, 47, 48, 49, 51]

        # risk_age
        df['risk_age'] = df['age'].apply(lambda x: 0 if x > 25 else 1)

        # more_than_40_years
        df['more_than_40_years'] = df['age'].apply(lambda x: 'yes' if x > 40 else 'no')

        #------------------------------------------------------------------------------------------------------
        # summing vehicle_damage by region_code
        aux = df.copy()
        aux['vehicle_damage'] = aux['vehicle_damage'].apply(lambda x: 0 if x == 'No' else 1)
        aux1 = aux[['region_code', 'vehicle_damage']].groupby('region_code').sum().reset_index()

        # counting regions' appearences
        df['region'] = df['region_code'].copy()
        aux4 = df[['region_code', 'region']].groupby('region_code').count().reset_index().drop('region_code', axis=1)
        aux5 = pd.concat([aux4, aux1], axis=1)

        # derivating the rate of risk region
        aux5['risk_region_rate'] = aux5['vehicle_damage']/aux5['region']

        # derivating rate - region variable to merge
        aux7 = aux5.copy()
        aux7 = aux7.drop(['region', 'vehicle_damage'], axis=1)
        aux7['risk_region_rate'] = aux7['risk_region_rate']*1000

        # merging datasets
        df = pd.merge(aux, aux7, how='left', on='region_code')

        #---------------------------------------------------------------------------------------------------------

        # risk_region
        df['risk_region'] = df['region_code'].apply(lambda x: 'Yes' if x in reg_risk else 'No')

        return df
        
    def data_filtering(self,df):
        
        df = df['vintage',
             'annual_premium',
             'region_code',
              'vehicle_damage',
              'policy_sales_channel',
             'driving_license',
             'previously_insured',
             'age',
             'more_than_40_years',
             'risk_region_rate']
        
        return df
                      
    def data_rescale(self,df):
        
        df['annual_premium'] = self.aps.transform(df[['annual_premium']].values)
        df['age'] = self.age.transform(df[['age']].values)
        df['vintage'] = self.vs.transform(df[['vintage']].values)
        df['policy_sales_channel'] = self.pscs.transform(df[['policy_sales_channel']].values)
        df['risk_region_rate'] = self.rrrs.transform(df[['risk_region_rate']].values)
        df['region_code'] = self.rcs.transform(df[['region_code']].values)
        
        return df
    
    def data_encoding(self, df):
        
        df['more_than_40_years'] = df['more_than_40_years'].apply(lambda x: 1 if x == 'yes' else 0)
        df = pd.get_dummies(df, prefix=['vehicle_age'], columns=['vehicle_age'])
        
        return df

    def get_prediction(self, model, original_data, test_data):
        
        # model prediction
        pred = model.predict_proba( test_data )

        # join prediction into original data
        original_data['prediction'] = pred

        return original_data.to_json( orient='records', date_format='iso' )   
