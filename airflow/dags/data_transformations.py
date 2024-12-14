from airflow import DAG
import requests 
import pandas as pd 
import numpy as np 
from datetime import timedelta, datetime 
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator 
from airflow.operators.python import PythonOperator 
import json 
import os 
import pickle

from airflow.providers.postgres.operators.postgres import PostgresOperator 
from airflow.hooks.postgres_hook import PostgresHook
import psycopg2
## For Machine Librairies 

import json
from pprint import pprint
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random
import matplotlib.colors as mcolors

# For Statistics 
from scipy.stats import pearsonr
## For Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_error,root_mean_squared_error
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
## For to save the model 
import joblib
from sklearn.ensemble import RandomForestRegressor

from sklearn.neighbors import KNeighborsRegressor



LIST_KEY_VAlUES = ["impacts", "query"]
COL_NAMES= ["acd",
            "cch" ,
            "etf" , 
            "etf_c" , 
            "fru" , 
            "fwe" ,
            "htc" ,
            "htc_c" , 
            "htn" ,
            "htn_c" ,
            "ior" ,  
            "ldu" , 
            "mru" , 
            "ozd" ,
            "pco" , 
            "pma" ,
            "swe" ,
            "tre" ,
            "wtu" ,
            "ecs" , 
            "pef" , 
            "air_transport_ratio", 
            "business" ,
            "country_dyeing" ,
            "country_fabric" ,
            "country_making" , 
            "country_spinning" , 
            "fabric_process" ,
            "making_complexity" , 
            "making_dead_stock" ,
            "making_waste" , 
            "mass" ,
            "number_of_references" ,
            "physical_durability" ,
            "price" , 
            "product" ,
            "surface_mass" , 
            "traceability" ,
            "upcycled" ,
            "yarn_size"]





## Function for to save data in the folder 

def save_data_in_folder(data,folder, filename)->None:
    ## Get the directory of the DAG file 
    current_dag_directory = os.path.dirname(os.path.abspath(__file__))
    # Specify the directory to save data 
    directory_to_save_data = os.path.join(current_dag_directory, folder)
    ## Create directory if not exists 
    if not os.path.isdir(directory_to_save_data): 
        os.makedirs(directory_to_save_data)
    # Join the filename and directory
    csv_path = os.path.join(directory_to_save_data, filename)
    # Save the data     
    data.to_csv(csv_path, index= False)


def read_json_file(**kwargs): 
    filename = kwargs["filename"]
    ## Get the directory of the DAG file 
    current_dag_directory = os.path.dirname(os.path.abspath(__file__))
    # Specify the directory to save data 
    directory_to_save_data = os.path.join(current_dag_directory, "Input_data")
    # Read json files
    file_data = os.path.join(directory_to_save_data, filename)
    with open (file_data, "r") as file: 
        data = json.load(file)
    return data

def transform_json_to_dataframe_function(task_instance): 
    data = task_instance.xcom_pull(task_ids = "load_json_file")
    ## Remove the index 8, that's bad format 
    result = {}
    LIST_KEY_VAlUES = ["impacts", "query"]
    for i in LIST_KEY_VAlUES:
        list_impacts_all = []
        list_values = []
        keys_values = []
        for element in range(0, len(data)): 
            list_impacts_all.append(data[element][i].values())
        ## Convert the values
        for element in range(0, len(list_impacts_all)):
            list_values.append(list(list_impacts_all[element]))
        ## get the keys values
        keys_values = data[element][i].keys()
        keys_values = [i for i in list(keys_values)]
        data_res = pd.DataFrame(list_values, columns= keys_values)
        result[i] = data_res
    # Get the value of the dataframe 
    data_impacts = result["impacts"]
    data_query = result["query"]
    data_result= pd.concat([data_impacts, data_query], axis=1)
    # Drop the column material 
    data_result = data_result.drop("materials", axis = 1)
     ## Get the directory of the DAG file 
    current_dag_directory = os.path.dirname(os.path.abspath(__file__))
    # Specify the directory to save data 
    directory_to_save_data = os.path.join(current_dag_directory, "Output")
    filename = "ecobalyse_data_transformed.csv"
    csv_path = os.path.join(directory_to_save_data, filename)
    # Save the data 
    data_result.to_csv(csv_path, index= False)
    # Save to csv in the specified output directory 
    #print("data saved to the", csv_path)
    return data_result

