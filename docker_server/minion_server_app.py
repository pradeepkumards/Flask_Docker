#!/usr/bin/python

##Import pyhton libraries
import os
import sys
import datetime
import subprocess
import logging
from flask import Flask, jsonify, request, make_response

#Static variables
LOG_PATH = "tmp/"

#Directory for logs and done file
if os.path.exists('tmp/') is not True:
    os.mkdir('tmp') 

#Check python version
#Note: have python virtual environment
sys.exit("Error: Use Python version less then 3") if not sys.version_info < (3,0,0) else None


class Whitelist(logging.Filter):
    """Logs filtering to separate out console and file logging"""

    def __init__(self, *whitelist):
        self.whitelist = [logging.Filter(name) for name in whitelist]

    def filter(self, record):
        record.levelno <= logging.CRITICAL
        return any(f.filter(record) for f in self.whitelist)


class Shell_execute():
        """ Execute script on minion server """

        def __init__( self ):

            #Loggging to file only, console only and both
            self.logfile =  os.path.basename(__file__).replace('.py','_') + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            self.file_logger = logging.getLogger('file')
            self.file_handler = logging.FileHandler(LOG_PATH + self.logfile)
            self.formatstr = '%(asctime)s - %(levelname)s - %(message)s'
            self.formatter = logging.Formatter(self.formatstr)
            self.file_handler.setFormatter(self.formatter)
            self.file_logger.addHandler(self.file_handler)

            self.console_logger = logging.getLogger('console')
            self.common_logger = logging.getLogger('common')
            self.common_logger.addHandler(self.file_handler)

            logging.basicConfig(level=logging.NOTSET,
                                    format='%(asctime)s %(levelname)-8s  %(message)s',
                                    datefmt='%a, %d %b %Y %H:%M:%S')
            for handler in logging.root.handlers:
                handler.addFilter(Whitelist('console', 'common'))
	    self.common_logger.info("Started logging to " + LOG_PATH + "/" + self.logfile)


        def run_cmd( self, cmd ):
            """ Function to run shell commands """

            self.file_logger.info("Executing: %s\n" % cmd)
            p = subprocess.Popen(cmd, shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()

            return ( stdout,stderr,p.returncode )


cmd_exec = Shell_execute()

#Flask to create a RESTFULL appliaction
app = Flask(__name__)
@app.route('/actions/cmds', methods=['POST'])
def restful_cmd_execute():
    cmd_list = request.json['action']
   
    for cmd in cmd_list:
        cmd_out = cmd_exec.run_cmd('python script_cmd.py '+  cmd)
	cmd_exec.file_logger.info("Command output "+ str(cmd_out))
	if not cmd_out[2]:
	    open(LOG_PATH + os.path.basename(__file__).replace('.py','.done'), "w").close()
    if os.path.exists(LOG_PATH + os.path.basename(__file__).replace('.py','.done')):
        return jsonify({'actions': cmd_list, 'status': 'successful'})
	    
#Request to check the status of execution
@app.route('/actions/cmds_status', methods=['GET'])
def get_tasks():
    if os.path.exists(LOG_PATH + os.path.basename(__file__).replace('.py','.done')):
        return jsonify({'status': 'successful'})

#Captured few error hanlders, can be extended to more error handlers
@app.errorhandler(400)
def restful_check_file(error):
    return make_response(jsonify({'error': 'JSON File Not found'}), 400)

@app.errorhandler(404)
def restful_check_file(error):
    return make_response(jsonify({'error': 'Wrong command triggered'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
