import pandas as pd
import matplotlib.pyplot as plt


subject = 8
character = 8
finger = "index"
glyph = None

pd.set_option('display.max_rows', None)

relevant_data=["ZSTROKE", "ZTIMESTAMP", "ZGLYPH", "ZARCLENGTH", "ZDURATION", "ZX", "ZY"]

df_subject = pd.read_csv('subject.csv', sep=',')
df_glyph = pd.read_csv('glyph.csv', sep=",")
df_strokes = pd.read_csv('stroke.csv', sep=",")
df_touchs = pd.read_csv('touch.csv', sep=",")


def show_data(x_values, y_values):

    for stroke in range(len(x_values)):
        x_values_one_stroke = x_values[stroke]
        y_values_one_stroke = y_values[stroke]
        plt.plot(x_values_one_stroke, y_values_one_stroke, marker="o", label=f"stroke {stroke}", zorder=0)
        plt.scatter(x_values_one_stroke[0], y_values_one_stroke[0], zorder=1, label="first point of stroke",
                    color="purple")
        plt.legend()

    plt.show()


def retrieve_data(subject = 8, character = 8, finger = "index", glyph = None):
    x_values = []
    y_values =[]
    timestamps = []
    result = pd.merge(df_touchs, df_strokes, left_on='ZSTROKE', right_on='Z_PK', how='inner')
    relevant_result = result[relevant_data]
    glyph_result = pd.merge(relevant_result, df_glyph, left_on='ZGLYPH', right_on='Z_PK', how='inner')
    relevant_data2 = ["ZSUBJECT", "ZGLYPH", "ZCHARACTER", "ZFINGER", "ZSTROKE", "ZTIMESTAMP", "ZX", "ZY"]
    relevant_glyph_result = glyph_result[relevant_data2]

    condition = (relevant_glyph_result["ZSUBJECT"] == subject) & \
                (relevant_glyph_result["ZCHARACTER"] == character) & \
                (relevant_glyph_result["ZFINGER"] == finger)
    filterd_glyph_data = relevant_glyph_result[condition]
    filterd_glyph_data = filterd_glyph_data.sort_values(by=["ZSTROKE", "ZTIMESTAMP"])  # sort

    condition2 = (filterd_glyph_data["ZGLYPH"] == filterd_glyph_data["ZGLYPH"].iloc[0])
    one_glyph_data = filterd_glyph_data[condition2]

    for i in one_glyph_data["ZSTROKE"].unique():
        filtered_one_glyph_data = one_glyph_data[one_glyph_data["ZSTROKE"] == i]

        x_values_one_stroke = filtered_one_glyph_data["ZX"].to_numpy()
        y_values_one_stroke = filtered_one_glyph_data["ZY"].to_numpy()
        timestamps_one_stroke = filtered_one_glyph_data["ZTIMESTAMP"].to_numpy()

        x_values.append(x_values_one_stroke)
        y_values.append(-y_values_one_stroke)
        timestamps.append(timestamps_one_stroke)
    for stroke in x_values:
        if len(stroke)<10:
            print(f"strokes too short: {subject}, {character}")
            break
    return x_values, y_values, timestamps


if __name__ == '__main__':
    X, Y, _= retrieve_data(3, 3)
    show_data(X, Y)
