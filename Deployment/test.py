import grpc
import unittest
import water_potability_pb2_grpc as pb2_grpc
import water_potability_pb2 as pb2
from unittest.mock import MagicMock

import os
from dotenv import load_dotenv

load_dotenv()
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_ADMIN_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_ADMIN_PASSWORD")
os.environ["MLFLOW_TRACKING_URI"] = os.getenv("MLFLOW_URL")
os.environ["MLFLOW_S3_IGNORE_TLS"] = "true"


class WaterClient:
    
    def __init__(self, host='10.34.4.242', port=50051):
        self.host = host
        self.port = port
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = pb2_grpc.WaterPotabilityServiceStub(self.channel)
    
    def predict(self, ph, totalDissolveSolids, turbidity):
        request = pb2.PredictWaterPotabilityRequest(
            ph=ph,
            totalDissolveSolids=totalDissolveSolids,
            turbidity=turbidity
        )

        print(f"\n[DEBUG] Sending request: {request}")  # Debugging request

        try:
            response = self.stub.PredictWaterPotability(request)
            print(f"[DEBUG] Received response: {response}")  # Debugging response
            return response
        except grpc.RpcError as e:
            print(f"[ERROR] gRPC error: {str(e)}")  # Fix: Use str(e) instead of e.details()
            raise


class TestWaterClient(unittest.TestCase):

    def setUp(self):
        self.client = WaterClient()
        self.client.stub = MagicMock()  # Mock the gRPC stub

    def test_valid_prediction(self):
        """Test valid prediction response"""
        expected_response = pb2.PredictWaterPotabilityResponse(
            prediction=1.0  # Corrected field name
        )

        # Mock the stub's response
        self.client.stub.PredictWaterPotability.return_value = expected_response

        print("\n[TEST] Running test_valid_prediction...")  # Debug info
        response = self.client.predict(ph=7.0, totalDissolveSolids=20000, turbidity=4.0)
        print(f"[DEBUG] Response in test: {response}")

        self.assertEqual(response.prediction, 1.0, "Expected prediction to be 1.0")

    def test_invalid_input(self):
        """Test invalid values where server should raise an error"""
        invalid_cases = [
            (-1, 20000, 4.0),  # Invalid pH
            (7.0, -500, 4.0),  # Invalid TDS
            (7.0, 20000, -3.0)  # Invalid turbidity
        ]

        for case in invalid_cases:
            ph, tds, turbidity = case
            print(f"\n[TEST] Running test_invalid_input with case: {case}")

            self.client.stub.PredictWaterPotability.side_effect = grpc.RpcError("Invalid input")

            with self.assertRaises(grpc.RpcError, msg=f"Should raise an error for input {case}"):
                self.client.predict(ph, tds, turbidity)

    def test_error_response(self):
        """Test handling of error response from the server"""
        expected_response = pb2.PredictWaterPotabilityResponse(
            prediction=0.0,  # Example prediction
            error=pb2.Error(message="Invalid pH value", code="400")  # Simulated error
        )

        self.client.stub.PredictWaterPotability.return_value = expected_response

        print("\n[TEST] Running test_error_response...")
        response = self.client.predict(ph=-1, totalDissolveSolids=20000, turbidity=4.0)
        print(f"[DEBUG] Response in test_error_response: {response}")

        self.assertEqual(response.error.message, "Invalid pH value", "Error message mismatch")
        self.assertEqual(response.error.code, "400", "Error code mismatch")


if __name__ == '__main__':
    unittest.main(verbosity=2)  # Enable verbose output for better debugging
