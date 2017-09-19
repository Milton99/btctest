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

url='http://api.btctrade.com/api/ticker?coin=btc'

def main():
    for i in range(1,100):
        r = requests.get(url, headers = headers)
        #i+=1
    #print i #r.content

#code_to_profile()
if __name__=='__main__':

	#import related libraries
	from pycallgraph import PyCallGraph
	from pycallgraph.output import GraphvizOutput
	from pycallgraph import Config, GlobbingFilter

	#config here, check definitions to find more options
	# config = Config(max_depth=1000)
	graphviz = GraphvizOutput(output_type='svg', output_file='filter_max_depth.svg')
	# #graphviz = GraphvizOutput(output_type='png', output_file='filter_max_depth.png')
	# config.trace_filter = GlobbingFilter(exclude=[
	# 	'abc.*',
	# 	'okk'
	# ])

	#do profiling and intercall relationship graphing
    #with PyCallGraph(output=graphviz, config=config):
	with PyCallGraph(output=graphviz):

		# run main program
		main()

