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

class ApiPlayerRequestHandlerPlayer2(ApiPlayerRequestHandler):
    pass

def api_player(player_class, port=8000):
    signal(SIGTERM, on_sigterm)
    try:
        httpd = HTTPServer(('0.0.0.0', port), ApiPlayerRequestHandler)
        while True:
            httpd.handle_request()
    finally:
        print 'player dead'

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
        ApiPlayerRequestHandler.player = QLearner('player1', base_file_name_1)
        player1_proc = Process(target=api_player, args=(ApiPlayerRequestHandler, 8000))
        PerformanceRequestHandler.player_1_file = base_file_name_1
        player1_proc.start()
        for base_file_name_2 in player2_file_names:
            ApiPlayerRequestHandler.player = QLearner('player2', base_file_name_2)
            player2_proc = Process(target=api_player, args=(ApiPlayerRequestHandlerPlayer2, 8001))
            PerformanceRequestHandler.player_2_file = base_file_name_2
            player2_proc.start()
            webbrowser.open('http://localhost:8300/performance.html')
            while not PerformanceRequestHandler.performance_measured:
                time.sleep(1)
            else:
                PerformanceRequestHandler.performance_measured = False
                player2_proc.terminate()
                player2_proc.join()       
        player1_proc.terminate()
        player1_proc.join()
    performance_proc.terminate()
    performance_proc.join()
    
