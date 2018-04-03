import time
import glob
import argparse
import webbrowser
from multiprocessing import Process
from signal import signal, SIGTERM
from player.QLearner import QLearner
from BaseHTTPServer import HTTPServer
from api.ApiPlayerRequestHandler import ApiPlayerRequestHandler
from api.PerformanceRequestHandler import PerformanceRequestHandler

from subprocess import Popen


parser = argparse.ArgumentParser()
parser.add_argument('-fp1','--folder_players1', help='Path to folder with models of first group', required=False)
parser.add_argument('-fp2','--folder_players2', help='Path to folder with models of second group', required=False)
parser.add_argument('-sf','--save_folder', help='Path to folder where to save results', required=False)

def on_sigterm(*va):
    raise SystemExit

def run_performance_api(save_folder, port=8200):
    signal(SIGTERM, on_sigterm)
    try:
        PerformanceRequestHandler.save_folder = save_folder
        httpd = HTTPServer(('0.0.0.0', port), PerformanceRequestHandler)
        while True:
            httpd.handle_request()
    finally:
        print 'Performance Api Proc Closed'

def get_player_files(path):
    return([x[:-6] for x in glob.glob(path + '/*.index')])

def api_player(port, path, name="player_1"):
    cmd = "python main.py -p %d -f %s -n %s" % (port, path, name) # TODO: Agregar parametro para que no aprenda la red
    print cmd
    return Popen(cmd, shell=True)

if __name__ == '__main__':
    args = vars(parser.parse_args())
    path_to_players1 = args['folder_players1']
    path_to_players2 = args['folder_players2']
    save_folder = args['save_folder']
    performance_proc = Process(target=run_performance_api, args=(save_folder,))
    map_port_player = {}

    player1_file_names = get_player_files(path_to_players1)
    player2_file_names = get_player_files(path_to_players2)

    performance_proc.start()

    for base_file_name_1 in player1_file_names:
        player1_proc = api_player(8000, base_file_name_1, 'player1')
        for base_file_name_2 in player2_file_names:
            player2_proc = api_player(8001, base_file_name_2, 'player2')
            print "Esperando 10 segundos antes de levatar el browser"
            time.sleep(10)
            webbrowser.open('http://localhost:8300/performance.html')
            while not PerformanceRequestHandler.performance_measured:
                time.sleep(1)
            else:
                PerformanceRequestHandler.performance_measured = False
                player2_proc.kill()
        player1_proc.kill()
    performance_proc.terminate()
    performance_proc.join()
    
