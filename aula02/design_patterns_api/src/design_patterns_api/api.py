from fastapi import FastAPI
from .payments import PaymentGateway, PaymentService

api = FastAPI()

@api.get("/")
def index():
    return {"message": "Welcome to the Design Patterns API!"}

@api.post("/pay")
def pay(method: str, amount: float):
    # Build the correct payment service based on the method
    payment_service: PaymentService = PaymentGateway.build(method=method)
    # Process the payment
    return payment_service.process(amount)