# Create function for to insert data in database 
## Create function for to insert the data in database 
def insert_data_into_postgres(task_instance): 
    data = task_instance.xcom_pull(task_ids = "transform_json_to_dataframe")
    #data = data.head(10)
    postgres_hook = PostgresHook(postgres_conn_id = "ecobalyse_database_connection")
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    ## Create a sql query for to insert data 
    insert_query = """
            INSERT INTO Ecobalyse_table (
                                "acd",
                                "cch" ,
                                "etf" , 
                                "etf_c" , 
                                "fru" , 
                                "fwe" ,
                                "htc" ,
                                "htc_c" , 
                                "htn" ,
                                "htn_c" ,
                                "ior" ,  
                                "ldu" , 
                                "mru" , 
                                "ozd" ,
                                "pco" , 
                                "pma" ,
                                "swe" ,
                                "tre" ,
                                "wtu" ,
                                "ecs" , 
                                "pef" , 
                                "air_transport_ratio", 
                                "business" ,
                                "country_dyeing" ,
                                "country_fabric" ,
                                "country_making" , 
                                "country_spinning" , 
                                "fabric_process" ,
                                "making_complexity" , 
                                "making_dead_stock" ,
                                "making_waste" , 
                                "mass" ,
                                "number_of_references" ,
                                "physical_durability" ,
                                "price" , 
                                "product" ,
                                "surface_mass" , 
                                "traceability" ,
                                "upcycled" ,
                                "yarn_size")

                VALUES(%s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,           
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,               
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s,
                      %s)


    """
     # Convert each row to a tuple using apply()
    tuples = data.apply(lambda row: tuple(row), axis=1)
    for record in tuples: 
        try:
            cursor.execute(insert_query,record)
        except: 
            pass
         
    connection.commit()
    cursor.close()
    connection.close()

## Create a function for to connect to the database 

def connect_to_database(): 
    connection = psycopg2.connect(
                    host = "172.23.0.3",
                    database = "ecobalyse", 
                    user = "airflow", 
                    password = "airflow", 
                    port = 5432)
    try: 
        cursor = connection.cursor()
        query = """
                 SELECT *
                 FROM Ecobalyse_table;

                """
        # Execute the request 
        cursor.execute(query)
        tuples_list = cursor.fetchall()
        #print(tuples_list)
        ## Fetch all rows from database 
    except (Exception, psycopg2.DatabaseError) as error:   
        print("Error: %s" % error)   
    # To execute for to return the list of tuples 
    cursor.close()

    # We need to transform the list into a pandas dataframe 
    df = pd.DataFrame(tuples_list, columns=COL_NAMES)
    ## Save data in  folder 
    ## return data
    return df


def dasrbord_visualization():
    print("Hello to le mond")

## Function for to convert categorial variable to numeric 
def convert_cat_variable(col): 
    ## Create an instance 
    label_encoder = LabelEncoder()
    transform_col = label_encoder.fit_transform(col)
    ## return the value 
    return transform_col

def prepare_data_for_machine_learning(task_instance): 
    data = task_instance.xcom_pull(task_ids = "read_data_from_postgre_database")
    ## Clearning data 
    # Clearning  the bad  modality of product
    product = data["product"].unique()
    vraie_value = [element for element in product if isinstance(element, str)]
    data= data.loc[data["product"].isin(vraie_value)]
    # Convert all columns 
    data = data.convert_dtypes()  
    ##  Variables selections
    columns_selected = ["pef", "mass", "product", "making_waste", "yarn_size", "physical_durability",
                        "making_dead_stock", "fabric_process", "price", "air_transport_ratio", "country_dyeing", 
                        "country_fabric"]
    data = data[columns_selected]
    ## transform numerical variables, standarization 
    num_col = data.select_dtypes("float64").columns
    # You dont normalize the target columns, pef 
    target = data["pef"]
    data[num_col] = (data[num_col] -data[num_col].mean())/ data[num_col].std()
    ## Transform categorial variable 
    cat_col = data.select_dtypes("string[python]").columns
    ## call function and use apply for transform columns
    data[cat_col]  = data[cat_col].apply(lambda x: convert_cat_variable(x))
    ## replace targget col 
    data["pef"] = target
    print("data is transformed")
    return data


