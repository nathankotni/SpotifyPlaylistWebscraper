import subprocess
import sys
import get_pip
import contextlib

toInstall = []

file = open("requirements.txt", "r")
toInstall = file.read().splitlines()
for package in toInstall:
    try:
        with contextlib.redirect_stdout(None):
            __import__(package)
        print(package, "already installed")
    except ImportError:
        try:
            try:
                with contextlib.redirect_stdout(None):
                    import pip
            except:
                get_pip.main()
            subprocess.call([sys.executable, "-m", "pip", "install", package])
            with contextlib.redirect_stdout(None):
                __import__(package)
            print(package, "has been installed")
        except Exception as e:
            print("Failed install:", package, "-", e)
file.close()
