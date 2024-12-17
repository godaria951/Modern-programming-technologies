from spyre import server
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import requests

save_dir = "files"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

NOAAIndex = {
    1: 24,
    2: 25,
    3: 5,
    4: 6,
    5: 27,
    6: 23,
    7: 26,
    8: 7,
    9: 11,
    10: 13,
    11: 14,
    12: 15,
    13: 16,
    14: 17,
    15: 18,
    16: 19,
    17: 21,
    18: 22,
    19: 8,
    20: 9,
    21: 10,
    22: 1,
    23: 3,
    24: 2,
    25: 4,
    26: 12,  # for Kyiv
    27: 20  # for Sevastopol
}

class StockExample(server.App):
    title = "NOAA data visualization"

    inputs = [
        {"type": 'dropdown',
         "label": 'NOAA data dropdown',
         "key": 'ticker',
         "action_id": "update_data",
         "options": [{"label": "VCI", "value": "VCI"},
                     {"label": "TCI", "value": "TCI"},
                     {"label": "VHI", "value": "VHI"}]},

        {"type": 'dropdown',
         "label": 'Province',
         "key": 'region_index',
         "action_id": "update_data",
         "options": [{"label": "Vinnytsya", "value": "1"},
                     {"label": "Volyn", "value": "2"},
                     {"label": "Dnipropetrovsk", "value": "3"},
                     {"label": "Donetsk", "value": "4"},
                     {"label": "Zhytomyr", "value": "5"},
                     {"label": "Transcarpathia", "value": "6"},
                     {"label": "Zaporizhzhya", "value": "7"},
                     {"label": "Ivano-Frankivsk", "value": "8"},
                     {"label": "Kiev", "value": "9"},
                     {"label": "Kirovohrad", "value": "10"},
                     {"label": "Luhansk", "value": "11"},
                     {"label": "Lviv", "value": "12"},
                     {"label": "Mykolayiv", "value": "13"},
                     {"label": "Odessa", "value": "14"},
                     {"label": "Poltava", "value": "15"},
                     {"label": "Rivne", "value": "16"},
                     {"label": "Sumy", "value": "17"},
                     {"label": "Ternopil", "value": "18"},
                     {"label": "Kharkiv", "value": "19"},
                     {"label": "Kherson", "value": "20"},
                     {"label": "Khmelnytskyy", "value": "21"},
                     {"label": "Cherkasy", "value": "22"},
                     {"label": "Chernihiv", "value": "23"},
                     {"label": "Chernivtsi", "value": "24"},
                     {"label": "Crimea", "value": "25"},
                     {"label": "Kiev City", "value": "26"},
                     {"label": "Sevastopol", "value": "27"}]},

        {"type": 'text',
         "label": 'Start Year',
         "value": '1982',
         "key": 'start_year',
         "action_id": "update_data"},

        {"type": 'text',
         "label": 'End Year',
         "value": '2023',
         "key": 'end_year',
         "action_id": "update_data"},

        {"type": 'text',
         "label": 'Start Week',
         "value": '1',
         "key": 'start_week',
         "action_id": "update_data"},

        {"type": 'text',
         "label": 'End Week',
         "value": '52',
         "key": 'end_week',
         "action_id": "update_data"},

        {"type": 'text',
         "label": 'Figure Width',
         "value": '12',
         "key": 'figure_width',
         "action_id": "update_data"},

        {"type": 'text',
         "label": 'Figure Height',
         "value": '8',
         "key": 'figure_height',
         "action_id": "update_data"},

    ]

    controls = [{"type": "hidden",
                 "id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "Plot",
                "on_page_load": True},

               {"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": True}]

    def getData(self, params):

        ticker = params['ticker']
        region_index = params['region_index']
        start_year = int(params['start_year'])
        end_year = int(params['end_year'])
        start_week = int(params['start_week'])
        end_week = int(params['end_week'])

        noaa_index = NOAAIndex.get(int(region_index))
        if noaa_index is None:
            raise ValueError(f"Region {region_index} not found in NOAAIndex")
        
        ###download file

        # url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?provinceID={noaa_index}&country=UKR&yearlyTag=Weekly&type=Mean&TagCropland=land&year1=1982&year2=2023"
        # response = requests.get(url)
        # current_datetime = datetime.now()
        # formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M")
        # filename = os.path.join(save_dir, f"file_{formatted_datetime}.csv")

        # with open(filename, 'wb') as file:
        #     content = response.text
        #     replacements = [("</pre></tt>", ""), ("<tt><pre>", ""), ("<br>", ""), (" VHI", "VHI"), (" SMN", "SMN"),
        #                     ("year", "Year"), ("week", "Week"), ("weeklyfor", "weekly for")]

        #     for old, new in replacements:
        #         content = content.replace(old, new)
        #     content = content.replace(',\n', '\n')
        #     file.write(content.encode('utf-8'))

        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']

        df = pd.read_csv("1.csv", skiprows=1, names=headers)

        df['Year'] = df['Year'].apply(pd.to_numeric, errors='coerce')
        df['Week'] = df['Week'].apply(pd.to_numeric, errors='coerce')
        df['VHI'] = pd.to_numeric(df['VHI'], errors='coerce')
        df['VCI'] = pd.to_numeric(df['VCI'], errors='coerce')
        df['TCI'] = pd.to_numeric(df['TCI'], errors='coerce')

        df = df[(df['SMN'] != -1.0)]

        year_range = (df['Year'] >= start_year) & (df['Year'] <= end_year)
        week_range = (df['Week'] >= start_week) & (df['Week'] <= end_week)

        limited_df = df[year_range & week_range]

        columns_to_display = ["Year", "Week", str(ticker)]

        df1 = limited_df[columns_to_display]

        return df1

    def getPlot(self, params):
        df = self.getData(params)
        df_copy = df.copy()
        df_copy = df_copy.reset_index(drop=True)

        for i in range(len(df_copy[['Year', 'Week']].values)):
            df_copy['Week'][i] = str(df_copy['Year'][i]) + "-" + str(df_copy['Week'][i])
            df_copy.drop(['Year'], axis=1)

        
        fig, ax = plt.subplots(figsize=(int(params['figure_width']), int(params['figure_height'])))
        ax.plot(df_copy['Week'], df_copy[params['ticker']], linestyle='-', color='g') #, marker='*', mec = 'r')

        ax.set_xlabel('Year-week')
        ax.set_ylabel(str(params['ticker']))
        ax.set_title(f'{str(params["ticker"])} for province {params["region_index"]} ')

        plt.xticks(rotation=45, ha='right')

        x_ticks = df_copy['Week'][::52]
        plt.xticks(x_ticks)

        return fig

app = StockExample()
app.launch(port=9093)
