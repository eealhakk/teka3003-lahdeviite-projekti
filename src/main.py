from console_io import ConsoleIO
from app import App

def main():
    io = ConsoleIO()
    app = App(io)
    app.run()

if __name__ == "__main__":
    main()