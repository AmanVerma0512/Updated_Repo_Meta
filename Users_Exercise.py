#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import matplotlib.pyplot as plt
import numpy as np
import yaml
from Updated_Scores import get_score
import pandas as pd
import boto3
import streamlit as st
st.set_page_config(layout="wide")

st.title("Last Exercise Activity System")

s3_client = boto3.client('s3')
s3_bucket_name = 'forgefait'
s3_client = boto3.client('s3')
s3_bucket_name = 'forgefait'
s3 = boto3.resource('s3',
                     aws_access_key_id = st.secrets["aws_access_key_id"],
                     aws_secret_access_key = st.secrets["aws_secret_access_key"])

@st.experimental_singleton
def load_data():
    print('Object Initialised')
    content_object = s3.Object('forgefait', 'new_data.json')
    file_content = content_object.get()['Body'].read().decode('utf-8')
    print('File Read')

    data = yaml.safe_load(file_content)
    print('File Converted to JSON')
    return data

data = load_data()

name_fields_array = []
date_fields_array = []

for idx, elem in enumerate(data):
    name_fields_array.append(elem['name'])

# st.title("Last Users Activity System")
user_name = st.selectbox('Enter the ID you want to check Last Activity for?',name_fields_array,key="user_name")

curr_elem_idx = 0
flag = False
for idx, elem in enumerate(data):
    if elem['name'] == user_name:
        curr_elem_idx = idx
        flag = True

date_fields_array = list(data[curr_elem_idx]['exercises'].keys())
exercise_date = st.selectbox('Enter the Last Activity Date?',date_fields_array,key="date")

last_exercise_activity = []
for act_elem in data[curr_elem_idx]['exercises']:
    if act_elem == exercise_date:
        for exercise_elem in data[curr_elem_idx]['exercises'][act_elem]:
            last_exercise_activity.append(exercise_elem)

exercise_list = [elem['exerciseName'] for elem in last_exercise_activity]
exercise_name = st.selectbox('Enter the Last Activity Exercise Name?',exercise_list,key="exer_name")

meta_tag = st.selectbox("Display Meta Values?",["False","True"],key="meta_tag")


curr_exercise_idx = 0
for idx, act_elem in enumerate(last_exercise_activity):
    if act_elem['exerciseName'] == exercise_name:
        curr_exercise_idx = idx


exercise = last_exercise_activity[curr_exercise_idx]


