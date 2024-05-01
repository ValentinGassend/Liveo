from webserver import WebServer
import multiprocessing

myWeb = WebServer('192.168.43.242', 3000)
server_process = multiprocessing.Process(target=myWeb.start)
server_process.start()
