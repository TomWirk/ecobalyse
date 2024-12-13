import requests
import json
import random
from collections import Counter

API_URL = "https://ecobalyse.beta.gouv.fr/api"
TOKEN = "b1635d73-6459-4e8f-a648-e6ceb41b0977"
HEADERS = {
    "token": TOKEN
}

def fetch_data_param(endpoint):
    response = requests.get(f"{API_URL}/{endpoint}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def fetch_data():
    response = requests.get(f"{API_URL}")
    response.raise_for_status()
    return response.json()


def main():
    # Extraction des données de base
    parameters = fetch_data()["components"]["schemas"]["TextileQuery"]["properties"]
    #parameters = fetch_data()["components"]["parameters"]
    countries = fetch_data_param("textile/countries")
    materials = fetch_data_param("textile/materials")
    products = fetch_data_param("textile/products")
        
    parameters["materials"]["enum"] = [material['id'] for material in materials]
    
    parameters["product"]["enum"] = [product['id'] for product in products]

    parameters["countryFabric"]["enum"] = [country['code'] for country in countries]
    parameters["countryDyeing"]["enum"] = [country['code'] for country in countries]
    parameters["countrySpinning"]["enum"] = [country['code'] for country in countries]
    parameters["countryMaking"]["enum"] = [country['code'] for country in countries]

    parameters["yarnSize"]["minimum"] = 9
    parameters["yarnSize"]["maximum"] = 200

    productsMass = {"chemise":0.250,
            "jean":0.450,
            "jupe":0.300,
            "manteau":0.950,
            "pantalon":0.450,
            "pull":0.550,
            "tshirt":0.150,
            "chaussettes":0.040,
            "calecon":0.040,
            "slip":0.030,
            "maillot-de-bain":0.100}
    
    data=[]

    for _ in range(2000):

        schemas = {}
        # Loop through each component to extract the "schema" key if it exists
        for key, value in parameters.items():
            #if "type" in value:
            #    schemas[key] = 1 # Save only the "schema" part
            if value['type'] == 'number' and key != 'mass':
                if key == 'surfaceMass' or key == 'numberOfReferences':
                    schemas[key] = int(random.uniform(value['minimum'], value['maximum']))
                else:
                    schemas[key] = round(random.uniform(value['minimum'], value['maximum']), 2)
            if value['type'] == 'string':
                schemas[key] = random.choice(value['enum'])
            if value['type'] == 'boolean':
                schemas[key] = random.choice([True, False])
            materials_reducted=[]
            if key == 'materials':
                for x in value['enum']:
                    if random.choice([True, False]):
                        materials_reducted.append(x)
                materials_props = [random.choice(materials_reducted) for _ in range(100)]
                schemas[key] = [{"id": key, "share": value/100} for key, value in Counter(materials_props).items()]
            # if key == 'disabledSteps':
            #     disabledSteps=[]
            #     for i in value['enum']:
            #         if random.choice([True, False]):
            #             disabledSteps.append(i)
            #     schemas[key] = disabledSteps
            if key == 'upcycled':
                schemas[key] = False

        schemas["mass"] = productsMass[schemas["product"]]
        data.append(schemas)

    # Sauvegarde des données
    #with open("parameters.json", "w") as json_file:
    #    json.dump(parameters, json_file, indent=4)

    combined_data = {
        "countries": countries,
        "materials": materials,
        "products": products
    }

    with open("parameters.json", "w") as json_file:
        json.dump(combined_data, json_file, indent=4)


    with open("schemas.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("Données combinées enregistrées dans ecobalyse_data.json")

if __name__ == "__main__":
    main()