def Linear_Regression_Model(task_instance): 
    data = task_instance.xcom_pull(task_ids = "prepare_data_for_ML")
    target = data["pef"]
    feats =data.drop("pef", axis = 1)
    # Separate data in train and test
    X_train, X_test, y_train, y_test = train_test_split(feats , target, test_size= 0.25, random_state=42)
    ## show the result 
    print("X_train shape", X_train.shape)
    print("-------------------------")
    print("X_test shape", X_test.shape)
    print("-------------------------")
    print("y_train shape", y_train.shape)
    print("-------------------------")
    print("y_test test shape", y_test.shape)

    # Linear Regression Model instance 
    model = LinearRegression()
    # Train model 
    model.fit(X_train, y_train) 
    #predicton with the test data
    y_pred_test = model.predict(X_test)
    # Prediction with the train data
    y_pred_train = model.predict(X_train)
    # ###############

    # The coefficient of the model 
    coeffs = model.coef_
    intercept = model.intercept_
    # calcul of metrics 
    R2_train = model.score(X_train, y_train) 
    R2_test = model.score(X_test, y_test)
    # Les metrics sur les données de decison 
        # train data
    mae_train = mean_absolute_error(y_train, y_pred_train) 
    mse_train = root_mean_squared_error(y_train, y_pred_train) 
    rmse_train = np.sqrt(root_mean_squared_error(y_train, y_pred_train))
            # the test data 
    mae_test = mean_absolute_error(y_test, y_pred_test) 
    mse_test = root_mean_squared_error(y_test, y_pred_test) 

    rmse_test = np.sqrt(root_mean_squared_error(y_test, y_pred_test))

    # return the result 
    metrics = {
              "mae_train" : mae_train, 
              "mse_train" : mse_train, 
              "rmse_train" : rmse_train, 
              "mae_test" : mae_test, 
              "mse_test": mse_test, 
              "rmse_test": rmse_test
            }
    ## create for the result of the model 
    data_metrics = pd.DataFrame(list(metrics.items()), columns=["Metrics", "Values"])
    ## show the data 
    print(data_metrics)
    ## get the coeff of the model
    coeff = list(coeffs)
    coeff.insert(0,intercept)
    features_names = X_train.columns
    feat = features_names.insert(0, "intercept")
    ## Create a dataframe to show a coeff for earch variable 
    data_coef = pd.DataFrame({"Coeffs": coeff}, index = feat)
    print(data_coef)
    # Save data 
    folder = "Output/Linear_regressor"
    save_data_in_folder(data = data_metrics, folder= folder, filename="Metrics_of_models.csv")
    save_data_in_folder(data = data_coef, folder= folder, filename="coefficients_of_models.csv")
    # Save the modele 
    current_dag_directory = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(current_dag_directory, folder, "model.jolib")
    joblib.dump(model, directory)


