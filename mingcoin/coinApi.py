# -*- coding: utf-8 -*-

import hashlib
import hmac
import random
import requests
import collections
import json
import time
import logging
from shared_conf import *
from CustomErrors import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)20s - %(name)20s - %(levelname)20s - %(message)20s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class MarketCondition(object):

	"""
	Class used to get market information. By now 3 markets have been supported, namely btctrade.com, jubi.com, and btc-e.com
	usage example:
	m = MarketCondition(market = "btctrade", coin = "ltc", logging = True)
	print m.get_depth()
	"""

	def __init__(self, market = "btctrade", coin = "ltc", coin2 = None, logging = False):
		if logging:
			logger.info('initilize. market: %s, coin type: %s', market, coin)
		if market not in support_market:
			raise Exception("Unknown market. Report to xfanzone@gmail.com to add support.")
		self._market = market
		if self._market == "btctrade":
			self._base_url = "http://api.btctrade.com/api"
		if self._market == "jubi":
			self._base_url = "http://www.jubi.com/api/v1"
		if self._market == "btc-e":
			self._base_url = "https://btc-e.com/api/3"
		self._coin = coin
		if market != "btc-e" and coin2 is not None:
			if logging:
				logger.warning("does not support set pair")
			coins = None
		self._coin2 = coin2
		self._adjust_pair()
		self._logging = logging

	@property 
	def coin(self):
		return self._coin

	@coin.setter
	def coin(self, value):
		if self._logging:
			logger.info('coin type set to %s', value)
		self._coin = value
		self._adjust_pair()

	@property 
	def coin2(self):
		return self._coin2

	@coin2.setter
	def coin2(self, value):
		if self._logging:
			logger.info('coin2 type set to %s', value)
		self._coin2 = value
		self._adjust_pair()


	def get_ticker(self):
		"""
		get ticker for particular market 
		"""
		#url construction
		url = self._get_request_url('ticker')
		#make the request
		if self._logging:
			logger.info('request for %s', url)
		r = requests.get(url, headers = headers)
		#check http status
		if r.status_code != 200:
			raise ServerError(r.status_code)	
		#parse and check content
		resp = r.json()
		self._check_resp(resp)

		#market specific operation
		#jubi does not come with server time.
		if self._market == "jubi":
			resp['time'] = time.time()

		return resp


	def get_depth(self):
		"""
		get depth for particular market
		"""
		url = self._get_request_url('depth')
		if self._logging:
			logger.info('request for %s', url)
		r = requests.get(url, headers = headers)
		if r.status_code != 200:
			raise ServerError(r.status_code)	
		resp = r.json()
		self._check_resp(resp)

		#market specific operation
		#btctrade comes with an additional 'result' key 
		if 'result' in resp:
			del resp['result']
		if self._market in ('jubi', 'btctrade'):
			asks = resp["asks"]
			resp["asks"] = [[float(x[0]), float(x[1])] for x in asks]
			bids = resp["bids"]
			resp["bids"] = [[float(x[0]), float(x[1])] for x in bids]
		return resp


	def get_trades(self):
		"""
		get trades over past time for particular market
		"""
		url = self._get_request_url('trades')
		if self._logging:
			logger.info('request for %s', url)
		r = requests.get(url, headers = headers)
		if r.status_code != 200:
			raise ServerError(r.status_code)	
		resp = r.json()
		if 'result' in resp and resp['result'] == False:
			if 'message' in resp:
				raise Exception(resp['message'])
			else:
				raise Exception("unkonwn return content")
		return resp

	def _check_resp(self, resp):
		if 'result' in resp and resp['result'] == False:
			if 'message' in resp:
				raise Exception(resp['message'], self._market)
			elif 'code' in resp:
				raise Exception(resp['code'], self._market)
			else:
				raise Exception("unkonwn return content")

	def _get_request_url(self, request_type):
		if self._market == "btctrade":
			url = "{0}/{1}?coin={2}".format(self._base_url, btctrade_api[request_type], self._coin)
		elif self._market == "jubi":
			url = "{0}/{1}/?coin={2}".format(self._base_url, jubi_api[request_type], self._coin)
		elif self._market == "btc-e":
			if self._coin is None or self._coin2 is None:
				raise Exception("illegal pair")
			url = "{0}/{1}/{2}_{3}".format(self._base_url, btce_api[request_type], self._coin, self._coin2)
		return url

	def _adjust_pair(self):
		if self._market != "btc-e":
			return 
		if self._coin is None or self._coin2 is None:
			return
		pair = "{0}_{1}".format(self._coin, self._coin2)
		if pair not in btce_pairs:
			pair = "{0}_{1}".format(self._coin2, self._coin)
			if pair in btce_pairs:
				(self._coin, self._coin2) = (self._coin2, self._coin)
			else:
				raise Exception("illegal pair")


