import pickle
import streamlit as st
import numpy as np
import math
from sklearn.ensemble import RandomForestRegressor

#load the trained model
model = pickle.load(open('rf_tuned.pkl', 'rb'))

# defining the prediction function
def prediction(Wbit, Hookload, BlockPosition, DepthBit, MudFlow, RateOfPenetration, DownholeWbit,
                StandpipePressure, DifHolBit, WbitDens):

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
        result = prediction(Wbit, Hookload, BlockPosition, DepthBit, MudFlow, RateOfPenetration, DownholeWbit,
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