def knn_regression_model(task_instance): 
    data = task_instance.xcom_pull(task_ids = "prepare_data_for_ML")
    target = data["pef"]
    feats =data.drop("pef", axis = 1)
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(feats , target, test_size= 0.25, random_state=42)

    model = KNeighborsRegressor(n_neighbors=3)
    model.fit(X_train, y_train)
    # Prediction sur le donnees de test et de train
    y_pred_test = model.predict(X_test)
    # Prediction with the train data
    y_pred_train = model.predict(X_train)

    mae_train = mean_absolute_error(y_train, y_pred_train) 
    mse_train = root_mean_squared_error(y_train, y_pred_train) 
    rmse_train = np.sqrt(root_mean_squared_error(y_train, y_pred_train))
            # the test data 
    mae_test = mean_absolute_error(y_test, y_pred_test) 
    mse_test = root_mean_squared_error(y_test, y_pred_test) 
    rmse_test = np.sqrt(root_mean_squared_error(y_test, y_pred_test))

    # return the result 
    metrics = {
              "mae_train" : mae_train, 
              "mse_train" : mse_train, 
              "rmse_train" : rmse_train, 
              "mae_test" : mae_test, 
              "mse_test": mse_test, 
              "rmse_test": rmse_test
            }
    
    ## create for the result of the model 
    data_metrics = pd.DataFrame(list(metrics.items()), columns=["Metrics", "Values"])
    # Save data 
    folder = "Output/Knn_model"
    save_data_in_folder(data = data_metrics, folder= folder, filename="Metrics_of_models.csv")
    ## Save the modele 
    current_dag_directory = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(current_dag_directory, folder, "model.jolib")
    joblib.dump(model, directory)



def random_forest_regressor(task_instance): 
    data = task_instance.xcom_pull(task_ids = "prepare_data_for_ML")
    target = data["pef"]
    feats =data.drop("pef", axis = 1)
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(feats , target, test_size= 0.25, random_state=42)

    model = RandomForestRegressor(n_estimators=10, random_state=0, oob_score=True)
    model.fit(X_train, y_train)
    # Prediction sur le données de test et de train
    #predicton with the test data
    y_pred_test = model.predict(X_test)
    # Prediction with the train data
    y_pred_train = model.predict(X_train)

    mae_train = mean_absolute_error(y_train, y_pred_train) 
    mse_train = root_mean_squared_error(y_train, y_pred_train) 
    rmse_train = np.sqrt(root_mean_squared_error(y_train, y_pred_train))
            # the test data 
    mae_test = mean_absolute_error(y_test, y_pred_test) 
    mse_test = root_mean_squared_error(y_test, y_pred_test) 
    rmse_test = np.sqrt(root_mean_squared_error(y_test, y_pred_test))

    # return the result 
    metrics = {
              "mae_train" : mae_train, 
              "mse_train" : mse_train, 
              "rmse_train" : rmse_train, 
              "mae_test" : mae_test, 
              "mse_test": mse_test, 
              "rmse_test": rmse_test
            }

    
    ## create for the result of the model 
    data_metrics = pd.DataFrame(list(metrics.items()), columns=["Metrics", "Values"])
    # Save data 
    folder = "Output/Random_Forest_Model"
    save_data_in_folder(data = data_metrics, folder= folder, filename="Metrics_of_models.csv")
    # Save the modele 
    current_dag_directory = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(current_dag_directory, folder, "model.jolib")
    joblib.dump(model, directory)



def choose_the_best_model(): 
    ## Read data 
    filename = "Metrics_of_models.csv"
    current_dag_directory = os.path.dirname(os.path.abspath(__file__))

    ## Create the list of directory
    list_of_directory = ["Linear_regressor","Knn_model", "Random_Forest_Model"]
    result ={}
    output_directory = os.path.join(current_dag_directory, "Output")
    for directory in list_of_directory: 
        file= os.path.join(output_directory,directory,filename)
        result[directory] = pd.read_csv(file)
    # create the dictionnary
    rmse_model ={}
    ## Get the rmse_test for earch model 
    for model, data in result.items(): 
        rmse_test = data[data["Metrics"] == "rmse_test"]["Values"]
        rmse_values =[i for i in rmse_test][0]
        rmse_values = round(rmse_values,2)
        rmse_model[model] = rmse_values
    ### find the best Model 
    best_model = min([(value, key) for key, value in rmse_model.items()]) 
    print("-------------------------------------")
    print("Best Model : ", best_model[1])
    print("-------------------------------------")
    print("RMSE obtenues avec les données de test est: ", best_model[0])






def Train_save_Model(): 
    print("Hello tout le mond")


default_args = {
            "owner": "airflow", 
            "depends_on_past" :False, 
            "start_date" : datetime(2024,12,6),
            "email" :["thiernosidybah232@gmail.com"], 
            "email_on_failure" : False, 
            "email_on_retry" : False, 
            "retries": 2, 
            "retry_delay" :timedelta(minutes=1)
}

