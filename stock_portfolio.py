#please install fastapi uvicorn yfinance before running this code
from fastapi import FastAPI
import yfinance as yf

app = FastAPI()


portfolio = []


@app.post("/add-stock/")
def add_stock(symbol: str, quantity: int, buy_price: float):
    stock = {"symbol": symbol.upper(), "quantity": quantity, "buy_price": buy_price}
    portfolio.append(stock)
    return {"message": f"Stock {symbol.upper()} added successfully"}


@app.delete("/remove-stock/")
def remove_stock(symbol: str):
    global portfolio
    portfolio = [stock for stock in portfolio if stock["symbol"] != symbol.upper()]
    return {"message": f"Stock {symbol.upper()} removed successfully"}


@app.get("/portfolio/")
def get_portfolio():
    portfolio_data = []
    for stock in portfolio:
        stock_data = yf.Ticker(stock["symbol"]).history(period="1d")
        current_price = stock_data["Close"].iloc[-1] if not stock_data.empty else None
        profit_loss = (current_price - stock["buy_price"]) * stock["quantity"] if current_price else None

        portfolio_data.append({
            "symbol": stock["symbol"],
            "quantity": stock["quantity"],
            "buy_price": stock["buy_price"],
            "current_price": current_price,
            "profit_loss": profit_loss
        })

    return portfolio_data

