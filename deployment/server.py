import grpc
from concurrent import futures
import time
import water_potability_pb2_grpc as pb2_grpc
import water_potability_pb2 as pb2

class WaterPotabilityService(pb2_grpc.WaterPotabilityServiceServicer) :
    def __init__(self, *args, **kwargs) :
        pass
    
    def PredictWaterPotability(self, request, context) :
        error_response = pb2.Error(message="No error", code="0")
        response = {'prediction' : 5.3, 'level' : '2', 'error' : error_response}
        return pb2.PredictWaterPotabilityResponse(**response)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_WaterPotabilityServiceServicer_to_server(WaterPotabilityService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
    
if __name__ == '__main__' :
    serve()