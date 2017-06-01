#!/usr/bin/env python

import sys
import os
import re
import argparse
import json
from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def index():
    algo = request.args.get('algo', 'lexrank')
    text = request.args.get('text', None)

    summarizer_params = {}
    if 'sent_limit' in request.args:
        summarizer_params['sent_limit'] = int(request.args.get('sent_limit'))
    if 'char_limit' in request.args:
        summarizer_params['char_limit'] = int(request.args.get('char_limit'))
    if 'imp_require' in request.args:
        summarizer_params['imp_require'] = float(request.args.get('imp_require'))

    factory = Factory()
    summarizer = None

    if algo in ('lexrank', 'clexrank', 'divrank'):
        summarizer = factory.get_summarizer('lexrank')
        if algo == 'clexrank':
            summarizer_params['continuous'] = True
        if algo == 'divrank':
            summarizer_params['use_divrank'] = True
    elif algo == 'mcp':
        summarizer = factory.get_summarizer('mcp')

    summary, debug_info = summarizer(text, **summarizer_params)

    # except Exception as e:
    #     return json.dumps({'error': str(e)}, ensure_ascii=False, indent=2)

    # else:
    res = json.dumps({'summary': summary, 'debug_info': debug_info}, ensure_ascii=False, indent=2)

    return res


class Factory(object):

    def __init__(self):
        self.summarizers = {}

    def get_summarizer(self, name):
        '''
        import summarizers on-demand
        '''
        if name in self.summarizers:
            pass
        elif name == 'lexrank':
            from summpy import lexrank
            self.summarizers[name] = lexrank.summarize
        elif name == 'mcp':
            from summpy import mcp_summ
            self.summarizers[name] = mcp_summ.summarize

        return self.summarizers[name]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple web server for summpy")
    parser.add_argument('-H', '--host', default="127.0.0.1", help="the hostname to listen on. default is 127.0.0.1.")
    parser.add_argument('-p', '--port', default="8080", help="the port of the webserver. defualt is 8080.")
    parser.add_argument('-d', '--debug', action="store_true", help="turn debug on if setted")
    o = parser.parse_args()

    app.run(host=o.host, port=int(o.port), debug=o.debug)

