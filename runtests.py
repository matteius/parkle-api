#!/usr/bin/env python

import os

import pytest


if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


if __name__ == '__main__':
    pytest.main()
