from xmlrpc.client import Boolean
import arcpy
import requests
import csv
import sys
import pandas

#import plotly
#import plotly.graph_objects as go

#CSV field names - and more field names as need be

CSV_FIELD_LATITUDE = "latitude"
CSV_FIELD_LONGITUDE = "longitude"
CSV_FIELD_EVENT_LOCATION = "where_coordinates"
CSV_FIELD_EVENT_TYPE = "conflict_name"
CSV_FIELD_EVENT_DATE = "year"
CSV_FIELD_EVENT_FATALITIES = "best"



#Shapefile field names 
SHAPEFILE_FIELD_ID = "Id"
SHAPEFILE_FIELD_EVENT_LOCATION = "location"
SHAPEFILE_FIELD_EVENT_TYPE = "violence"
SHAPEFILE_FIELD_EVENT_DATE = "year"




MAIN_CSV_URL = r'C:\\Users\Wisdom Aklamati\Documents\HFT\Semester 2\GIS programming\Arcpy_learning\conflict_data_afg.csv'

ROOT_DIRECTORY = 'C:\\Users\Wisdom Aklamati\Documents\HFT\Semester 2\GIS programming\Arcpy_learning\\'

#Create the PRJ file so the shapefile references correctly

WGS_84_Info = r'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984", 6378137.0,298.257223563]],PRIMEM["Greenwich", 0.0], UNIT["Degree", 0.0174532925199433]]'
f = open(ROOT_DIRECTORY + "WGS_84.prj", "w")
f.write(WGS_84_Info)
f.close()

arcpy.env.overwriteOutput = True  #Tells the created shapefile to overwrite and not throw an error

Output_Shapefile_FeatureClass = arcpy.CreateFeatureclass_management(ROOT_DIRECTORY, "AFG_Conflict_Event.shp","Point")
arcpy.AddField_management(Output_Shapefile_FeatureClass, SHAPEFILE_FIELD_ID, "TEXT", field_length = 255)
arcpy.AddField_management(Output_Shapefile_FeatureClass, SHAPEFILE_FIELD_EVENT_LOCATION, "TEXT", field_length = 255)
arcpy.AddField_management(Output_Shapefile_FeatureClass, SHAPEFILE_FIELD_EVENT_TYPE, "TEXT", field_length = 255)
arcpy.AddField_management(Output_Shapefile_FeatureClass, SHAPEFILE_FIELD_EVENT_DATE, "TEXT", field_length = 255)



#open CSV file using requests
req = requests.get(MAIN_CSV_URL)
csv_content = req.content

#convert the web content into a string
csv_in_fixed = str(csv_content, 'utf-8')

#split the string into lines so that it can be parsed as CSV
lines = csv_in_fixed.splitlines()

#Put the csv into a dictionary
datareader = csv.DictReader(lines)

#set identifier for each record
rowidval = 0

#lists that will go into the plotly chart

event_dates = []
event_fatalities = []
event_location = []

for row in datareader:
    try:

        #try demonstration purposes, only take the first 1000 records then break out of the loop
        if(rowidval == 1000):
           break
        
        shapefile_fields = [SHAPEFILE_FIELD_ID,SHAPEFILE_FIELD_EVENT_LOCATION,SHAPEFILE_FIELD_EVENT_TYPE,SHAPEFILE_FIELD_EVENT_DATE]
        cursor = arcpy.da.InsertCursor(Output_Shapefile_FeatureClass, shapefile_fields)

        rowidval += 1

        xy = (float(row[CSV_FIELD_LONGITUDE]), float(row[CSV_FIELD_LATITUDE]))

        cursor.insertRow((rowidval,row[CSV_FIELD_EVENT_LOCATION], row[CSV_FIELD_EVENT_TYPE], row[CSV_FIELD_EVENT_DATE]))

        #Add dates for the plot if one or more fatalities were found, dates and fatalities will be plotted with plotly

        if(int(row[CSV_FIELD_EVENT_FATALITIES])) >= 1:
            event_dates.append(row[CSV_FIELD_EVENT_DATE])
            event_fatalities.append(int(row[CSV_FIELD_EVENT_FATALITIES]))
            event_location.append(row[CSV_FIELD_EVENT_LOCATION])

    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        rowidval -= 1

        del cursor
#make simple chartr from the CSV data
""" fig = go.Figure(
    data= [go.Bar(x=event_dates, y =event_fatalities)],
    layout=go.Layout(
        title=go.layout.Title(text="AFG Conflict Dates and Fatalities")    
    )
)

fig.write_html(ROOT_DIRECTORY + 'dates_and_fatalities.html', auto_open=True)"""

print("finished")

        


