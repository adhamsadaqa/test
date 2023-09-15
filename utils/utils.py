import math
import os
import re
from utils.definitions import YELLOW_CHAR,GREEN_CHAR,RESET_COLOR,ROOT_DIR
import multiprocessing
import time

os.system('color')
DOMAIN_REGEX = r"((?:[a-z0-9A-Z](?:[a-z0-9A-Z-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z0-9])"
DOMAIN_WILDCARD_REGEX = r"(?:\*\.)((?:(?:[a-z0-9A-Z-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z0-9])"

def list_to_file(List, path, mode='w'):
    # #write to data directory if absoulte path was given
    # if(os.path.isabs(path)):
    #     path=f'{__file__}/../../data/{path}'
    # List = [(l.encode('utf-8') if l != None else continue) for l in List]
    filtered_list = list(filter(None, List))
    with open(path, mode) as file:
        file.write("\n".join(filtered_list))



def list_from_file(path):
    with open(path) as file:
        return file.read().split('\n')

def show_progress(value, max, length=100,title=''):
    percentage = math.ceil((value/max)*100)
    finished = math.ceil((value/max)*length)
    remaining=length-finished
    title=title+' -->' if title else title
    print(f"{YELLOW_CHAR}{title} [{'='*finished}{'.'*remaining}:{percentage}%]{RESET_COLOR}", end='\r')
    if percentage==100:
        print("\n")
def filter_domains(unfiltered_list):
    filtered_domains=set()
    for string in unfiltered_list:
        if string !=None:
            matched_domains=re.findall(DOMAIN_REGEX,string)
            filtered_domains.update(matched_domains)
    return filtered_domains


#Filter domains that start with an asterik *.google.com --> google.com
def filter_wildcard_domains(unfiltered_list):
    filtered_domains = set()
    for string in unfiltered_list:
        if string!=None:
            matched_domains = re.findall(DOMAIN_WILDCARD_REGEX, string)
            filtered_domains.update(matched_domains)
    return filtered_domains

def parse_multithread_args(*args):
    parsed_args=[]
    max_length=max([len(arg) for arg in args if isinstance(arg,list)])
    max_indexs=[i for i,arg in enumerate(args) if isinstance(arg,list) and len(arg)==max_length ]
    for i in range(max_length):
        parsed_args.append([None]*len(args))
        for arg_index,arg in enumerate(args):
            if arg_index in max_indexs:
                parsed_args[i][arg_index]=arg[i]
            else:
                parsed_args[i][arg_index]=arg
    return parsed_args


def multithread(target,args,threads_num=10,progress_title=False):
    # manager = multiprocessing.Manager()
    # args_current_index=manager.Namespace()
    args_current_index=0
    threads_pool = [None]*threads_num

    while args_current_index<len(args):
        for thread_index,thread in enumerate(threads_pool):
            if (args_current_index<len(args) and (thread==None or thread.is_alive()==False)):
                # args_list=[args[args_current_index]] if isinstance(args[args_current_index])
                threads_pool[thread_index]=multiprocessing.Process(target=target, args=args[args_current_index])
                threads_pool[thread_index].start()
                args_current_index+=1
        if(progress_title):
            show_progress(args_current_index,len(args),title=progress_title)
        time.sleep(0.5)