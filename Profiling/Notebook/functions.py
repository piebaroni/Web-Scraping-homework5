import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import string
from matplotlib_venn import venn3, venn3_circles
import matplotlib.colors
import geopandas as gpd
from matplotlib_venn import venn3, venn3_circles
from itertools import combinations

blu_fiordaliso = "#6495ED"
blu_fiordaliso_chiaro = "#93CCEA"
verde_primavera = "#00FF7F"
lilla = "#c8a2c8"
color_of_bar = "#c8a2c8"
color_of_edge = "#000000"
gradient1 = ["#ebc4eb", "#dfb8df", "#d4add4", "#c8a2c8", "#bd97bd", "#b18cb1", "#a681a6"]
gradient2 = ["#ffffff", "#dcc4dc","#c8a2c8", "#a787ad", "#93779c", "#735d82", "#6c4675"]
gradient = ["#ffffff", "#d4add4", "#c8a2c8", "#a681a6"]
my_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", gradient2)

# restituisce una stringa casuale data una lunghezza
def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
	
# toglie gli gli \n dal csv
def clean_csv(csv1, csv2):
    file1 = open(csv1, 'r')
    file2 = open(csv2, 'w')

    lines = file1.readlines()

    for line in lines:
        if line != "\n":
            file2.writelines(line)

    file1.close()
    file2.close()

# funzione di utilita per count_type_in_list(), serve a convertire una stringa in int o float
def maybeMakeNumber(s):
    # handle None, "", 0
    if s is np.nan:
        return None
    if s is pd.NA:
        return None
    else:
        if not isinstance(s, float):
            try:
                return int(s)
            except:
                try:
                    return float(s)
                except:
                    return s
        else:
            return s
			
# conta il numero di int, float e str in una lista di stringhe
def count_type_in_list(l):
    info = {}
    converted = list(map(maybeMakeNumber, l))
    converted = [0 if isinstance(x, int) else x for x in converted]
    converted = [1 if isinstance(x, float) else x for x in converted]
    converted = [2 if isinstance(x, str) else x for x in converted]
    info["numero int"] = converted.count(0)
    info["numero float"] = converted.count(1)
    info["numero str"] = converted.count(2)
    return info
	
# estrazione dati da un dataframe 
def extract_data_from_df(df):
    info = {}
    info["numero righe"] = df.shape[0]
    info["numero colonne"] = df.shape[1]
    info["numero celle"] = df.shape[0] * df.shape[1]
    info["numero celle nulle"] = df.isnull().sum().sum()
    info["numero righe con celle nulle"] = (df.isnull().sum(axis=1) != 0).sum()
    info["numero colonne con celle nulle"] = (df.isnull().sum(axis=0) != 0).sum()
    info["numero celle int"] = 0
    info["numero celle float"] = 0
    info["numero celle str"] = 0
    info["numero colonne int"] = 0
    info["numero colonne float"] = 0
    info["numero colonne str"] = 0
    for key in df:
        column = list(df[key])
        info_type = count_type_in_list(column)
        not_value_column = len(list(filter(lambda x: x is not np.nan and x is not pd.NA, column)))
        info["numero celle int"] += info_type["numero int"]
        info["numero celle float"] += info_type["numero float"]
        info["numero celle str"] += info_type["numero str"]
        if not_value_column == info_type["numero int"]:
            info["numero colonne int"] += 1
        elif not_value_column == info_type["numero float"]:
            info["numero colonne float"] += 1
        elif not_value_column == info_type["numero str"]:
            info["numero colonne str"] += 1
    return info
	
# plot diagrammi di venn di tre insiemi
def venn_plot(subset, key_set, path, dim=(5,5)):
    plt.figure(figsize=dim) 
    venn3(
        subsets = subset,
        set_labels = key_set,
        set_colors=("#FF0000", "#00FF00", "#0000FF"), 
        alpha = 0.5
    )
    venn3_circles(
        subsets = subset,
        linestyle='-', 
        linewidth=1, 
        color=color_of_edge
    )
    plt.savefig(path, bbox_inches='tight', transparent=True)
    plt.show()

# plot distribuzioni di valori con bar chart
def distribution_plot(x, y, x_label, y_label, title, path, dim):
    plt.figure(figsize=dim) 
    plt.grid(color=color_of_edge, linestyle='-', linewidth=0.5, axis="y")
    plt.yscale("log")
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.fill_between(
        x, 
        y,
        color=color_of_bar, 
        edgecolor=color_of_edge, 
        linewidth=1
    )
    plt.savefig(path, bbox_inches='tight', transparent=True)
    plt.show()

