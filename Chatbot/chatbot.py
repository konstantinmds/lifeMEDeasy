import os
import pickle
import csv
import re
from numpy.random import randint 

starter = [
        "Hi there! I am a medical chatbot. We can help you with diagnosing your symptoms online. Would you like to tell us?"     
        ]


with open("dataset/label.pickle", "rb") as f:
    setLabels = pickle.load(f) 

with open('dataset/best_svc.pickle', 'rb') as output:
    best_svc = pickle.load(output)

with open("dataset/tdf.pickle", "rb") as f:
    tf = pickle.load(f) 


convert = dict(enumerate(setLabels))


def tryPredict(data):
    data = [data]
    testData = tf.transform(data).toarray()
    s = best_svc.predict(testData)
    return (convert[s[0]]) 

symptoms_list = []
disease_list = []

def cleanText(datalist):
    f = "[_]"
    sent = []
    for each in datalist:
        x = re.split(f, each)
        sent.extend(iter(x)) 

    return sent 

with open("dataset/dataset.csv") as f:
    dataFile = csv.reader(f, delimiter=",")

    for countVal, row in enumerate(dataFile):
        if countVal != 0:
            disease_list.append(row[0].lower().lstrip().rstrip())
            d = [each.lower().lstrip().rstrip() for each in row[1:] if each != ""]

            l = cleanText(d)
            for each in l: symptoms_list.append(each)

precaution_list = {}

with open("dataset/symptom_precaution.csv") as f:
    dataFile = csv.reader(f, delimiter=",")

    for countVal, row in enumerate(dataFile):
        if countVal != 0:
            diseaseName = row[0].lower().lstrip().rstrip()
            d = [each.lower().lstrip().rstrip() for each in row[1:] if each != ""]

            precaution_list[diseaseName] = d

def cleanWord(word):
    f = "[_]"
    x = re.split(f, word)
    return list(x) 


severityIndex = {} # 4.2222 being the mean value, 1 -> lowest, 7 -> highest  
# set mean as 4 or 5 

with open("dataset/Symptom-severity.csv") as f:
    dataFile = csv.reader(f, delimiter=",")
    for countVal, row in enumerate(dataFile):
        if countVal != 0:
            diseaseName = row[0].lower()
            sevVal = row[1]
            diseaseName = cleanWord(diseaseName)
            for each in diseaseName:
                severityIndex[each] = int(sevVal)

diseaseDesc = {}

with open("dataset/symptom_Description.csv") as f:
    dataFile = csv.reader(f, delimiter=",")
    for countVal, row in enumerate(dataFile):
        if countVal != 0:
            diseaseName = row[0].lower()
            desc = row[1]
            diseaseName = diseaseName.split()
            for each in diseaseName:
                diseaseDesc[each] = desc 

#text = "I have got fever since a few days. Headache as well. an a stomach pain"


while True:
    # TODO: NORMAL CHATTING. Greeting 
    text = str(input(":"))
    if text == "bye":
        break
    #text = "I have been suffering from dry throat, difficulty in breathing"

    text = text.lower().split()

    identified_symptoms = [each for each in text if each in symptoms_list]
    s = " ".join(identified_symptoms)
    pred_disease = tryPredict(s)

    appointment_necessity = any(
        severityIndex[each] > 5 for each in identified_symptoms
    )
    #appointment_necessity = False # TODO: remove this
    if appointment_necessity:
        print("we think it's is a serious case given your symptoms so, please pick and appointment")
        print("possible disease is: ", pred_disease)
    else:
        print("disease is:", pred_disease) 
        # precaution to be taken 
        random_number = randint(0,3)
        print(precaution_list[pred_disease][random_number])