with DAG( "ecobalyse_dag", 
         default_args = default_args, 
         schedule_interval = "@daily", 
         catchup = False) as dag : 

        load_json_file_task = PythonOperator( task_id = "load_json_file", 
                                        python_callable = read_json_file, 
                                        op_kwargs={'filename': 'simulations.json'})  

        transform_json_to_dataframe_task = PythonOperator(task_id = "transform_json_to_dataframe", 
                                                          python_callable = transform_json_to_dataframe_function)

        
        create_table_task = PostgresOperator(
                task_id = "create_table", 
                postgres_conn_id = "ecobalyse_database_connection", 
                sql = """ 
                        DROP TABLE  IF EXISTS Ecobalyse_table;
                        CREATE TABLE IF NOT EXISTS Ecobalyse_table(
                           
                                acd NUMERIC,
                                cch NUMERIC,
                                etf NUMERIC, 
                                etf_c NUMERIC, 
                                fru NUMERIC, 
                                fwe NUMERIC,
                                htc NUMERIC,
                                htc_c NUMERIC, 
                                htn NUMERIC,
                                htn_c NUMERIC,
                                ior NUMERIC,  
                                ldu NUMERIC, 
                                mru NUMERIC, 
                                ozd NUMERIC,
                                pco NUMERIC, 
                                pma NUMERIC,
                                swe NUMERIC,
                                tre NUMERIC,
                                wtu NUMERIC,
                                ecs NUMERIC, 
                                pef NUMERIC, 
                                air_transport_ratio NUMERIC, 
                                business TEXT,
                                country_dyeing TEXT,
                                country_fabric TEXT,
                                country_making TEXT, 
                                country_spinning TEXT, 
                                fabric_process TEXT,
                                making_complexity TEXT, 
                                making_dead_stock NUMERIC,
                                making_waste NUMERIC, 
                                mass NUMERIC,
                                number_of_references NUMERIC,
                                physical_durability NUMERIC,
                                price NUMERIC, 
                                product TEXT,
                                surface_mass NUMERIC, 
                                traceability BOOLEAN,
                                upcycled BOOLEAN,
                                yarn_size NUMERIC
                           
                           
                           
                           
                           ); 
                    """
        )

        insert_data_in_table_trask = PythonOperator(
                task_id = "Load_Data", 
                python_callable = insert_data_into_postgres
        )
        
        read_data_from_database_task = PythonOperator(
                    task_id = "read_data_from_postgre_database", 
                    python_callable = connect_to_database
        )
        
        dashbord_task = PythonOperator(
                        task_id = "dashboard_application",
                        python_callable = dasrbord_visualization
        )
        prepare_data_for_machine_task = PythonOperator(
                        task_id = "prepare_data_for_ML", 
                        python_callable = prepare_data_for_machine_learning
        )
    
        linear_regressor_task = PythonOperator(
                                task_id = "linear_regression",
                                python_callable = Linear_Regression_Model)
        
        knn_for_machine_task = PythonOperator(
                                task_id = "Knn_model", 
                                python_callable = knn_regression_model
        )

        random_forest_model_task = PythonOperator(
                                 task_id = "Random_forest_model",
                                 python_callable = random_forest_regressor
        )

        best_model_task = PythonOperator(
                                task_id = "best_Model", 
                                python_callable = choose_the_best_model
        )


        
        load_json_file_task >> transform_json_to_dataframe_task >> create_table_task >>insert_data_in_table_trask >>read_data_from_database_task
        read_data_from_database_task >> dashbord_task
        read_data_from_database_task >> prepare_data_for_machine_task 
        prepare_data_for_machine_task >> linear_regressor_task
        prepare_data_for_machine_task >> knn_for_machine_task
        prepare_data_for_machine_task  >> random_forest_model_task 
        linear_regressor_task >> best_model_task
        knn_for_machine_task >> best_model_task
        random_forest_model_task >> best_model_task

