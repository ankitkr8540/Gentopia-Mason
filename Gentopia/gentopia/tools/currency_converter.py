import requests
from typing import AnyStr, Optional, Type, Any
from pydantic import BaseModel, Field
from gentopia.tools.basetool import BaseTool

class CurrencyConverterArgs(BaseModel):
    amount: float = Field(..., description="the amount of money to convert")
    from_currency: str = Field(..., description="the currency code to convert from, e.g., USD")
    to_currency: str = Field(..., description="the currency code to convert to, e.g., EUR")

class CurrencyConverter(BaseTool):
    name = "currency_converter"
    description = "Convert an amount from one currency to another using real-time exchange rates."
    args_schema: Optional[Type[BaseModel]] = CurrencyConverterArgs

    def _run(self, amount: float, from_currency: AnyStr, to_currency: AnyStr) -> AnyStr:
        api_url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(api_url)
        data = response.json()
        if to_currency in data['rates']:
            converted_amount = amount * data['rates'][to_currency]
            return f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}"
        else:
            return f"Currency {to_currency} is not supported."

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    converter = CurrencyConverter()
    result = converter._run(100, "USD", "EUR")
    print(result)