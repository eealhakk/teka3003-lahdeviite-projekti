from console_io import ConsoleIO

def test_console_io_write(capsys):
    io = ConsoleIO()

    io.write("Hei maailma!")

    captured = capsys.readouterr()
    assert captured.out.strip() == "Hei maailma!"