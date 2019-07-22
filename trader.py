class Trader:
  ticks_lookup=[
  [2.0, 100, 100, 0.02],
  [3.0, 50, 150, 0.05],
  [4.0, 20, 170, 0.1],
  [6.0, 20, 190, 0.2],
  [10.0, 20, 210, 0.5],
  [20.0, 20, 230, 1.0],
  [30.0,10, 240, 2.0],
  [50.0, 10, 250, 5.0]
  ]

  def get_ticks(self, price):
    ticks = 0
    index = -1
    for i in range(8):
      if price > Trader.ticks_lookup[i][0]:
        index+= 1
      else:
        ticks = Trader.ticks_lookup[index][2]
        dif = price - Trader.ticks_lookup[index][0]
        dif_in_ticks = dif /(Trader.ticks_lookup[index][3])
        ticks += dif_in_ticks
    if index == -1:
      ticks = (price -1.0) / 0.01

    return round(ticks)

  def increment_price(self, price, ticks):
    price_ticks = self.get_ticks(price)
    target_ticks = price_ticks + ticks
   # print(price_ticks, target_ticks)
    index = -1
    for i in range(8):
      if( Trader.ticks_lookup[i][2] > target_ticks):
        index = (i - 1)
        break
    if index == -1:
      return(price + (ticks * 0.01))
    #print(index)
    remaining_ticks = target_ticks - Trader.ticks_lookup[index][2]
    #print(remaining_ticks)
    price_increment = remaining_ticks * Trader.ticks_lookup[index][3]
    #print(price_increment)
    target_price =  Trader.ticks_lookup[index][0] + price_increment
    return(target_price)



  def is_trading_opportunity(self, back_price, lay_price, ticks):
    back_ticks = self.get_ticks(back_price)
    lay_ticks = self.get_ticks(lay_price)

    if(back_ticks - lay_ticks) > ticks:
      return True
    else:
      return False

  def simulate_back_to_lay(self, odds_to_back, stake_to_back, l_observed, target_ticks, stop_loss_ticks):
      '''
        Simulate the operation of a back to lay trade against a time series of observed lay prices
        parameters:
          odds_to_back -- float, odds at which to place the starting back bet
          stake_to_back -- float, stake at which to place the starting back bet
          l_observed -- array of floats, observed sequence of lay prices
          target_ticks -- integer, target number of ticks difference before trading out for a profit
          stop_loss_ticks -- negative integer, maximum number of ticks of loss to accept before performing a stop loss process
        returns:
          float: return on the trade
      '''
      #self.strike_lay_bet(odds_to_lay, stake_to_lay)

      backed_ticks = self.get_ticks(odds_to_back)
      for t in range(len(l_observed)):
        observed_price = l_observed[t]
        observed_ticks = self.get_ticks(observed_price)

        tick_diff = backed_ticks - observed_ticks 


        if(tick_diff >= target_ticks):
          return self.simulate_back_to_lay_trade(odds_to_back, stake_to_back, observed_price) #take profit
          break
        if(tick_diff <= stop_loss_ticks):
          return self.simulate_back_to_lay_trade(odds_to_back, stake_to_back, observed_price) #stop loss
          break

      return self.simulate_back_to_lay_trade(odds_to_back, stake_to_back, observed_price) #close position


  
  def simulate_lay_to_back(self, odds_to_lay, stake_to_lay, b_observed, target_ticks, stop_loss_ticks):
    '''
      Simulate the operation of a lay to back trade against a times eries of observed back prices
      parameters:
        odds_to_lay -- float, odds at which to place the starting lay bet
        stake_to_lay -- float, stake at which to place the starting lay bet i.e. amount to lose
        b_observed -- array of floats, observed sequence of back prices
        target_ticks -- integer, target number of ticks difference before trading out for a profit
        stop_loss_ticks -- negative integer, maximum number of ticks of loss to accept before performing a stop loss process
      returns:
        float: return on the trade
    '''
    #self.strike_lay_bet(odds_to_lay, stake_to_lay)

    layed_ticks = self.get_ticks(odds_to_lay)
    for t in range(len(b_observed)):
      observed_price = b_observed[t]
      observed_ticks = self.get_ticks(observed_price)

      tick_diff = observed_ticks - layed_ticks


      if(tick_diff >= target_ticks):
        return self.simulate_lay_to_back_trade(odds_to_lay, stake_to_lay, observed_price) #take profit
        break
      if(tick_diff <= stop_loss_ticks):
        return self.simulate_lay_to_back_trade(odds_to_lay, stake_to_lay, observed_price) #stop loss
        break

    return self.simulate_lay_to_back_trade(odds_to_lay, stake_to_lay, observed_price) #close position



  def simulate_lay_to_back_trade(self, lay_odds, lay_stake, back_odds):
    '''simulate the placing of a lay to back trade
      parameters:
        lay_odds -- float, the decimal odds of the lay part of the trade
        lay_stake -- float, the stake on the lay side of the trade (amount layed to lose)
        back_odds -- float, the decimal odds of the back half of the trade
      returns:
        float, the return on the trade
      '''
    back_stake = lay_stake * ((lay_odds /(lay_odds -1.0)) / back_odds)

    return (back_stake * (back_odds -1)) - lay_stake, lay_odds, lay_stake, back_odds, back_stake

  def simulate_back_to_lay_trade(self, back_odds, back_stake, lay_odds):
    '''simulate the placing of a back to lay trade
      parameters:
        back_odds -- float, the decimal odds of the back half of the trade
        back_stake -- float, the stake on the back side of the trade
        lay_odds -- float, the decimal odds of the lay part of the trade
      returns:
        float, the return on the trade
      '''

    lay_stake = back_stake / ((lay_odds /(lay_odds -1.0)) / back_odds)

    return (back_stake * (back_odds -1)) - lay_stake, back_odds, back_stake, lay_odds, lay_stake

