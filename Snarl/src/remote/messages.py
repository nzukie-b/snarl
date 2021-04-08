import sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from constants import WELCOME

class Welcome:
    def __init__(self, server_info):
        self.type = WELCOME
        self.info = server_info
    
    def __str__(self):
        return '{{"type": {}, "info": {}}}'.format(self.type, self.info)
        