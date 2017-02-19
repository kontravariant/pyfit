import json
import os


def compile():
    data_list = []
    for file in os.listdir("data/"):
        with open("data/" + file) as df:
            data_list.append( json.load(df) )
    return(data_list)

def averages(all_data):
    outset = {}
    for dataset in all_data:
        for key in dataset.keys():
            date = key
            lift_avg = {}
            for lift, sets in dataset[date].items():
                allwts = []
                for set,wt_reps in sets.items():
                    if wt_reps[1] != 0 and wt_reps[0] !=0:
                        allwts.append(wt_reps[0])
                if len(allwts):
                    lift_avg[lift] = sum(allwts)/len(allwts)
        outset[date] = lift_avg
    print(outset)

