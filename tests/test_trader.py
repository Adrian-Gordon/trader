import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest

import mock

from trader import Trader


def test_get_ticks_less_then_2():
  '''test that the correct number of tcks is returned for prices less than 2.0'''
  trader = Trader()

  ticks = trader.get_ticks(1.64)

  assert ticks == 64

def test_get_ticks_6_point_6():
  trader = Trader()
  ticks = trader.get_ticks(6.6)
  assert ticks == 193

def test_is__trading_opportunity_true():
  trader = Trader()

  assert trader.is_trading_opportunity(6.6, 1.64, 60) == True

def test_is_trading_opportunity_false_not_enough_ticks():
  trader = Trader()

  assert trader.is_trading_opportunity(6.6, 1.64, 200) == False

def test_is_trading_opportunity_false_negative_ticks():
  trader = Trader()

  assert trader.is_trading_opportunity(1.64, 6.6, 10) == False


def test_back_to_lay_take_profit():
  trader = Trader()
  returns = trader.simulate_back_to_lay( 3.0, 10.0, [3.0, 2.9, 2.8, 2.7, 2.6, 2.5], 10, -10)
  assert returns > 0.0

def test_back_to_lay_stop_loss():
  trader = Trader()
  returns,_, _, _, _ = trader.simulate_back_to_lay( 3.0, 10.0, [3.0, 3.1, 3.2, 3.3, 3.4, 3.5], 10, -10)
  assert returns < 0.0

def test_back_to_lay_close_position():
  trader = Trader()
  returns,_, _, _, _ = trader.simulate_back_to_lay( 3.0, 10.0, [3.0, 3.1, 3.0, 3.1, 3.0, 3.1, 3.0], 10, -10)
  assert round(returns, 2) == 0.0



def test_lay_to_back_take_profit():
  trader = Trader()
  returns,_, _, _, _ = trader.simulate_lay_to_back( 3.0, 10.0, [3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.4, 3.4], 10, -10)
  assert returns > 0.0



def test_lay_to_back_close_position():
  trader = Trader()
  returns,_, _, _, _ = trader.simulate_lay_to_back( 3.0, 10.0, [3.0, 3.1, 3.2, 3.3, 3.3, 3.3, 3.3, 3.3, 3.0], 10, -10)
  assert round(returns, 2) == 0



def test_lay_to_back_stop_loss():
  trader = Trader()
  returns,_, _, _, _ = trader.simulate_lay_to_back( 3.0, 10.0, [3.0, 2.9, 2.8, 2.7, 2.6, 2.5], 10, -10)
  assert returns < 0.0


def test_simulate_lay_to_back_trade_take_profit():
  trader = Trader()
  returns,_, _, _, _ = trader.simulate_lay_to_back_trade(2.5, 1.0, 3.5)
  assert round(returns, 2) == 0.19


def test_simulate_lay_to_back_trade_stop_loss():
  trader = Trader()
  returns,_, _, _, _ = trader.simulate_lay_to_back_trade(3.5, 1.0, 2.5)
  assert round(returns, 2) == -0.16

def test_simulate_lay_to_back_trade_close_position():
  trader = Trader()
  returns,_, _, _, _ = trader.simulate_lay_to_back_trade(3.5, 1.0, 3.5)
  assert round(returns, 2) == -0.0

def test_simulate_back_to_lay_trade_take_profit():
  trader = Trader()
  returns,_, _, _, _ = trader.simulate_back_to_lay_trade(3.5, 1.0, 2.5)
  assert round(returns, 2) == 0.4

def test_simulate_back_to_lay_trade_stop_loss():
  trader = Trader()
  returns,_, _, _, _ = trader.simulate_back_to_lay_trade(3.5, 1.0, 4.0)
  assert round(returns, 3) == -0.125

def test_simulate_back_to_lay_trade_close_position():
  trader = Trader()
  returns,_, _, _, _ = trader.simulate_back_to_lay_trade(3.5, 1.0, 3.5)
  assert round(returns, 3) == 0.0