import pickle
import streamlit as st
import pandas as pd
import numpy as np
import math
from sklearn.preprocessing     import RobustScaler, MinMaxScaler
from sklearn.ensemble import RandomForestRegressor

#load the trained model
model = pickle.load(open('model.pkl', 'rb'))

# defining the prediction function
def predict(Wbit, Hookload, BlockPosition, DepthBit, MudFlow, RateOfPenetration, DownholeWbit,
                StandpipePressure, DifHolBit, WbitDens):
                
    # preparing the dataset

    #bpos.ft
    rs = pickle.load(open('scalers/bpos_ft_scaler.pkl', 'rb'))
    BP = (rs.transform([[BlockPosition]]))[0]
    BlockPosition = BP[0]

    # woba.klbf
    mms = pickle.load(open('scalers/woba_klbf_scaler.pkl', 'rb'))
    Wb = (mms.transform([[Wbit]]))[0]
    Wbit = Wb[0]

    # hkla.klbf
    mms = pickle.load(open('scalers/hkla_klbf_scaler.pkl', 'rb'))
    Hk = (mms.transform([[Hookload]]))[0]
    Hookload = Hk[0]

    # dbtm.ft
    mms = pickle.load(open('scalers/dbtm_ft_scaler.pkl', 'rb'))
    DB = (mms.transform([[DepthBit]]))[0]
    DepthBit = DB[0]

    # mfop.%
    mms = pickle.load(open('scalers/mfop_%_scaler.pkl', 'rb'))
    MF = (mms.transform([[MudFlow]]))[0]
    MudFlow = MF[0]

    # ropa.ft/h
    mms = pickle.load(open('scalers/ropa_ft_h_scaler.pkl', 'rb'))
    RP = (mms.transform([[RateOfPenetration]]))[0]
    RateOfPenetration = RP[0]

    # dhwob.klbf
    mms = pickle.load(open('scalers/dhwob_klbf_scaler.pkl', 'rb'))
    DW = (mms.transform([[DownholeWbit]]))[0]
    DownholeWbit = DW[0]

    # sppa.psi
    mms = pickle.load(open('scalers/sppa_psi_scaler.pkl', 'rb'))
    SP = (mms.transform([[StandpipePressure]]))[0]
    StandpipePressure = SP[0]

    # dif_hol_bit
    mms = pickle.load(open('scalers/dif_hol_bit_scaler.pkl', 'rb'))
    DB = (mms.transform([[DifHolBit]]))[0]
    DifHolBit = DB[0]

    # weig_bit_dens
    mms = pickle.load(open('scalers/weig_bit_dens_scaler.pkl', 'rb'))
    WD = (mms.transform([[WbitDens]]))[0]
    WbitDens = WD[0]

    # making the prediction
    yhat = model.predict([[Wbit, Hookload, BlockPosition, DepthBit, MudFlow, RateOfPenetration, DownholeWbit,
                StandpipePressure, DifHolBit, WbitDens]])
    
    # giving the answer
    prediction = (yhat)
    
    return prediction
    
def main():
    st.header('Time Out and In Slips Predictor')
    st.text("Author: Valcilio Eugenio - Data Scientist")
    
    #asking for DepthHole
    DepthHole = st.number_input('Depth Hole (measured) in feet (ft)', value=0)
    
    #asking for DepthBit
    DepthBit = st.number_input('Total feet (ft) of the Depth Bit (measured)', value=0)
    
    #asking for StandpipePressure
    StandpipePressure = st.number_input('Standpipe Pressure (average)', value=0)
    
    #asking for Hookload
    Hookload = st.number_input('Force (klbf) of Hookload (average)', value=0)
    
    #asking for BlockPosition
    BlockPosition = st.number_input('Block position in feet (ft)', value=0)
    
    #asking for MudFlow
    MudFlow = st.number_input('Mud Flow Out (percentual)', value=0)
    
    if MudFlow > 0:
        
        #defining wbit
        df1_var1 = DepthBit*0.052
        Wbit = StandpipePressure/df1_var1
    
        #defining rate of penetration
        RateOfPenetration = DepthBit/DepthHole
    
        #defining downhole weight on bit
        DownholeWbit = Wbit*DepthBit
    
        #defining the difference between depth bit and depth hole
        DifHolBit = DepthHole - DepthBit
    
        #defining the Wbit Density
        WbitDens = (Wbit/9.807)*DepthBit
    
        # defining result
        result = ''
        final_result = ''
    
    if st.button('Predict'):
        
        #making the prediction
        result = predict(Wbit, Hookload, BlockPosition, DepthBit, MudFlow, RateOfPenetration, DownholeWbit,
                StandpipePressure, DifHolBit, WbitDens)
        
        # converting and showing result
        result = (np.expm1(result))
        
        if result > 0:
            
            result_final = (result/60)
                                   
            if result_final >= 3.9:
                result_min_in = math.floor(result_final*0.26)
                result_sec_in = math.floor(((((result/60)*0.26) - result_min_in)*60))
                st.success(f'\nThe slips will be placed in at: {result_min_in} minutes and {result_sec_in} seconds')
     
            elif result_final < 3.9:
                result_sec_in = math.floor(result*0.26)
                st.success(f'\nThe slips will be placed in at: {result_sec_in} seconds')
        
            result_min = math.floor(result_final)
            result_sec = math.floor(((result/60) - result_min)*60)
            st.success(f'\nThe slips will be placed out at: {result_min} minutes and {result_sec} seconds')
        
if __name__ == '__main__':
    main()
