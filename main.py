import socket
import select
import errno
import sys
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)


class MyGrid(Widget):
    name = ObjectProperty(None)
    email = ObjectProperty(None)

    def btn(self):
        print(self.name.text)
        message = self.name.text
        if message:
            message = message.encode('utf-8')
            message_header = f'{len(message):<{HEADER_LENGTH}}'.encode('utf-8')
            client_socket.send(message_header + message)
        try:
            while True:
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')
                print(f'{message_length}')
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error ', str(e))
                sys.exit()
        except Exception as e:
            print('General error', str(e))
            sys.exit()
        self.name.text = ""


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()

