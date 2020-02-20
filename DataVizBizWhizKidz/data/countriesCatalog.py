"""
Cleaning and consolidation data script
"""

import re
import csv
import sys

# Historial Athletes data sets
historical_athletes_data     = "source-athlete_events-tab.txt"

# Country code data sets
country_codes_iso_data            = "source-country_codes_iso-tab.txt"
historical_country_codes_iso_data = "source-country_codes_iso-historical-tab.txt"

# Population datasets
population_by_country_data         = "source-population_by_country.txt"

# Place holders
country_names_collection = {}
athletes_historical_data_compiled = {}



def get_historical_country_population(year):

    print ("Getting population for year: %s" % year)
    dataIn = open(population_by_country_data)

    for countryRecord in dataIn:

        country_code = re.sub("[^a-z0-9]+", "", countryRecord.split('\t')[1], flags=re.IGNORECASE)

        print ("%s : (%s, %s)  " % (country_code, countryRecord.split('\t')[0],  countryRecord.split('\t')[21]))



def get_historical_and_current_country_codes():
    """
    Produces a list of current and historical 3 character country codes
    and corresponding names
    """
    myFile = open('cleaned-historical_and_current_country_codes.csv', 'wb')
    columns = ['country_code', 'country_name']
    writer = csv.DictWriter(myFile, fieldnames=columns)
    writer.writeheader()

    for country_code, country_name in country_names_collection.items():
        print (" %s, %s " % (country_code, country_name))

        writer.writerow({'country_code': country_code,
                         'country_name': country_name })

def get_historical_athletes_data():
    """
    Produces historical lust of athlete events in alympics since 1960
    """

    firstLine = False
    index = 0

    myFile = open('cleaned-historical_athletes_dataset.csv', 'wb')

    with myFile:
        myFields = ['name', 'sex', 'age', 'height', 'weight', 'team', 'country_code', 'country_name', 'games', 'year', 'season', 'city', 'sport', 'event', 'medal']
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writeheader()
        for record in open(historical_athletes_data).readlines():
            #if index > 100:
            #    break
            index += 1
            (id, name, sex, age, height, weight, team, noc, games, year, season, city, sport, event, medal ) =  record.split('\t')
            if not firstLine:
                firstLine = True
                continue

            country_code = re.sub("[^a-z0-9]+","", noc, flags=re.IGNORECASE)

            try:
                writer.writerow({'name': name ,
                                 'sex': sex,
                                 'age': age,
                                 'height': height,
                                 'weight': weight,
                                 'team': team,
                                 'country_code': country_code,
                                 'country_name': country_names_collection[country_code],
                                 'games': games,
                                 'year': year,
                                 'season': season,
                                 'city': city,
                                 'sport': sport,
                                 'event': event,
                                 'medal': medal })
            except:
                e = sys.exc_info()[0]
                print ("Error: %s" % e)
                print("===========================================")

                #" Missing country code: %s" % record.split('\t')[7])
                pass

def country_codes_iso():

    print ("*** Country codes ***")

    index = 0

    for country in open(country_codes_iso_data):

        country_code = re.sub("[^a-z0-9]+", "", country.split('\t')[1], flags=re.IGNORECASE)

        country_name = country.split('\t')[0].strip()
        country_names_collection[country_code] = country_name

        #if  country.split('\t')[1].strip() in country_names_collection.keys():
        #    print ("Country already in list: %s -> %s" % ( country_code, country_names_collection[country_code] ))

        index += 1

    print (" Total Count: %d" % index)


def historical_country_codes_iso():

    print("*** Historical Country Codes ***")

    for country in open(historical_country_codes_iso_data):

        try:
            country_code = re.sub("[^a-z0-9]+", "", country.split('\t')[1], flags=re.IGNORECASE)
            #country_code = country.strip().split('\t')[1].strip()
            country_name = country.strip().split('\t')[0].strip()
            country_names_collection[country_code] = country_name

            #if country.split('\t')[1].strip() in country_names_collection.keys():
            #    print("Country already in list: %s -> %s" % (country_code, country_names_collection[country_code]))

        except:
            pass


def generateHistoricalCountriesList():
    country_codes_iso()
    historical_country_codes_iso()


def main():

    print ("*** Olympics Historical Data ***")

    generateHistoricalCountriesList()
    get_historical_athletes_data()
    get_historical_and_current_country_codes()
    # get_historical_country_population(2019)





if __name__ == "__main__":

    main()