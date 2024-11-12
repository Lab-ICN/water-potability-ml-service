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
import numpy as np

load_dotenv()
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_ADMIN_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_ADMIN_PASSWORD")
os.environ["MLFLOW_TRACKING_URI"] = os.getenv("MLFLOW_URL")
os.environ["MLFLOW_S3_IGNORE_TLS"] = "true"

model_name = "ml_water_potability"
client = MlflowClient()

# Global model variable
model = None
current_version = None


def load_latest_model():
    global model, current_version
    # Fetch the latest version of the model
    latest_version_info = client.get_latest_versions(name=model_name, stages=["None"])
    if latest_version_info:
        latest_version = latest_version_info[0].version
        if current_version != latest_version:
            # Update the model if there's a newer version
            model = mlflow.pyfunc.load_model(
                model_uri=f"models:/{model_name}/{latest_version}"
            )
            current_version = latest_version
            print(f"Loaded model version {latest_version}")


load_latest_model()


class WaterPotabilityService(pb2_grpc.WaterPotabilityServiceServicer):
    #  def PredictWaterPotability(self, request, context) :
    #     error_response = pb2.Error(message="No error", code="0")
    #     # response = {'prediction' : 5.3, 'level' : '2', 'error' : error_response}

    #     return pb2.PredictWaterPotabilityResponse(**response)
    def PredictWaterPotability(self, request, context):
        error_response = pb2.Error(message="No error", code="0")
        print(request)
        print(request.ph)
        bahan = np.array([[request.ph, request.totalDissolveSolids]])
        prediction = model.predict(bahan)[0]
        response = {"prediction": prediction, "error": error_response}
        return pb2.PredictWaterPotabilityResponse(**response)


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
