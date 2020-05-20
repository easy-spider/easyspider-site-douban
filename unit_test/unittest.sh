#!/bin/bash
coverage erase
coverage run --source=../ -m unittest
coverage report
coverage html