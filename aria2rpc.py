#!/usr/bin/env python2

import urllib2
import json
from argparse import ArgumentParser
from collections import defaultdict

parser = ArgumentParser()
parser.add_argument('-U', '--user-agent', help='user-agent', type=str,
                    default='', metavar='USER_AGENT', dest='user_agent')
parser.add_argument('-c', '--cookie', help='use cookies', type=str,
                    default='', metavar='COOKIES', dest='cookies')
parser.add_argument('-o', '--output', help='output name', type=str,
                    default='', metavar='NAME', dest='output')
parser.add_argument('-d', '--dir', help='dest dir (server side)', type=str,
                    default='', metavar='DIR', dest='dir')
parser.add_argument('-R', '--rpc',
                    help='aria2 rpc (http://localhost:6800/jsonroc)',
                    type=str, default='http://127.0.0.1:6800/jsonrpc',
                    metavar='URL', dest='rpc')
parser.add_argument('-s', '--secret', dest='secret', default='',
                    metavar='TOKEN', help='token')
parser.add_argument('-u', '--user', dest='user', default='',
                    metavar='USER', help='user name (deprecated)')
parser.add_argument('-p', '--passwd', dest='pw', default='',
                    metavar='PASSWD', help='password (deprecated)')
parser.add_argument('-r', '--referer', help='referer', default='', type=str,
                    metavar='URL', dest='referer')
parser.add_argument('-H', '--host', dest='host', default='')
parser.add_argument('URIs', nargs='+', help='URIs', type=str,
                    default='', metavar='URI')
opts = parser.parse_args()

jsondict = {'jsonrpc':'2.0',
		    'id':'aria2rpc',
		    'method':'aria2.addUri'}

jsondict['params'] = []
if opts.secret:
    jsondict['params'].append('token:{0}'.format(opts.secret))
jsondict['params'].append(opts.URIs)

aria2optsDefault = {}

aria2opts = defaultdict(lambda: [])
aria2opts.update(aria2optsDefault)

if opts.user_agent:
    aria2opts['user-agent'] = opts.user_agent
if opts.output:
    aria2opts['out'] = opts.output
if opts.dir:
    aria2opts['dir'] = opts.dir
if opts.referer:
    aria2opts['referer'] = opts.referer
if opts.cookies:
    aria2opts['header'].append('Cookie: {0}'.format(opts.cookies))
if opts.host:
    aria2opts['header'].append('Host: {0}'.format(opts.host))
if opts.secret:
    aria2opts['rpc-secret'] = opts.secret

if not opts.secret and opts.user and opts.passwd:
    aria2opts['rpc-user'] = opts.user
    aria2opts['rpc-passwd'] = opts.pw

jsondict['params'].append(aria2opts)

jsonreq = json.dumps(jsondict)

print urllib2.urlopen(opts.rpc, jsonreq).read()
