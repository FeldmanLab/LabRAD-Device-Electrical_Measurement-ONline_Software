import subprocess
import time


labrad_file = open('.\\labrad_output.txt','w')
web_server_file = open('.\\labrad_web_output.txt','w')
node_file = open('.\\node_output.txt','w')
subprocess.Popen(['labrad'], shell=True, stdout = labrad_file)
print('Labrad started')
subprocess.Popen(['labrad-web'], shell=True, stdout = web_server_file)
print('Web server started')
time.sleep(3)

subprocess.Popen(['python','-m','labrad.node'],stdout = node_file,stderr=subprocess.STDOUT)

print('Labrad servers opened')
