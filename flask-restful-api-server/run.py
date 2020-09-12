#!/usr/bin/env python3
import logging
from har_restapi import create_app

app = create_app()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s-%(funcName)s: %(message)s',
    datefmt='%H:%M:%S')

if __name__ == '__main__':
    app.run(debug=True)
