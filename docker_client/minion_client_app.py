    #!/usr/bin/python

#Import pyhton libraries
import os
import sys
import datetime
import requests
import json
import logging
import yaml
import subprocess

#Static variables
LOG_PATH = "tmp/"
OPRATOR_FILE = "operator_input_file.yaml"
JSON_PAYLOAD = "action_list.json"

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


class Restful_client():
        """ Client script execution """

	def __init__(self, oprator_infile):

            self.oprator_infile = oprator_infile

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

	    self.file_logger.debug("Intialization succeeded")
	    self.common_logger.info("Started logging to " + LOG_PATH + self.logfile)
	
	    self.__read_input_file()

        def run_cmd( self, cmd ):
            """ Function to run shell commands """

            self.file_logger.info("Executing: %s\n" % cmd)
            p = subprocess.Popen(cmd, shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()

            return ( stdout,stderr,p.returncode )


	def __read_input_file( self ):
	    """ Read and parse the input file """

	    try:
		self.tpd = yaml.load( open( self.oprator_infile, 'r' ) )
		minion_hosts = self.tpd["hosts"]
		for i in minion_hosts.keys():
		    if self.ping_host(minion_hosts[i]) == 0:
              	        self.restful_request(minion_hosts[i])
		    else:
			 self.common_logger.info("server " + i + " not reachable, check the connectivity")
			 self.common_logger.error("Orcestration failed, check logfile for more information")
			 sys.exit(1)

	    except yaml.YAMLError as exc:
		self.common_logger.error(exc)

	def ping_host(self, ip_addr):
	    """ Check reachability, ping host IP address provided in the input file """

	    return self.run_cmd("ping -c 1 " + ip_addr)[2]
	    


	def restful_request(self, host_addr):
	    """ Send and check restfull request to server """

	    self.common_logger.info("Intiating restful action on minion servers....")
	    headers = {'Content-Type': 'application/json'}
	    payload = open(JSON_PAYLOAD, "r").read()

	    p = requests.post("http://" + host_addr.strip() + ":5000/actions/cmds", data=payload, headers=headers)
	    #UCL#r = requests.post("http://127.0.0.1:5000/actions/cmds", data=payload, headers=headers)
	    r = requests.get("http://" + host_addr.strip() + ":5000/actions/cmds_status")

	    if p.status_code == 200 and r.status_code == 200:
	        self.common_logger.info("Restfull request posted on server " + host_addr)

	    self.file_logger.debug(p.text)
	    self.file_logger.debug(r.text)

def main():
    """ Trigger actions on server """

    Restful_client(OPRATOR_FILE)
    
if __name__ == "__main__":
    main()
