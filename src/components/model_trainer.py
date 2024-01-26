import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utlis import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("traintestdata","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config==ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("splitting training and test input data")
            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,:-1],
                test_array[:,:-1],
                test_array[:,:-1]
            )
            models={
                "Random Forest": RandomForestRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "Linear Regression":LinearRegression(),
                "K-Neighbors Regressor":KNeighborsRegressor(),
                "XG Boost Regressor":XGBRegressor(),
                "Cat Boost Regressor":CatBoostRegressor(verbose=False),
                "Ada boost Regressor":AdaBoostRegressor()
            }

            model_report:dict=evaluate_model(x=x_train,y=y_train,x_test=x_test,y_test=y_test,models=models)

            ##To get best model score from dict
            best_model_score= max(sorted(model_report.values()))

            ##to get best model name from dict

            best_model_score=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
                ]
            
            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on training and test dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(x_test)

            r2_score=r2_score(y_test,predicted)
            return r2_score

        except Exception as e:
            raise CustomException(e,sys)