# plot di bar chart
def bar_plot(keys, values, title, path = "plot.png", dim = (7,4), bar_label = False, v_max = None):
    plt.figure(figsize=dim) 
    #plt.yscale("log")
    plt.title(title)
    p = plt.bar(
        keys, 
        values, 
        width= 0.5, 
        color=color_of_bar, 
        edgecolor=color_of_edge, 
        linewidth=1, 
        align='center'
    )
    if bar_label:
        plt.bar_label(p, label_type='edge')
        plt.xticks(rotation = 45, ha='right', rotation_mode='anchor')
        plt.margins(y=0.2)
        if v_max != None:
            plt.grid(color=color_of_edge, linestyle='-', linewidth=0.5, axis="y")
            l = "{:,}".format(v_max)
            l = l.replace(',', '.')
            plt.yticks([v_max], [l])
        else:
            plt.tick_params(left = False, labelleft = False)
    else:
        labels = ["{:,}".format(elem) for elem in values]
        labels = list(map(lambda x: x.replace(',', '.'), labels))
        plt.yticks(values, labels)
        plt.grid(color=color_of_edge, linestyle='-', linewidth=0.5, axis="y")
    plt.savefig(path, bbox_inches='tight', transparent=True)
    plt.show()
	
# plot bar chart esteso
def bar_plot_ex(keys, values, title, path, dim):
    plt.figure(figsize=dim) 
    plt.grid(color=color_of_edge, linestyle='-', linewidth=0.5, axis="y")
    plt.yscale("log")
    plt.title(title)
    p = plt.bar(
        keys, 
        values, 
        width=1, 
        color=color_of_bar, 
        edgecolor=color_of_edge, 
        linewidth=0.5, 
        align='center'
    )
    plt.xticks(rotation = 90)
    plt.savefig(path, bbox_inches='tight', transparent=True)
    plt.show()

# plot di dati su mappa geografica con geopandas
def map_plot(map_df, column_to_plot, column_label, column_geometry, resize, label, path):
    fig, ax = plt.subplots(figsize=(20, 15))
    ax.set_axis_off()
    min_value_of_column = 0 #min(map_df[column_to_plot])
    max_value_of_column = max(map_df[column_to_plot])
    step = int((max_value_of_column - min_value_of_column) / resize)
    map_df.plot(
        ax=ax, 
        column=column_to_plot, 
        cmap=my_cmap,
        legend=True, 
        linewidth=0.5,
        edgecolor='black',
        legend_kwds={
            'label': label, 
            'orientation': "vertical", 
            "shrink": 0.5,
            'ticks': np.arange(min_value_of_column, max_value_of_column, step)
        },
        missing_kwds={
            "color": "lightgrey",
            "edgecolor": "red",
            "hatch": "///",
            "label": "Missing values",
        }
    )
    x = plt.xlim()
    y = plt.ylim()
    map_df['coords'] = map_df[column_geometry].apply(lambda x: x.representative_point().coords[:])
    map_df['coords'] = [coords[0] for coords in map_df['coords']]
    for idx, row in map_df.iterrows():
        plt.annotate(
            row[column_label], 
            xy=row['coords'], 
            horizontalalignment='center',
            size=14,
            color="#000000",
            #xytext=(0, row['coords'][1]),
            #arrowprops = dict(
            #    facecolor = color_of_edge,
            #    shrink = 1,
            #    width = 0.2,
            #    headwidth = 5,
            #    headlength = 5
            #),
            #xycoords="data"
        )
    plt.savefig(path, bbox_inches='tight', transparent=True)

# calcola l'intersezione di tre liste o set
def intersection3(l1, l2, l3):
    l1 = set(l1)
    l2 = set(l2)
    l3 = set(l3)
    i1 = l1.difference(l2).difference(l3)
    i2 = l2.difference(l1).difference(l3)
    i3 = l3.difference(l1).difference(l2)
    i123 = l1.intersection(l2, l3)
    i12 = l1.intersection(l2).difference(i123)
    i13 = l1.intersection(l3).difference(i123)
    i23 = l2.intersection(l3).difference(i123)
    return {"100":len(i1), "010":len(i2) , "001":len(i3) , "110":len(i12), "101":len(i13), "011":len(i23), "111":len(i123)}

# set1 = {1, 2, 3, 4, 5}
# set2 = {4, 5, 6, 7, 1}
# set3 = {6, 7, 8, 9, 10, 1}
# set4 = {1, 8, 9, 15}
# sets = {"s1": set1, "s2": set2, "s3": set3, "s4": set4}
# or
# sets = {"s1": list1, "s2": list2, "s3": list3, "s4": list4}
def n_intersection(sets):
    # algoritmo per calcolare l'intersezione fra tutte le possibili tuple dei sets
    res = []
    for i in range(1,len(sets)+1):
        for s in list(combinations(sets, i)):
            set_intersection = set(sets[s[0]])
            for j in range(1,i):
                set_intersection = set_intersection.intersection(set(sets[s[j]]))
            res.append([s, set_intersection])    
    diff = []
    # sottrazione per insieme mutuamente esclusivi A - A !U B - A !U C
    for n_tuple in range(1,len(sets)+1):
        lst = [e for e in res if len(e[0])==n_tuple]
        for tup_companies in lst:
            for index in range(0,len(res)):
                if tup_companies[0] != res[index][0] and set(tup_companies[0]).issubset(set(res[index][0])):
                    tup_companies[1] = tup_companies[1].difference(res[index][1])
            diff.append([tup_companies[0], len(tup_companies[1])])
    return diff


