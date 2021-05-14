# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# (C) Copyright IBM Corp. 2020
# Developed by Vincenzo Saturnino (IBM Systems)
# ALL RIGHTS RESERVED

from flask import Flask, render_template, request, jsonify
import atexit
import os
import json
import logging
import logging.handlers
from server import app


#CONFIG VARIABLES
level_logging = os.getenv('LEVEL_LOGGING', 'INFO')
#####

#LOGGING
#LOG_FILENAME = os.path.join(resource_path, 'logging.log')
#LOG_FILENAME = 'logging.log'
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(level_logging)
# create formatter
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(module)s;%(message)s","%Y-%m-%d %H:%M:%S")
# Add the log message handler to the logger
handler = logging.StreamHandler()
#handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=log_maxBytes, backupCount=5)
handler.setFormatter(formatter)
my_logger.addHandler(handler)
############

#RESOURCES FOLDER
#discriminiamo il path in base alla macchina su cui gira l'applicativo
if os.uname()[4] == 'ppc64le':
    resource_path = "/res"
else:
    resource_path = 'res'
    #resource_path = '/Users/it058917/work/ENI/Progetti/git/annotatori/caption/CD-annotator/resources'
#############

fname = os.path.join(resource_path, "vince.txt")


@app.route('/list')
def get_configurations():
    try:
        with open(fname) as f:
            lines = f.readlines()
        result = {"text": lines}
        return jsonify(result), 200

    except Exception as e:
        error = {"error": "internal server error"}
        log = {
            "function" : "list",
            "error": f"{e}"
        }
        my_logger.error(log)
        return jsonify(error), 500

@app.route('/insert', methods=['POST'])
def annotator():
    body = {}
    try:
        #body = request.json
        body2 = request.data
        body = json.loads(body2)

        if 'name' in body:
            name = body['name']
            file_object = open(fname, 'a')
            file_object.write(name)
            file_object.close()
            result = {'message': name}
            log = {
                "input": find_entities['texts'],
                "output": result
            }
            my_logger.info(log)
            return jsonify(result)
       

            log = {
                "input": name,
                "output": result
            }
            my_logger.info(log)
            return jsonify(result)
    except Exception as e:
        error = {"error": "internal server error"}
        log = {
            "function" : "/api/annotator",
            "input": body,
            "error": f"{e}"
        }
        my_logger.error(log)
        return jsonify(error), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)