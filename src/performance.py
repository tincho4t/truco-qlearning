import time
import glob
import argparse
from selenium import webdriver
from player.QLearner import QLearner
from BaseHTTPServer import HTTPServer
from api.ApiPlayerRequestHandler import ApiPlayerRequestHandler
from api.PerformanceRequestHandler import PerformanceRequestHandler

from subprocess import Popen
import psutil

# Python performance.py -fp1 x -fp2 y -sf z

parser = argparse.ArgumentParser()
parser.add_argument('-fp1','--folder_players1', help='Path to folder with models of first group', required=False)
parser.add_argument('-fp2','--folder_players2', help='Path to folder with models of second group', required=False)
parser.add_argument('-sf','--save_folder', help='Path to folder where to save results', required=False)


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def startPerformanceWebServer(save_folder, port=8200):
    PerformanceRequestHandler.save_folder = save_folder
    return HTTPServer(('0.0.0.0', port), PerformanceRequestHandler)

def get_player_files(path):
    return([x[:-6] for x in glob.glob(path + '/*.index')])

def api_player(port, path, name="player_1", hidden=640, learn='n'):
    cmd = "python main.py -p %d -f %s -n %s -hi %d -l %s" % (port, path, name, hidden, learn) # TODO: Agregar parametro para que no aprenda la red
    print cmd
    return Popen(cmd, shell=True)

def get_h1_layer_size(file):
    file_array = file.split('_')
    print(file_array)
    return int(file_array[file_array.index('h1')+1])

if __name__ == '__main__':
    args = vars(parser.parse_args())
    path_to_players1 = args['folder_players1']
    path_to_players2 = args['folder_players2']
    save_folder = args['save_folder']
    httpd = startPerformanceWebServer(save_folder)
    browser = webdriver.Firefox()
    map_port_player = {}

    player1_file_names = get_player_files(path_to_players1)
    player2_file_names = get_player_files(path_to_players2)

    for base_file_name_1 in player1_file_names:
        try:
            player1_h1_nodes = get_h1_layer_size(base_file_name_1)
            player1_proc = api_player(8000, base_file_name_1, 'player1', player1_h1_nodes)
            PerformanceRequestHandler.player_1_file = base_file_name_1
            for base_file_name_2 in player2_file_names:
                try:
                    player2_h1_nodes = get_h1_layer_size(base_file_name_2)
                    player2_proc = api_player(8001, base_file_name_2, 'player2', player2_h1_nodes)
                    PerformanceRequestHandler.player_2_file = base_file_name_2
                    print "Esperando 10 segundos antes de levatar el browser"
                    time.sleep(10)
                    if 'localhost' in browser.current_url:
                        browser.refresh()
                    else:
                        browser.get('http://localhost:8300/performance.html')
                    httpd.handle_request() # ESPERO EL OPTIONS
                    httpd.handle_request() # ESPERO EL POST
                    print "Se termino el torneo"
                except Exception as e: 
                    print(e)
                finally:    
                    print "Matando player 2"
                    kill(player2_proc.pid)
        except Exception as e: 
            print(e)
        finally:
            print "Matando player 1"
            kill(player1_proc.pid)
    
