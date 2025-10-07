import os 
import sys 
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import evaluate_models,save_object

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifact","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split training and test input data")
            xTrain , yTrain , xTest , yTest = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )


            ## creating the dictonary of models 

            models = {
                "Random Forest" : RandomForestRegressor(),
                "Decision Tree" : DecisionTreeRegressor(),
                "Gradient Boosting" : GradientBoostingRegressor(),
                "Linear Regressor" : LinearRegression(),
                "K-Nearest Neighbour" : KNeighborsRegressor(),
                "XGBClassifier" : XGBRegressor(),
                "Catboost Classifier" : CatBoostRegressor(),
                "Adaboost Classifier" : AdaBoostRegressor()
            }

            model_report = dict=evaluate_models(xTrain=xTrain,yTrain = yTrain ,xTest = xTest , yTest = yTest,models = models)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]


            best_model = models[best_model_name]

            if best_model_score < 0.6 :
                raise CustomException("No Best model Found")
            
            logging.info(f"Best found model on both training and testing dataset")
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(xTest)
            r2_square = r2_score(yTest , predicted)

            return r2_square
        

        except Exception as e:
            raise CustomException(e,sys)