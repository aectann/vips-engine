__author__ = 'konstantin.burov'
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

__version__ = '0.0.1'

try:
    from vips_engine.engine import Engine  # NOQA
except ImportError:
    logging.exception('Could not import vips. Probably due to setup.py installing it.')
