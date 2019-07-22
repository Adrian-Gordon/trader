from trader import Trader

trader = Trader()

print(trader.get_ticks(1.15))
print(trader.get_ticks(4.3))


price = trader.increment_price(1.15, 158)

print("new price: ", price)