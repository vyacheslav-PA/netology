Установка Zabbix server на Debian 11
С помощью инструкции с официального сайта установите Zabbix server 
на операционную систему:
Установите PostgreSQL:
sudo apt install postgresql
Добавьте репозиторий Zabbix:
wget https://repo.zabbix.com/zabbix/6.0/debian/pool/main/z/zabbix-release/zabbix-release_6.0-4%2Bdebian11_all.deb
dpkg -i zabbix-release_6.0-4+debian11_all.deb
apt update
Запустите Zabbix server:
sudo apt install zabbix-server-pgsql zabbix-frontend-php php7.4-pgsql zabbix-apache-conf zabbix-sql-scripts nano -y # zabbix-agent
Создайте пользователя БД:
sudo -u postgres createuser --pwprompt zabbix
Создайте БД:
sudo -u postgres createdb -O zabbix zabbix

su - postgres -c 'psql --command "CREATE USER zabbix WITH PASSWORD '\'123456789\'';"'
su - postgres -c 'psql --command "CREATE DATABASE zabbix OWNER zabbix;"'

sed -i 's/# DBPassword=/DBPassword=123456789/g' /etc/zabbix/zabbix_server.conf