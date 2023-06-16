from controller import Controller
from model import Model
from view import TkView

DB_FILE_NAME = "ipsplash.db"


def main():
    ips_app = Controller(Model(DB_FILE_NAME), TkView())
    ips_app.start()


if __name__ == "__main__":
    main()
