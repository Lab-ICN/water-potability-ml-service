import grpc
import water_potability_pb2_grpc as pb2_grpc
import water_potability_pb2 as pb2

class WaterClient(object) :
    
    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051
        
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port)
        )
        
        self.stub = pb2_grpc.WaterPotabilityServiceStub(self.channel)
    
    def predict(self) :
        this_message = pb2.PredictWaterPotabilityRequest(
            [1,1,1,1,1,1,1,1,1]
            )
        return self.stub.PredictWaterPotability(this_message)
    
if __name__ == '__main__' :
    client = WaterClient()
    res = client.predict()
    print(res)
        