if flag == True:
    st.header("Exercise Details")
    col1, col2 = st.columns(2)
    exercise_name = exercise['exerciseName']
    date = exercise['id']
    dailypower = int(exercise['dailyPower'])
    x = exercise['workoutData']
    workoutData = list(map(int, x))
    peakforce = int(exercise['peakForce'])
    bps = int(exercise['bestPowerSet'])
    # Exercise Details
    with col1:

        st.subheader("Exercise Info")
        st.write("Client's Name: " + str(user_name))
        st.write("Exercise Name: " + str(exercise_name))
        st.write("Date: " + str(date))

    with col2:

        st.subheader("Exercise Scores")
        st.write("Daily Power: " + str(dailypower))
        st.write("Peak Force: " + str(peakforce))
        st.write("Best Power Set: " + str(bps))

    st.subheader("Exercise Plot")
    chart_data = pd.DataFrame(
    np.array(workoutData),
    columns=['workout'])
    st.line_chart(chart_data)
    
    header={
        "subScores":True,
        "coachingTip":True,
        "score":True,
        "meta":True
    }

    h_params={
                            "global_score": 25,
                            "setting":"experiment",
                             "bwt": 60,
                             "gender": "men's",
                             "exercise_mode": "Equipped Powerlifting",
                             "l0": 1,
                             "l1": 1,
                             "l2": 1,
                             "l3": 1,
                             "power":{
                                 "w_power": 1,
                                 "w_explosiveness": 1,
                                  "peaks": {
                                      "sz": 12,
                                      "max_win": 100
                                  },

                                  "mode": {
                                      "sz": 12
                                  },
                                "power":{
                                    "growth factor":1.15,
                                     "bwt": 60,
                                     "gender": "men's",
                                     "exercise_mode": "Equipped Powerlifting",
                                     "scipyPeaks":False,
                                     "intervalPeaks":None
                                     # "peaks": {
                                     #     "sz": 12,
                                     #     "max_win": 100
                                     # },
                                 },
                                 "explosiveness":{
                                     "scipyPeaks":False,
                                     "intervalPeaks":None
                                     # "peaks": {
                                     #     "sz": 12,
                                     #     "max_win": 100
                                     # },
                                 }
                             },

                             "formScore":{
                                "w_jitter": 1,
                                "w_tempo": 1,
                                "w_sudden release": 1,
                                "sudden release": {
                                    "max_to_fall_ratio": 0.4,
                                    "fall_time": 4
                                },
                                "tempo":{
                                    "scipyPeaks":False,
                                    "intervalPeaks":False
                                },
                                "peaks": {
                                    "sz": 12,
                                    "max_win": 100
                                },
                                "jitter": {
                                    "window_size": 4,
                                    "delta": 2,
                                    "t0": 2,
                                    "x_dist_rel": 0.2,
                                    "jitterPolicyThreshold":4,
                                    "scipyPeaks":False,

                                    # "smoothBlips": {
                                    #     "smoothenFactor": 2,
                                    #     "prominentPeaksProminence":0.5,
                                    #     "prominentPeaksWidth":2,
                                    #     "smallPeaksHeightLowerFactor":0.6,
                                    #     "smallPeaksHeightHigherFactor":0.8,
                                    #     "smallPeaksWidth":2
                                    # }
                                },

                                "peaks": {
                                    "sz": 12,
                                    "max_win": 100
                                },

                                "mode": {
                                    "sz": 12
                                },
                             },

                             "stamina":{
                                "w_ring stamina": 1,
                                "w_area stamina": 1,
                                "w_total time":1,
                                "peaks": {
                                    "scipyPeaks":False,
                                    "intervalPeaks":None,
                                    "sz": 12,
                                    "max_win": 100
                                },
                                "area stamina":
                                {
                                    "referenceFactor":1.4,
                                    "peaks":{
                                    "scipyPeaks":False,
                                    "intervalPeaks":None
                                    # "peaks": {
                                    #     "sz": 12,
                                    #     "max_win": 100
                                    # },
                                    }
                                },
                                "total time":
                                {
                                    "referenceFactor":1.4,
                                    "peaks":{
                                    "scipyPeaks":False,
                                    "intervalPeaks":None
                                    # "peaks": {
                                    #     "sz": 12,
                                    #     "max_win": 100
                                    # },
                                    }
                                },
                                "ring stamina":{
                                    "baseBased":False,
                                    "peakBased":{
                                        "power_ref":0.8,
                                        "time_ref":200
                                    }
                                },
                                "peaks":{
                                     "scipyPeaks":False,
                                     "intervalPeaks":None
                                     # "peaks": {
                                     #     "sz": 12,
                                     #     "max_win": 100
                                     # },
                                     },
                                 "mode": {
                                     "sz": 12
                                 },
                             },

                             "discount": 0.9,
                             "peaks": {
                                 "sz": 12,
                                 "max_win": 100
                             },

                             "mode": {
                                 "sz": 12
                             },

                             "print": 0,
                             "plot": 0,
                             "log_dir": "D:/Forge/Forge/jupyter/formscore-log/",
                             }
    score_object = get_score(workoutData,h_params,header)
    score_object = score_object['scores']
    agg_power = score_object["agg power"]
    stamina = score_object["stamina"]
    formscore = score_object["formscore"]
    total_time = score_object['total time']
    
    st.subheader("Model Calculated Scores")
    
    col3, col4, col5 = st.columns(3)

    with col3:

        st.write("AGGREGATE POWER SCORES")
        st.write("Explosiveness Score: " + str(round(agg_power['subScores']['explosiveness']['score'],2)))
        st.write("Explosiveness Coaching Tip: " + str(agg_power['subScores']['explosiveness']['coachingTip']))
        st.write("Power Score: " + str(round(agg_power['subScores']['power']['score'],2)))
        st.write("Power Coaching Tip: " + str(agg_power['subScores']['power']['coachingTip']))
        st.write("Net Score: " + str(round(agg_power['score'],2)))
        st.write("Net Coaching Tip: " + str(agg_power['coachingTip']))

    with col4:

        st.write("STAMINA SCORES")
        st.write("Total Time Score: " + str(round(total_time['score'],2)))
        st.write("Total Time Coaching Tip: " + str(total_time['coachingTip']))
        st.write("Area Stamina Score: " + str(round(stamina['subScores']['area stamina']['score'],2)))
        st.write("Area Stamina Coaching Tip: " + str(stamina['subScores']['area stamina']['coachingTip']))
        st.write("Net Score: " + str(round(stamina['score'],2)))
        st.write("Net Coaching Tip: " + str(stamina['coachingTip']))

    with col5:
        
        st.write("FORM SCORES")
        st.write("Sudden Release Score: " + str(round(formscore['subScores']['sudden release']['score'],2)))
        st.write("Sudden Release Coaching Tip: " + str(formscore['subScores']['sudden release']['coachingTip']))
        st.write("Tempo Score: " + str(round(formscore['subScores']['tempo']['score'],2)))
        st.write("Tempo Coaching Tip: " + str(formscore['subScores']['tempo']['coachingTip']))
        st.write("Jitter Score: " + str(round(formscore['subScores']['jitter']['score'],2)))
        st.write("Jitter Coaching Tip: " + str(formscore['subScores']['jitter']['coachingTip']))
        st.write("Net Score: " + str(round(formscore['score'],2)))
        st.write("Net Coaching Tip: " + str(formscore['coachingTip']))
        
    st.subheader("Meta Values: Set to " + str(meta_tag))
    
    if meta_tag == "True":
        col6, col7, col8 = st.columns(3)

        with col6:

            st.write("AGGREGATE POWER META VALUES")
            st.write("A. Explosiveness ")
            st.write("Base/Mode: " + str(round(agg_power['subScores']['explosiveness']['meta']['base/mode'],2)))
            st.write("Average Ascent: " + str(round(agg_power['subScores']['explosiveness']['meta']['average ascent'],2)))
            st.write("Peak Value Used: " + str(round(agg_power['subScores']['explosiveness']['meta']['peak value used'],2)))

            st.write("B. Power")
            st.write("Power: " + str(round(agg_power['subScores']['power']['meta']['power'],2)))
            st.write("Power Reference From History: " + str(round(agg_power['subScores']['power']['meta']['powerReferenceFromHistory'],2)))

        with col7:

            st.write("STAMINA META VALUES")
            st.write("A. Time ")
            st.write("Start/End: " + str(total_time['meta']['start,end']))
            st.write("Low Filter: " + str(round(total_time['meta']['low_filter'],2)))
            st.write("B. Stamina ")
            st.write("Total Power/Area: " + str(round(stamina['subScores']['area stamina']['meta']['total power/area'],2)))
            st.write("Length: " + str(round(stamina['subScores']['area stamina']['meta']['length'],2)))
            st.write("Ideal Power/Reference x Length: " + str(round(stamina['subScores']['area stamina']['meta']['ideal power/reference x length'],2)))

        with col8:
            st.write("FORM META VALUES")
            st.write("A. Sudden Release")
            st.write("Max To Fall Ratio: " + str(round(formscore['subScores']['sudden release']['meta']['max_to_fall_ratio'],2)))
            st.write("Fall Time: " + str(round(formscore['subScores']['sudden release']['meta']['fall_time'],2)))
            st.write("Points: " + str(formscore['subScores']['sudden release']['meta']['points']))
            st.write("B. Tempo")
            st.write("Peaks: " + str(formscore['subScores']['tempo']['meta']['peaks']))
            st.write("Current Tempo: " + str(formscore['subScores']['tempo']['meta']['curr_tempo']))
            st.write("Average: " + str(round(formscore['subScores']['tempo']['meta']['avg'],2)))
            st.write("Current Score: " + str(round(formscore['subScores']['tempo']['meta']['currScore'],2)))
            st.write("C. Jitter")
            st.write("Per Rep Jitter Dictionary: " + str(formscore['subScores']['jitter']['meta']['per rep jitter dictionary']))