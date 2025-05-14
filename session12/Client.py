import grpc
import cube_pb2
import cube_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = cube_pb2_grpc.CubeServiceStub(channel)
        number = float(input("Enter a number to find its cube: "))
        response = stub.GetCube(cube_pb2.CubeRequest(number=number))
        print(f"The cube of {number} is {response.result}")


if __name__ == "__main__":
    run()
