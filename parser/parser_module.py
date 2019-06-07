#! /usr/bin/env python 

'''A light-weight parser to extract outguard features.

'''
import sys
import math 
import json 
import struct 
import random
import scipy
import datetime
import numpy as np 
import logging
import time
import os 
import ast
import operator
import itertools
import gzip
import logging
import re
import urlparse
import csv



try:
    import ujson as json 
except BaseException:
    import json


class CryptoDetect(object):
    def __init__(self,options):
        self.devtools_file = ''
        self.target_folder = options.trace_folder
        self.out_file = options.out
        self.blob_url = ''
        self.websocket_url = ''
        self.wasm = 0
        self.hash_function= 0
        self.no_workers = 0
        self.messageloop = 0
        self.postmessage = 0
        self.parallel_functions = 0
    def reset(self,options):
        self.__init__(options)
  
       
    def detecting_hashfunction_wasm(self,raw_events):
        hash_function_sig = ["Cryptonight", "wasmwrapper", "neoscript","scrypt"]
        try:
            for raw_event in raw_events:
                if raw_event['cat'] == "disabled-by-default-v8.cpu_profiler":
                    for arg, val in raw_event["args"].iteritems():
                        if arg == "data":
                            for a,v in val.iteritems():
                                if isinstance(v, dict):
                                    for s,p in v.iteritems():
                                        if s == "nodes":
                                            for n,d in p[0].iteritems():
                                                if n == "callFrame":
                                                    try:
                                                       if d['url'] == "(wasm)":
                                                            self.wasm = 1
                                                    except:
                                                        pass
                                                        
                                                    if [element for element in hash_function_sig if element in d['functionName']] :
                                        
                                                        self.hash_function = 1
                           
        except Exception as e: print(e)

    def detecting_blob_socket(self, raw_events):
        try:
            for raw_event in raw_events:
                  if raw_event['cat'] == 'devtools.timeline':
                    for key, value in raw_event.iteritems():
                        if key == 'args':
                            for k,v in value.iteritems():
                                for s,p in v.iteritems():
                                    if s=="url":
                                        if p.startswith('blob:https://'):
                                            self.blob_url= p
                                         
                                        elif p.startswith('wss') or p.startswith('ws'):
                                            self.websocket_url = p
                                            break
                    
                        else:
                            if key == 'name' and value =="FunctionCall":
                                for key, value in raw_event["args"].iteritems():
                                    if value['url'].startswith("blob:http"):
                                        self.blob_url= p
                                      
                  else:
                    continue
        except Exception as e: print(e)

    def message_loop(self, raw_events):
        try:
            for raw_event in raw_events:
                if raw_event['cat'] == 'toplevel':

                    for key, value in raw_event.iteritems():
                        if key == "args":

                            for a,b in value.iteritems():

                                if b == "../../third_party/WebKit/Source/platform/scheduler/base/thread_controller_impl.cc":
                                    
                                    if raw_event['args']['src_func'] == 'ScheduleWork':
                                        try:
                                            self.messageloop = self.messageloop + raw_event['dur']
                                        except Exception as e:
                                            logging.error(e)

                        if raw_event['name'] == "TaskQueueManager::ProcessTaskFromWorkQueue":
                            if raw_event['args']['src_func'] == "PostMessageToWorkerGlobalScope":
                                try:
                                    self.postmessage = self.postmessage + raw_event['dur']           
                                except Exception as e:
                                    logging.error(e)
                          
        except Exception as e: print(e)


    def parallel_tasks(self,raw_events):
        tid = {}
        try:
            for raw_event in raw_events:
                if raw_event['cat'] == 'devtools.timeline':
                    for key, value in raw_event.iteritems():
                        if key == 'args':
                            for k,v in value.iteritems():
                                for s,p in v.iteritems():
                                    if s == 'functionName':
                                        if raw_event['tid'] not in tid:
                                            tid[raw_event['tid']]= [p]   
                                        else:
                                            if p not in tid[raw_event['tid']]:
                                                tid[raw_event['tid']].append(p)

                             
            listed_values = [item for sublist in tid.values() for item in sublist]
            duplicates = []
            for i in listed_values:
                if listed_values.count(i) > 1:
                    duplicates.append(i)
            if duplicates:
                self.parallel_functions = ", ".join(str(e) for e in set(duplicates))
            
        
        except Exception as e: print(e)   
    def workers(self,raw_events):
        try:
            worker_count =0
            workers_id = []
            parallel_worker = {}
            for raw_event in raw_events:
                if raw_event['cat'] == '__metadata':
                    for key, value in raw_event.iteritems():
                        if key == 'args':
                            for k,v in value.iteritems():
                                if v =="DedicatedWorker Thread":
                                    workers_id.append(raw_event['tid'])
                                    parallel_worker[raw_event['tid']] = raw_event['pid']     

                else:
                
                    continue
            #print parallel_worker
            self.no_workers = len(workers_id)
        except Exception as e: print(e)
    def path_creation(self, file_path):
        self.devtools_file = file_path
        print ("[+] parsing %s"%self.devtools_file)
        f_in = open("./"+self.target_folder+"/"+self.devtools_file.split(".devtools.trace")[0]+"/"+self.devtools_file,'r')
        #f_in = open("./"+self.target_folder+"/"+self.devtools_file,'r')
        return f_in
    def feature_setup(self):

        features = []
        if self.websocket_url:
            features.append(1)
        else:
            features.append(0)
        features.append(self.wasm)
        features.append(self.hash_function)
        features.append(self.no_workers)
        features.append(self.messageloop)
        features.append(self.postmessage)
        if self.parallel_functions:
            features.append(1)
        else:
            features.append(0)
        print "[+] Corresponding features: %s"%(features)
        return features

    def output_file(self,vectors):
     
        file_exists = os.path.isfile(self.out_file)
        with open (self.out_file, 'a') as csvfile:
            headers = ['websocket','wasm','hash_function','webworkers', 
                    'messageloop_load','postmessage_load','parallel_functions']
        
            writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            #writer = csv.writer(filename, delimiter=',')
            if not file_exists:
                writer.writerow(headers)  # file doesn't exist yet, write a header

   
      
            #writer.writerow(header)
            writer.writerow(vectors)
       

    def process(self,options):
    

        for root, dir, files in os.walk(self.target_folder):

          try:
            for datafile in files:
              if datafile.endswith(".devtools.trace"):
                #worker_count = 0	
                detection_features = {'path':'','message_loop':0,'is_blob_available':0, 'wasm':0 ,'established_websocket':0, "hash_function":0, 'parallel_worker':0, 'is_worker_queue':0}
                raw_events = json.load(self.path_creation(datafile))
                self.detecting_blob_socket(raw_events)
                self.detecting_hashfunction_wasm(raw_events)
                self.workers(raw_events)
                self.message_loop(raw_events)
                self.parallel_tasks(raw_events)
                #self.postmessage(raw_events)
                #print self.blob_url
                #print self.websocket_url
                #print self.devtools_file
                #print self.wasm
                #print self.hash_function
                #print self.no_workers
                #print self.messageloop
                #print self.postmessage
                #print self.parallel_functions
                detection_features = self.feature_setup()

                self.output_file(detection_features)
                self.reset(options)

               
          except Exception as e: print(e)  
        
	
    
def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(description='Chrome trace parser.',
                                     prog='trace-parser')
    parser.add_argument('-v', '--verbose', action='count',
                        help="Increase verbosity (specify multiple times for more)" \
                             ". -vvvv for full debug output.")
    parser.add_argument('-d', '--trace_folder', help="Input trace folder.")
    parser.add_argument('-o', '--out', help="Output requests json file.")
    #parser.add_argument('-l', '--label', help = "label of the input")
    options, _ = parser.parse_known_args()

    # Set up logging
    log_level = logging.CRITICAL
    if options.verbose == 1:
        log_level = logging.ERROR
    elif options.verbose == 2:
        log_level = logging.WARNING
    elif options.verbose == 3:
        log_level = logging.INFO
    elif options.verbose >= 4:
        log_level = logging.DEBUG
    logging.basicConfig(
        level=log_level, format="%(asctime)s.%(msecs)03d - %(message)s", datefmt="%H:%M:%S")

    if not options.trace_folder or not options.out:
        parser.error("Input devtools or output file is not specified.")
    start = time.time()
    devtools = CryptoDetect(options)
    devtools.process(options)

if __name__ == '__main__':
    main()




