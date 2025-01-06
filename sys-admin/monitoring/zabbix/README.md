# Домашнее задание к занятию «Система мониторинга Zabbix» - Перков Вячеслав

---

### Задание 1 

Установите Zabbix Server с веб-интерфейсом.

#### Процесс выполнения
1. Выполняя ДЗ, сверяйтесь с процессом отражённым в записи лекции.
2. Установите PostgreSQL. Для установки достаточна та версия, что есть в системном репозитороии Debian 11.
3. Пользуясь конфигуратором команд с официального сайта, составьте набор команд для установки последней версии Zabbix с поддержкой PostgreSQL и Apache.
4. Выполните все необходимые команды для установки Zabbix Server и Zabbix Web Server.

#### Требования к результаты 
1. Прикрепите в файл README.md скриншот авторизации в админке.
2. Приложите в файл README.md текст использованных команд в GitHub.

### Решение 1   

1.Страница авторизации в zabbix
![admin](https://github.com/vyacheslav-PA/netology/blob/c1fdc19fa3422985fee1655de9dffdf6806d6fd8/sys-admin/monitoring/zabbix/img/img-zabbix-admin.png)   

2.Команды для установки Zabbix Server и Zabbix Web Server

```
 apt install postgresql - установка БД
 wget https://repo.zabbix.com/zabbix/6.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_latest_6.0+ubuntu22.04_all.deb -  скачать скрипт установки репозитория
 dpkg -i zabbix-release_latest_6.0+ubuntu22.04_all.deb - добавить репозиторий zabbix
 apt update - обновить cache 
 apt install zabbix-server-pgsql zabbix-frontend-php php8.1-pgsql zabbix-apache-conf zabbix-sql-scripts  установка Zabbix Server и Zabbix Web Server
 su - postgres -c 'psql --command "CREATE USER zabbix WITH PASSWORD '\'123456789\'';"' - создать пользователя
 su - postgres -c 'psql --command "CREATE DATABASE zabbix OWNER zabbix;"' - создать БД для zabbix 
 zcat /usr/share/zabbix-sql-scripts/postgresql/server.sql.gz | sudo -u zabbix psql zabbix - импорт БД
 sed -i 's/# DBPassword=/DBPassword=123456789/g' /etc/zabbix/zabbix_server.conf - указать пароль БД в конфиг-файле
 systemctl restart zabbix-server zabbix-agent apache2 - запуск сервисов
 systemctl enable zabbix-server zabbix-agent apache2 - добавить сервисы в автозагрузку
 http://host/zabbix - адрес веб интерфейса zabbix

```

---

### Задание 2 

Установите Zabbix Agent на два хоста.

#### Процесс выполнения
1. Выполняя ДЗ, сверяйтесь с процессом отражённым в записи лекции.
2. Установите Zabbix Agent на 2 вирт.машины, одной из них может быть ваш Zabbix Server.
3. Добавьте Zabbix Server в список разрешенных серверов ваших Zabbix Agentов.
4. Добавьте Zabbix Agentов в раздел Configuration > Hosts вашего Zabbix Servera.
5. Проверьте, что в разделе Latest Data начали появляться данные с добавленных агентов.

#### Требования к результаты 
1. Приложите в файл README.md скриншот раздела Configuration > Hosts, где видно, что агенты подключены к серверу
2. Приложите в файл README.md скриншот лога zabbix agent, где видно, что он работает с сервером
3. Приложите в файл README.md скриншот раздела Monitoring > Latest data для обоих хостов, где видны поступающие от агентов данные.
4. Приложите в файл README.md текст использованных команд в GitHub


### Решение 2   
1.Список подключеных хостов
![zabbix hosts](https://github.com/vyacheslav-PA/netology/blob/c1fdc19fa3422985fee1655de9dffdf6806d6fd8/sys-admin/monitoring/zabbix/img/img-zabbix-hosts.png)   

2.Логфайл zabbix-agent
![log](https://github.com/vyacheslav-PA/netology/blob/c1fdc19fa3422985fee1655de9dffdf6806d6fd8/sys-admin/monitoring/zabbix/img/img-zabbix-log.png)   

3.latest data
![latest data](https://github.com/vyacheslav-PA/netology/blob/c1fdc19fa3422985fee1655de9dffdf6806d6fd8/sys-admin/monitoring/zabbix/img/img-zabbix-latestdata.png)  

4.команды для установки Zabbix Agent

``` 
 wget https://repo.zabbix.com/zabbix/6.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_latest_6.0+ubuntu22.04_all.deb - скачать скрипт установки репозитория
 dpkg -i zabbix-release_latest_6.0+ubuntu22.04_all.deb - добавить репозиторий zabbix
 apt update - обновить cache 
 apt install zabbix-agent - установить zabbix-agent
 systemctl restart zabbix-agent - запуск сервисов
 systemctl enable zabbix-agent - добавить сервисы в автозагрузку

```


---
## Задание 3 со звёздочкой*
Установите Zabbix Agent на Windows (компьютер) и подключите его к серверу Zabbix.

#### Требования к результаты 
1. Приложите в файл README.md скриншот раздела Latest Data, где видно свободное место на диске C:
--- 

## Критерии оценки

1. Выполнено минимум 2 обязательных задания
2. Прикреплены требуемые скриншоты и тексты 
3. Задание оформлено в шаблоне с решением и опубликовано на GitHub