class DealerConst():
	NONCE = "nonce"
	KEY = "key"
	SIGNATURE = "signature"
	COIN = "coin"
	AMOUNT_ORIGINAL = "amount_original"
	AMOUNT_OUTSTANDING = "amount_outstanding"
	PRICE = "price"
	TYPE = "type"
	ID = "id"
	DAYTIME = "daytime"
	STATUS = "status"
	VERSION = "version"
	AMOUNT = "amount"
	SINCE = "since"
	ACCESS_KEY = 'hpcmm-puu7v-nxqe5-r5nz2-emn9t-edk1k-th955' #公钥
	SECRET_KEY = '%/$W2-/u(J]-6q*Xp-$c^Qz-W4;q5-w8LQj-VH6Tj' #私钥
	ACCOUNT_ID = '970406'

class Dealer(object):
	"""
	Class used to do transactions on particular markets. By now 2 markets have been supported, namely btctrade.com and jubi.com
	usage example:
	d = Dealer(market = "btctrade", coin = "ltc", public_key = "{your publib key}", secret_key = "{you secret key}", logging = True)
	d.get_balance()
	d.buy(price = 1.0, amount = 1.0)
	"""

	def __init__(self, market = "btctrade", coin = "btc",  logging = False):
		if logging:
			logger.info('initilize. market: %s, coin type: %s', market, coin)
		if market not in ("btctrade", "jubi"):
			raise Exception("Unknown market. Report to xfanzone@gmail.com to add support.")
		self._market = market
		if self._market == "btctrade":
			self._base_url = "http://api.btctrade.com/api"
		if self._market == "jubi":
			self._base_url = "http://www.jubi.com/api/v1"
		self._coin = coin
		self._public_key = DealerConst.ACCESS_KEY
		self._secret_key = DealerConst.SECRET_KEY
		if self._secret_key is not None:
			self._hash_key = hashlib.md5(self._secret_key).hexdigest()
		else:
			self._hash_key = None
		self._logging = logging

	def get_balance(self):
		"""
		get current balance
		"""
		self._url = self._get_request_url('balance')
		self._get_basic_payload()
		self._post_signatured_payload()
		resp = self.resp.json() 
		if self._speed_issue(resp):
			time.sleep(2)
			return self.get_balance()
		for k, v in resp.iteritems():
			if '_lock' in k:
				resp[k.replace('_lock', '_reserved')] = resp[k]
				del resp[k]
		return resp

	def get_orders(self, order_type = "open", since = None, coin = 'btc'):
		"""
		get orders issued by yourself
		"""
		self._url = self._get_request_url('orders')
		self._get_basic_payload()
		self._set_coin(coin)
		if self._market == "btctrade" and since is not None:
			if self._logging:
				logger.warning("btctrade does not support `since' keyword, omitting")
			since = None
		if since is not None:
			self._set_get_order_since(since)
		self._set_get_orders_type(order_type)
		self._post_signatured_payload()
		resp = self.resp.json()
		if self._speed_issue(resp):
			time.sleep(2)
			return self.get_orders()
		return resp

	def fetch_order(self, orderId):
		"""
		fetch order information by order id
		"""
		self._url = self._get_request_url('fetch_order')
		self._get_basic_payload()
		self._set_orderId(orderId)
		self._post_signatured_payload()
		resp = self.resp.json()
		if self._speed_issue(resp):
			time.sleep(2)
			return self.fetch_order(orderId)
		return resp

	def cancel_order(self, orderId):
		"""
		cancel order by order id
		"""
		self._url = self._get_request_url('cancel_order')
		self._get_basic_payload()
		self._set_orderId(orderId)
		self._post_signatured_payload()
		resp = self.resp.json()
		if self._logging:
			logger.debug("cancel order: %s", resp.__str__())
		if self._speed_issue(resp):
			time.sleep(2)
			return self.cancel_order(orderId)
		return resp

	def buy(self, price, amount):
		"""
		buy `amount' coin at `price'
		"""
		self._url = self._get_request_url('buy')
		self._get_basic_payload()
		self._set_coin()
		self._set_amount(amount)
		self._set_price(price)
		if self._market == "jubi":
			self._set_trade_type("buy")
		self._post_signatured_payload()
		resp = self.resp.json()
		if self._speed_issue(resp):
			time.sleep(2)
			return self.buy(price, amount)
		return resp

	def sell(self, price, amount):
		"""
		sell `amount' coin at `price'
		"""
		self._url = self._get_request_url('sell')
		self._get_basic_payload()
		self._set_coin()
		self._set_amount(amount)
		self._set_price(price)
		if self._market == "jubi":
			self._set_trade_type("sell")
		self._post_signatured_payload()
		resp = self.resp.json()
		if self._speed_issue(resp):
			time.sleep(2)
			return self.sell(price, amount)
		return resp

	def _generate_signature(self):
		para_dict = self.payload
		str_list = []
		for k, v in para_dict.iteritems():
			str_list.append(str(k) + "=" + str(v))
		str_to_sig = "&".join(str_list)
		sig = hmac.new(self._hash_key, str_to_sig, hashlib.sha256).hexdigest()
		para_dict[DealerConst.SIGNATURE] = sig

	def _generate_nonce(self, length=13):
		"""Generate pseudorandom number."""
		#nonce = ''.join([str(random.randint(0, 9)) for i in range(length)])
		nonce = str(int(round(time.time() * 1000)))
		return nonce

	def _build_http_param(self):
		para_dict = self.payload
		str_list = []
		for k, v in para_dict.iteritems():
			str_list.append(str(k) + "=" + str(v))
		str_to_sig = "&".join(str_list)
		return str_to_sig

	def _get_basic_payload(self):
		if self._public_key is None:
			raise Exception('public key not set')
		self.payload = collections.OrderedDict()
		self.payload[DealerConst.NONCE] = self._generate_nonce()
		if self._market == "btctrade":
			self.payload[DealerConst.VERSION] = 2
		self.payload[DealerConst.KEY] = self._public_key

	def _post_signatured_payload(self):
		self._generate_signature()
		self._post_data()

	def _post_data(self):
		http_param = self._build_http_param()
		if self._logging:
			logger.info("request for %s with data: %s", self._url, http_param)
		self.resp = requests.post(self._url, http_param, headers = headers)

	def _set_orderId(self, orderId):
		self.payload[DealerConst.ID] = orderId

	def _set_coin(self, coin):
		self.payload[DealerConst.COIN] = coin

	def _set_amount(self, amount):
		self.payload[DealerConst.AMOUNT] = amount

	def _set_price(self, price):
		self.payload[DealerConst.PRICE] = price

	def _set_get_orders_type(self, order_type):
		self.payload[DealerConst.TYPE] = order_type

	def _set_get_order_since(self, since):
		self.payload[DealerConst.SINCE] = since

	def _set_trade_type(self, trade_type):
		self.payload[DealerConst.TYPE] = trade_type

	def is_buy_done(self, orderId):
		"""
		return a float between 0 and 1, indicating the percentage that is done of the order 
		"""
		resp = self.fetch_order(orderId)
		amount_original = float(resp[DealerConst.AMOUNT_ORIGINAL])
		amount_outstanding = float(resp[DealerConst.AMOUNT_OUTSTANDING])
		return 1 - amount_outstanding / amount_original

	def is_sell_done(self, orderId):
		"""
		return a float between 0 and 1, indicating the percentage that is done of the order 
		"""
		resp = self.fetch_order(orderId)
		if self._speed_issue(resp):
			return self.is_sell_done(orderId)
		amount_original = float(resp[DealerConst.AMOUNT_ORIGINAL])
		amount_outstanding = float(resp[DealerConst.AMOUNT_OUTSTANDING])
		return 1 - amount_outstanding / amount_original

	def _speed_issue(self, resp):
		if type(resp) == dict and 'message' in resp.keys() and 'result' in resp.keys() and resp['result'] == False and "S_U_001" in resp['message']:
			return True
		return False

	def _get_request_url(self, request_type):
		if self._market == "btctrade":
			url = "{0}/{1}?coin={2}".format(self._base_url, btctrade_api[request_type], self._coin)
		elif self._market == "jubi":
			url = "{0}/{1}/?coin={2}".format(self._base_url, jubi_api[request_type], self._coin)
		return url

