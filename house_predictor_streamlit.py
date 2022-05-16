from re import L
import streamlit as st
import json
import pickle
import datetime
import pandas as pd

st.title("House price predictor application", anchor=None)
form = st.form(key="annotation")

construction_status = {
      'construction_status__Under Construction':0 ,
      'construction_status__Ready to move':0
   }
new_resale_status = {
      'new_resale__New':0 ,
      'new_resale__Resale':0,
      'new_resale__old':0
   }
house_type = {
      'house_type__Apartment':0,
      'house_type__Independent Floor':0,
      'house_type__Independent House':0,
      'house_type__Penthouse':0, 
      'house_type__Studio Apartment':0,
      'house_type__Villa':0
   }
with form:
    #Personal details
    # st.subheader("Personal details: ")
    with open('d_region_loc.json') as json_file:
      d_region_loc = json.load(json_file)
    
    l_regions = d_region_loc.keys()
    
    s_region_selected = st.selectbox(
       "Select the region: ", l_regions, index=12
    )
    
    l_locality = []
    for i in d_region_loc.values():
       l_locality=l_locality+i
       
    s_locality_selected = st.selectbox(
       "Select the nearest locality: ", l_locality
    )
    
    i_area_selected = st.number_input("Enter the area of house in sq/ft", step=1,)
    i_rooms_selected = st.number_input("Enter the number of rooms of house", step=1,)
    i_beds_selected = st.number_input("Enter the number of beds of house", step=1,)
    date_of_possession = st.date_input("Enter the expected or actual date of possession of the property" ,min_value=datetime.date(1990, 1, 1))
    
    s_construct_status_selected = st.selectbox(
       "Select the construction status: ",['Under Construction', 'Ready to move'], index=0
    )
    s_new_resale_selected =  st.selectbox(
       "Select the new/resale status: ",['New', 'Resale', 'old'], index=0
    )
    s_house_type_selected =  st.selectbox(
       "Select the house type: ",['Apartment', 'Independent House', 'Villa', 'Studio Apartment','Independent Floor', 'Penthouse'], index=0
    )
    
    submitted = st.form_submit_button(label="Predict the price in crores")


if submitted:
   print("submitted", submitted)
   xgb_model = pickle.load(open("xgb_house_predict.pkl", 'rb'))
   
   with open('d_loc_enc.json') as json_file:
      d_loc_enc = json.load(json_file)
      
   with open('d_reg_enc.json') as json_file:
      d_reg_enc = json.load(json_file)
      
   construction_status['construction_status_'+'_'+ s_construct_status_selected] = 1
   new_resale_status['new_resale_'+'_'+ s_new_resale_selected] = 1
   house_type['house_type_'+'_'+ s_house_type_selected] = 1
   
   test = pd.DataFrame(dict(zip(['locality_name', 'region_name', 'area', 'total_rooms', 'total_beds',
       'age', 'construction_status__Ready to move', 'construction_status__Under Construction', 'new_resale__New',
       'new_resale__Resale', 'new_resale__old', 'house_type__Apartment',
       'house_type__Independent Floor', 'house_type__Independent House',
       'house_type__Penthouse', 'house_type__Studio Apartment',
       'house_type__Villa'],[[d_loc_enc[s_locality_selected]],[d_reg_enc[s_region_selected]],[i_area_selected],[i_rooms_selected],[i_beds_selected],[date_of_possession.year],[construction_status['construction_status__Under Construction']],
         [construction_status['construction_status__Ready to move']], [new_resale_status['new_resale__New']], [new_resale_status['new_resale__Resale']],[new_resale_status['new_resale__old']],
        [house_type['house_type__Apartment']],[house_type['house_type__Independent Floor']],[house_type['house_type__Independent House']],[house_type['house_type__Penthouse']],[house_type['house_type__Studio Apartment']]
        ,[house_type['house_type__Villa']]                   
                             ])))
   price = xgb_model.predict(test)[0]
   print(price)
   st.header('The predicted price of the house is: {}'.format(price))

expander = st.expander("See all records")