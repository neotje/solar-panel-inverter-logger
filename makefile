

setup-dev: dependencies
	./setup-venv

dependencies:
	sudo apt install gcc make cpanminus
	sudo cpanm Device::SerialPort
	sudo cpanm Switch
	sudo cpanm DateTime
