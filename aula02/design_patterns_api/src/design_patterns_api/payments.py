from typing import Protocol

class PaymentService(Protocol):
    def process(self, amount: float):
        raise NotImplementedError

class CreditCardPayment(PaymentService):
    def process(self, amount: float):
        # Logic for processing credit card payment
        return {"message": f"Processed {amount} using credit card"}
    
class PayPalPayment(PaymentService):
    def process(self, amount: float):
        # Logic for processing PayPal payment
        return {"message": f"Processed {amount} using PayPal"}
    
class BitcoinPayment(PaymentService):
    def process(self, amount: float):
        # Logic for processing Bitcoin payment
        return {"message": f"Processed {amount} using Bitcoin"}
    
    
class PaymentGateway:
    registry = {
        "credit_card": CreditCardPayment,
        "paypal": PayPalPayment,
        "bitcoin": BitcoinPayment,
    }

    @classmethod
    def build(cls, method: str) -> PaymentService:
        # Return the corresponding payment service class instance
        payment_class = cls.registry.get(method)
        if not payment_class:
            raise ValueError(f"Unknown payment method: {method}")
        return payment_class()
