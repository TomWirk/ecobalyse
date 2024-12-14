from fastapi import FastAPI, Body, Depends, HTTPException, status, Security
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import joblib 
import numpy as np 
from typing import Optional
#from typing import Annotated
from fastapi.security import api_key
from sqlalchemy.orm import Session


# Create an API KEY 
api_key_header = api_key.APIKeyHeader(name = "X-API-KEY")
async def validate_api_key(key : str = Security (api_key_header)): 
    if key != settings.API_KEY: 
        raise HTTPException (
                status_code = 401, 
                detail = "Unauthorized - API Key is wrong"
        )
    return None



## Load Linear Regressor 
filename = '/code/app/models/regressor_model.jolib'

model = joblib.load(filename)
print(model.feature_names_in_)


app = FastAPI(openapi_tags = [{
                    "name": "API for Prediction of Impact",
                    "description": "default functions"
}], 
                title = "Ecobalyse Project", 
                description = "My owner API",
                contact = {
                        "name" : "Thierno BAH", 
                        "email" : "thiernosidybah232@gmail.com"
                        })


## Include authentification
#app.include_router(auth.router)

# Create a base Model 
class EcobalyseData(BaseModel):
    airTransportRatio : Optional[float] = 0.94
    business : Optional[float] = 0
    countryDyeing	: Optional[int] = 0
    countryFabric : Optional[int] = 0
    countryMaking : Optional[int] = 1
    countrySpinning	: Optional[int] = 0
    fabricProcess	: Optional[int] = 1
    makingComplexity : Optional[int] = 2
    makingDeadStock	: Optional[float] = 0.22
    makingWaste : Optional[float] = 0.25
    mass	: Optional[float] = 0.55
    physicalDurability	: Optional[float] = 0.92
    price	: Optional[float] = 166.80
    product	: Optional[float] = 0
    surfaceMass	: Optional[float] = 180
    yarnSize	: Optional[float] = 59




@app.get("/")
async def root():
    """
    Check if API is working 
    Return a message if the API is working
    """
    return {"message": "API is working"}




# create a post for predict data 
@app.post("/predict")
async def predict_impact(data: EcobalyseData): 
    new_data = [[ 
                data.airTransportRatio,
                data.business ,
                data.countryDyeing,
                data.countryFabric ,
                data.countryMaking,
                data.countrySpinning,
                data.fabricProcess,
                data.makingComplexity ,
                data.makingDeadStock	,
                data.makingWaste ,
                data.mass,
                data.physicalDurability,
                data.price,
                data.product,
                data.surfaceMass,
                data.yarnSize,
               
     ]]
    # Make Prediction 
    predictions = round(model.predict(new_data)[0],3)
    return {
            "predictions_impacts" : predictions
    }
