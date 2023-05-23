sudo useradd -m -G sudo tgrepbot
sudo mkdir /home/tgrepbot/tgrepostbot
sudo cp -a ./{*,.*} /home/tgrepbot/tgrepostbot
sudo chown -R tgrepbot:tgrepbot /home/tgrepbot/tgrepostbot
sudo locale-gen ru_RU.utf8
sudo update-locale LANG=ru_RU.UTF8
sudo apt-get update
sudo apt-get -y install python3 python3-pip python3.8-venv
sudo python3 -m venv /home/tgrepbot/tgrepostbot/venv
sudo cp tgrepbot.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start tgrepbot.service
sudo systemctl enable tgrepbot.service
