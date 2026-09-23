import configparser
import json
import redshift_connector


config = configparser.ConfigParser()
config.read("config.ini")

path_location = config["paths"]["path_location"]

with open(path_location, "r") as f:
    config = json.load(f)

host = config["host"]
port = config.get("port",0)
user = config["user"]
pw = config["pw"]
database = config.get("database", [])

def run_query_single(query):
    conn = redshift_connector.connect(
        host=host,
        port=port,
        user=user,
        password=pw,
        database=database,
        ssl = True
        )
    cursor = conn.cursor()
    cursor.execute(query)
    #For counts/aggeregates 
    result = cursor.fetchone()[0]

    #for data validation across_rows
    result1 = cursor.fetchmany(10)
    cursor.close()
    conn.close()
    return result1