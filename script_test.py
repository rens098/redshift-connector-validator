from db import run_query_single
import json
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

path_location = config["paths"]["path_location"]

with open(path_location, "r") as f:
    config = json.load(f)   

#Variables
schema = config["schema"]
table_name = config["table_name"]
count_not_0 = config.get("count_not_0", 0)
duplicate_count = config.get("duplicate_count", 0)
not_null_column = config.get("not_null_fields", [])
check_null_0 = config.get("check_null_0")
column_list = ", ".join(config["field_list"])

#Validator
def test_total_count():
    query = f"""
            SELECT 
            count(1) from {schema}.{table_name};
            """
    result = run_query_single(query)
    print(f"Count: {result}")
    assert result != count_not_0, f" Count:{result}"

def test_duplicate():
    query = f"""
            SELECT
            Count(1) 
            from (SELECT
            {column_list},
            count(1) 
            from {schema}.{table_name}
            group by {column_list}
            HAVING count(1) > 1) a;
            """
    result = run_query_single(query)
    print(f"Duplicate Data: {result}")
    assert result == duplicate_count, f"Duplicate Data:{result}"

def test_check_null_0():
    for col in not_null_column:
        query = f"""
                SELECT
                count(1) from (SELECT
                {col}
                FROM {schema}.{table_name}
                WHERE {col} IS NULL
                )a ;
                """
        result = run_query_single(query)
        print(f"Null Count {col}: {result}")
        assert result == check_null_0, f"Null Count for {col}:{result}"