#-------------------------------------------------------------------------------------------
def main():
	# 查询当前行情
	m_btc = MarketCondition(market = "btctrade", coin = "btc", logging = False).get_ticker()
	m_eth = MarketCondition(market = "btctrade", coin = "eth", logging = False).get_ticker()
	m_ltc = MarketCondition(market = "btctrade", coin = "ltc", logging = False).get_ticker()
	m_doge = MarketCondition(market = "btctrade", coin = "doge", logging = False).get_ticker()
	m_ybc = MarketCondition(market = "btctrade", coin = "ybc", logging = False).get_ticker()

	# 查询账户资产信息
	dealer_balance = Dealer(market = "btctrade", coin = "btc",  logging = False).get_balance()
	dealer_balance = {key: float(value) for (key,value) in dealer_balance.items()} 

	#折算人民币价值
	cny_balance={}
	cny_balance['cny'] = (dealer_balance['cny_balance'] + dealer_balance['cny_reserved']) 
	cny_balance['btc'] = (dealer_balance['btc_balance'] + dealer_balance['btc_reserved']) * m_btc['last']
	cny_balance['eth'] = (dealer_balance['eth_balance'] + dealer_balance['eth_reserved']) * m_eth['last']
	cny_balance['ltc'] = (dealer_balance['ltc_balance'] + dealer_balance['ltc_reserved']) * m_ltc['last']
	cny_balance['doge'] = (dealer_balance['doge_balance'] + dealer_balance['doge_reserved']) * m_doge['last']
	cny_balance['ybc'] = (dealer_balance['ybc_balance'] + dealer_balance['ybc_reserved']) * m_ybc['last']
	value_total = sum(cny_balance.values())

	for k,v in cny_balance.items():
		print "the rmb value of " + k + " is： %f" %v

	print "财产折合人民币：%.2f" %value_total
	print "财产折合比特币: %f" %(value_total/m_btc['last'])
	rate=6.87
	print "比特币现行价: %.2f" %m_btc['last'] + " 元 or " + ("%.2f" %(m_btc['last']/rate)) + " 美金"
	


	# 查询特定挂单信息，需要提供挂单ID
	# d = Dealer(market = "btctrade", coin = "btc",  logging = True)
	# print d.fetch_order()

	# 查询挂单信息
	# d = Dealer(market = "btctrade", coin = "btc",  logging = True)
	# print d.get_orders('all')


#code_to_profile()
if __name__=='__main__':

	#import related libraries
	from pycallgraph import PyCallGraph
	from pycallgraph.output import GraphvizOutput
	from pycallgraph import Config, GlobbingFilter

	#config here, check definitions to find more options
	config = Config(max_depth=10)
	graphviz = GraphvizOutput(output_type='svg', output_file='filter_max_depth.svg')
	#graphviz = GraphvizOutput(output_type='png', output_file='filter_max_depth.png')
	config.trace_filter = GlobbingFilter(exclude=[
		'abc.*',
		'okk'
	])

	#do profiling and intercall relationship graphing
	with PyCallGraph(output=graphviz, config=config):

		# run main program
		main()



