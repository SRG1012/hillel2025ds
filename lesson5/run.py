from typing import Any


CONVERSION_RATES = {
    "USD": 0.9,  # 1 USD = 0.9 CHF
    "EUR": 1.1,  # 1 EUR = 1.1 CHF
    "CHF": 1.0   # 1 CHF = 1.0 CHF (reference currency)
}

class Price:
    def __init__(self, value: int, currency: str):
        self.value: int = value
        self.currency: str = currency

        if self.currency not in CONVERSION_RATES:
            raise ValueError(f"Unsupported currency: {self.currency}")

    def __str__(self) -> str:
        return f"Price: {self.value} {self.currency}"

    def convert(self, to: str) -> "Price":

        if to not in CONVERSION_RATES:
            raise ValueError(f"Unsupported target currency: {to}")


        value_in_chf = self.value * CONVERSION_RATES[self.currency]
        target_value = value_in_chf / CONVERSION_RATES[to]
        return Price(value=round(target_value), currency=to)

    def __add__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operations only with Price objects")

        if self.currency != other.currency:
            other_converted = other.convert(to=self.currency)
            return Price(value=self.value + other_converted.value, currency=self.currency)
        else:
            return Price(value=self.value + other.value, currency=self.currency)

    def __sub__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operations only with Price objects")

        if self.currency != other.currency:
            other_converted = other.convert(to=self.currency)
            return Price(value=self.value - other_converted.value, currency=self.currency)
        else:
            return Price(value=self.value - other.value, currency=self.currency)


PRODUCT_CATALOG = {
    "phone": Price(value=200, currency="USD"),
    "tablet": Price(value=400, currency="USD"),
    "laptop": Price(value=500, currency="EUR"),
    "headphones": Price(value=50, currency="USD"),
    "mouse": Price(value=30, currency="EUR")
}

if __name__ == "__main__":
    print("Available products:")
    for product, price in PRODUCT_CATALOG.items():
        print(f"{product}: {price}")

    cart = []

    while True:
        user_input = input("Enter a product to add to the cart (or 'done' to finish): ").strip().lower()
        if user_input == "done":
            break
        if user_input in PRODUCT_CATALOG:
            cart.append(PRODUCT_CATALOG[user_input])
            print(f"Added {user_input} to the cart.")
        else:
            print("Product not found. Please try again.")

    if cart:
        total_price = cart[0]
        for item in cart[1:]:
            total_price += item

        print(f"Total price: {total_price}")
    else:
        print("Your cart is empty.")
