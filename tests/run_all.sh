#!/usr/bin/bash

coverage erase
coverage run -m unittest discover
coverage report --skip-empty --show-missing