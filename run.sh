#!/bin/bash
export PATH="$PATH:/opt/.local/bin"
gunicorn --chdir /opt -w 1 --threads 2 -b 0.0.0.0:8000 --timeout 120 --access-logfile '-' 'app:http()'