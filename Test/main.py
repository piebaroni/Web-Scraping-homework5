import json
import matplotlib.pyplot as plt
import pandas as pd

color_of_bar = "#c8a2c8"
color_of_edge = "#000000"


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


def dict_list_to_dict_first_value(d):
    return {k: v[0] for k, v in d.items() if len(v) >= 1}


def difference(string1, string2):
    a = set(string1.split())
    b = set(string2.split())
    return a.symmetric_difference(b)


def extract_info():
    for dataset in ["ebusiness", "cmc", "govuk", "infoclipper"]:

        df = pd.read_csv("Datasets\\" + dataset + ".csv", encoding='cp1252')
        df_test = pd.read_csv("Test\\" + dataset + ".csv", encoding='cp1252', delimiter=";")

        res = []
        df_test = df_test.reset_index()
        for index, row_df_test in df_test.iterrows():

            if dataset == "ebusiness":
                url = row_df_test["URL"]
                id = url.split("/")[5]
                row_df = dict_list_to_dict_first_value(df.loc[df['URL'].str.contains(id)].to_dict(orient="list"))
            else:
                url = row_df_test["URL"]
                row_df = dict_list_to_dict_first_value(df.loc[df['URL'] == url].to_dict(orient="list"))

            tmp = {}
            for key, value in row_df_test.items():
                if key in row_df.keys() and key in row_df_test.keys():
                    diff = difference(str(row_df[key]), str(row_df_test[key]))
                    if len(diff) == 0:
                        diff = ""
                    tmp.update({
                        "SYSTEM-"+key: row_df[key],
                        "TEST-"+key: row_df_test[key],
                        "DIFF-"+key: diff
                    })
            res.append(tmp)

        df_res = pd.DataFrame(res)
        df_res.to_excel("output\\"+dataset+".xlsx", index=False)

        not_empty_cells = {}
        for row in res:
            for key, value in row.items():
                if "DIFF" in key:
                    key = key.split("-")[1]
                    if key not in not_empty_cells.keys():
                        not_empty_cells[key] = 0
                    if value != "":
                        not_empty_cells[key] += 1

        with open("json_output\\"+dataset+".json", "w") as outfile:
            json.dump(not_empty_cells, outfile, indent=4)


def plot():
    for dataset, v in {"ebusiness": 30, "cmc": 30, "govuk": 29, "infoclipper": 50}.items():
        with open("json_output\\" + dataset + ".json", "r") as infile:
            not_empty_cells = json.load(infile)
        keys = list(not_empty_cells.keys())
        values = list(not_empty_cells.values())
        bar_plot(keys, values, dataset, "plot\\" + dataset + ".png", (15, 5), True, v)


if __name__ == '__main__':
    #extract_info()
    plot()

