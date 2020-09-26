import os
import re

a = os.popen("curl -s http://icanhazip.com").read()

print a
