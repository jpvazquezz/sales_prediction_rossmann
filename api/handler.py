import pickle
import pandas as pd
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann 

#loading model
model = pickle.load(open('C:/Users/Dell/Desktop/ciencia_de_dados/0.Comunidade DS/0.Data_Science_em_Producao/Modulo_9_Interpretação_do_Erro/model_rossman.pkl','rb'))

# initialize API
app = Flask(__name__)

@app.route('/rossmann/predict', methods=['POST']) #POST porque envia dados para receber e não pede (o que seria GET)

def rossmann_predict():
    test_json = request.get_json()
    
    if test_json: #if there is data
        
        if isinstance(test_json,dict):  # Unique Example
            test_raw = pd.DataFrame(test_json, index=[0])
        
        else: # multiple examples
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
        
        # Instantiate Rossman Class
        
        pipeline = Rossmann()
        
        # data cleaning
        df1 = pipeline.data_cleaning(test_raw)
        
        # feature engeineering
        df2 = pipeline.feature_engineering(df1)
        
        # data preparation
        df3 = pipeline.data_preparation(df2)
        
        # prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)
    
        return df_response
        
        
    else:
        return Response('{}',status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run()