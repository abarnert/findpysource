#!/usr/bin/env python3

import inspect
import sys
from bs4 import BeautifulSoup
import requests

_vi = sys.version_info
_pyver = f'{_vi.major}.{_vi.minor}'
_modules = {}
def _getmodules():
    if not _modules:
        r = requests.get(f'https://github.com/python/cpython/tree/{_pyver}/Modules')
        soup = BeautifulSoup(r.text, 'lxml')
        for td in soup.find_all('td', {'class': 'content'}):
            for a in td.find_all('a', {'class': 'js-navigation-open'}):
                name = a.text
                # TODO: handle directories
                if name.endswith('.c'):
                    name = name.split('.c')[0].split('module')[0]
                    _modules[name] = 'https://github.com' + a['href']
        _modules['os'] = _modules['posix']
        r = requests.get(f'https://github.com/python/cpython/tree/{_pyver}/Python')
        soup = BeautifulSoup(r.text, 'lxml')
        for td in soup.find_all('td', {'class': 'content'}):
            for a in td.find_all('a', {'class': 'js-navigation-open'}):
                name = a.text
                if name == 'bltinmodule.c':
                    _modules['builtin'] = 'https://github.com' + a['href']
                elif name == 'sysmodule.c':
                    _modules['sys'] = 'https://github.com' + a['href']
    return _modules

def getsourceurl(object):
    modules = _getmodules()
    if inspect.ismodule(object):
        mod = object.__name__
    else:
        mod = object.__module__
    return modules[mod]

if __name__ == '__main__':
    modules = _getmodules()
    for mod in sys.argv[1:]:
        try:
            print(modules[mod])
        except KeyError:
            print(f'{mod}: NOT FOUND', file=sys.stderr)
