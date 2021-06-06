import pickle
import streamlit as st
import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
import datetime

#load the trained model
model = pickle.load(open('rf_tuned.pkl', 'rb'))

# defining the prediction function
def prediction(Amount, OrigimOldBalance, DestinyNewBalance, DestinyOldBalance, HourofDay, DayofWeek,
                ZeroNewDest, ZeroOldDest, FlaggedFraud, type_CASH_OUT, type_TRANSFER):

    # making the prediction
    yhat = model.predict([[Amount, OrigimOldBalance, DestinyNewBalance, DestinyOldBalance, HourofDay, DayofWeek,
                ZeroNewDest, ZeroOldDest, FlaggedFraud, type_CASH_OUT, type_TRANSFER]])
    
    # giving the answer
    prediction = (yhat)
    
    return prediction
    
def main():
    st.header('Fraud Detector')
    st.text("By: Valcilio Silva Junior (Data Scientist)")
    
    # defining Amount and FlaggedFraud
    Amount = st.number_input('Total amount of this transaction', value=0)
    
    if Amount >= 200000:
        FlaggedFraud = 1
        
    elif Amount < 200000:
        FlaggedFraud = 0
    #FlaggedFraud = Amount.apply(lambda x: 1 if x >= 200000 else 0)
        
    # defining Origim Balances
    OrigimOldBalance = st.number_input('Original amount of the origim account', value=0)
    DestinyOldBalance = st.number_input('Original amount of the destiny account', value=0)
    DestinyNewBalance = st.number_input('Pos transaction amount of the destiny account', value=0)
    if DestinyNewBalance == 0:
        ZeroNewDest = 1
        
    elif DestinyNewBalance > 0:
        ZeroNewDest = 0
    #ZeroNewDest = DestinyNewBalance.apply(lambda x: 1 if x == 0 else 0)
    
    if DestinyOldBalance == 0:
         ZeroOldDest = 1
        
    elif DestinyOldBalance > 0:
        ZeroOldDest = 0
    #ZeroOldDest = DestinyOldBalance.apply(lambda x: 1 if x == 0 else 0)
    
    # defining date variables
    DayofWeek = st.selectbox('Day of the transaction (0 - monday, 1 - tuesday, 2 - wednesday, 3 - thursday, 4 - friday, 5 - saturday, 6 - sunday', 
    [0, 1, 2, 3, 4, 5, 6])
    HourofDay = st.number_input('Hour of the transaction', value=0)
    
    # defining type transaction
    Type = st.selectbox('Type of the transaction', ['Cash Out', 'Transfer'])
    
    if Type == 'Cash Out':
    	CashOut = 1
    	
    elif Type != 'Cash Out':
    	CashOut = 0
    	
    if Type == 'Transfer':
    	Transfer = 1
    	
    elif Type != 'Transfer':
    	Transfer = 0
    
    
    #CashOut = st.selectbox('The transaction was a Cash Out? 0 - no, 1- yes', [0, 1])
    #Transfer = st.selectbox('The transaction was a Transfer? 0 - no, 1 - yes', [0, 1])
    
    # defining result
    result = ''
    final_result = ''
    
    if st.button('Predict'):
        #making the prediction
        result = prediction(Amount, OrigimOldBalance, DestinyNewBalance, DestinyOldBalance, HourofDay, DayofWeek,
                ZeroNewDest, ZeroOldDest, FlaggedFraud, CashOut, Transfer)
        
        # converting and showing result
        
        if result == 1:
        	result_final = 'fraud'
        	
        elif result == 0:
        	result_final = 'legitimate'
        	
        st.success('The transaction is: {}'.format(result_final))
        
if __name__ == '__main__':
    main()
