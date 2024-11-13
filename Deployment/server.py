import grpc
from concurrent import futures
import time
import threading
import water_potability_pb2_grpc as pb2_grpc
import water_potability_pb2 as pb2
from mlflow import MlflowClient
from dotenv import load_dotenv
import os
import mlflow.pyfunc
import pandas as pd
import numpy as np
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_ADMIN_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_ADMIN_PASSWORD")
os.environ["MLFLOW_TRACKING_URI"] = os.getenv("MLFLOW_URL")
os.environ["MLFLOW_S3_IGNORE_TLS"] = "true"

model_name = "ml_water_potability"
client = MlflowClient()
model = None
current_version = None


def load_latest_model():
    """Loads the latest model version if it's not already loaded."""
    global model, current_version
    try:

        latest_version_info = client.search_model_versions(f"name='{model_name}'")
        
        if latest_version_info:
            latest_version = max(int(version.version) for version in latest_version_info)
            
            if current_version != latest_version:

                model = mlflow.pyfunc.load_model(
                    model_uri=f"models:/{model_name}/{latest_version}"
                )
                current_version = latest_version
                print(f"Loaded model version {latest_version}")
    except Exception as e:
        print(f"Failed to load model: {e}")


load_latest_model()

class WaterPotabilityService(pb2_grpc.WaterPotabilityServiceServicer):
    def PredictWaterPotability(self, request, context):
        error_response = pb2.Error(message="No error", code="0")
        
        data_dict = {
            "ph": request.ph if request.ph else np.nan,
            "Hardness": request.hardness if hasattr(request, "hardness") else np.nan,
            "Solids": request.totalDissolveSolids if request.totalDissolveSolids else np.nan,
            "Chloramines": request.chloramines if hasattr(request, "chloramines") else np.nan,
            "Sulfate": request.sulfate if hasattr(request, "sulfate") else np.nan,
            "Conductivity": request.conductivity if hasattr(request, "conductivity") else np.nan,
            "Organic_carbon": request.organicCarbon if hasattr(request, "organicCarbon") else np.nan,
            "Trihalomethanes": request.trihalomethanes if hasattr(request, "trihalomethanes") else np.nan,
            "Turbidity": request.turbidity if request.turbidity else np.nan
        }
        
        data = pd.DataFrame([data_dict])
        
        if model is None:
            error_response.message = "Model not loaded"
            error_response.code = "1"
            return pb2.PredictWaterPotabilityResponse(prediction=-1, error=error_response)
        
        try:
            prediction = model.predict(data)[0]
            response = {"prediction": prediction, "error": error_response}
            return pb2.PredictWaterPotabilityResponse(**response)
        except Exception as e:
            print(f"Prediction error: {e}")
            error_response.message = str(e)
            error_response.code = "1"
            return pb2.PredictWaterPotabilityResponse(prediction=-1, error=error_response)



def poll_for_new_model():
    while True:
        try:
            load_latest_model()
        except Exception as e:
            print(f"Error reloading model: {e}")
        time.sleep(10)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pb2_grpc.add_WaterPotabilityServiceServicer_to_server(
        WaterPotabilityService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started on port 50051.")
    server.wait_for_termination()


if __name__ == "__main__":
    threading.Thread(target=poll_for_new_model, daemon=True).start()
    serve()
