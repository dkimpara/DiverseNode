#from experimentRunner import *
from reprocess import modify_main

if __name__ == '__main__':  # run experiments for sayama
    #sayama_base('base')
    #sayama_change_all()
    #change_group_size()
    
    modify_main('base')
    modify_main('sayama_change_all')
    modify_main('group_size17-34_changeall')
    modify_main('group_size17-34')
    modify_main('group_size10-40_changeall')
    modify_main('group_size10-40')