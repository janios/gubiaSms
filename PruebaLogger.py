#!/usr/bin/python2
# -*- coding: utf-8 -*-

import yaml


config = yaml.safe_load(open('configuracion.yml'))
print(config['logger.archivo'])