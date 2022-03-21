import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from matplotlib import pyplot as plt
import time

# variable declarations
wikipedia_url = "https://en.wikipedia.org/wiki/Road_safety_in_Europe"
table_classes_or_ids = "wikitable"


# HTTP requests  to get url from the wiki page
def http_request(url):
    response = requests.get(url)
    return response


# scrapping the requests responses for data using beautifulSoup4
def web_scrapper():
    response = http_request(wikipedia_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': table_classes_or_ids})
    return table


# basic data science using pandas
def data_frames():
    wiki_table = web_scrapper()
    df = pd.read_html(str(wiki_table))
    df = pd.DataFrame(df[0])

    # create a column to add to data table
    year = []
    for i in df.Country:
        year.append(2018)
    year_column = pd.Series(year, name='Year')
    df2 = pd.concat([df, year_column], axis=1)

    # Extract column of interest ::
    # Country, Year, Area, Population, GDP per capita, Population density, Vehicle ownership, Total road deaths, Road deaths per Million Inhabitants

    selected_column = ['Country', 'Year', 'Area (thousands of km2)[21]', 'Population in 2018[22]',
                       'GDP per capita in 2018[23]', 'Population density (inhabitants per km2) in 2017[24]',
                       'Vehicle ownership (per thousand inhabitants) in 2016[25]', 'Total Road Deaths in 2018[27]',
                       'Road deaths per Million Inhabitants in 2018[27]']
    df_selected = df2[selected_column]

    # rename columns for ease
    data = df_selected.rename(
        columns={
            "Area (thousands of km2)[21]": "Area",
            "Population in 2018[22]": "Population",
            "GDP per capita in 2018[23]": "GDP per capita",
            "Population density (inhabitants per km2) in 2017[24]": "Population density",
            "Vehicle ownership (per thousand inhabitants) in 2016[25]": "Vehicle ownership",
            "Total Road Deaths in 2018[27]": "Total road deaths",
            "Road deaths per Million Inhabitants in 2018[27]": "Road deaths per Million Inhabitants"
        }
    )

    data.sort_values(by=['Road deaths per Million Inhabitants'], inplace=True)

    return data


def data_directory():
    """" This fucnction  covert and save both csv of the dataset and jpeg of the data visualization charts into data
    and visuals directory respectively """

    data_table = data_frames()
    data_table.plot(kind="bar", x='Country', y='Road deaths per Million Inhabitants', figsize=(20, 10))

    # before running script change the value for outdir to './data' and visual_plots to ./visual_plots;
    # # here you can find your exported .csv file just like that in my data direct0ry
    outdir, visual_plots = ['./data_dir_test', './visual_plots_test']
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    if not os.path.exists(visual_plots):
        os.mkdir(visual_plots)

    fullname = os.path.join(outdir, 'EU_ROAD_SAFETY_data_curated.csv')
    data_table.to_csv(fullname, index=False)
    plt.savefig(f"{os.path.join(visual_plots, 'EU_Road Death Rate.jpg')}")


def main():
    data_directory()


if __name__ == '__main__':
    print(f"{__file__} processing......")
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds Successfully.  Check your directories")