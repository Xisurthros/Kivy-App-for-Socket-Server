import socket
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class MyGrid(Widget):
    HEADER_LENGTH = 10
    IP = '192.168.1.71'
    PORT = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)

    name = ObjectProperty(None)
    email = ObjectProperty(None)

    def btn(self):
        message = self.name.text
        if message:
            message = message.encode('utf-8')
            message_header = f'{len(message):<{self.HEADER_LENGTH}}'.encode('utf-8')
            self.client_socket.send(message_header + message)
        try:
            while True:
                username_header = self.client_socket.recv(self.HEADER_LENGTH)
                if not len(username_header):
                    print('Connection closed by the server')
                username_length = int(username_header.decode('utf-8').strip())
                username = self.client_socket.recv(username_length).decode('utf-8')
                message_header = self.client_socket.recv(self.HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = self.client_socket.recv(message_length).decode('utf-8')

        except:
            pass
        self.name.text = ""


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()

