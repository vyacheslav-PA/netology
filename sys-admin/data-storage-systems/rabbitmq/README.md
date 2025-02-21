# Домашнее задание к занятию  «Очереди RabbitMQ» - Перков Вячеслав

---

### Задание 1. Установка RabbitMQ

Используя Vagrant или VirtualBox, создайте виртуальную машину и установите RabbitMQ.
Добавьте management plug-in и зайдите в веб-интерфейс.

*Итогом выполнения домашнего задания будет приложенный скриншот веб-интерфейса RabbitMQ.*



### Решение 1
Веб-интерфейс RabbitMQ:   

![rabbit](https://github.com/vyacheslav-PA/netology/blob/a5e1306437e3c9977ef718724ab9adcea58dd189/sys-admin/data-storage-systems/rabbitmq/img/img-rabbit-1.png)

---

### Задание 2. Отправка и получение сообщений

Используя приложенные скрипты, проведите тестовую отправку и получение сообщения.
Для отправки сообщений необходимо запустить скрипт producer.py.

Для работы скриптов вам необходимо установить Python версии 3 и библиотеку Pika.
Также в скриптах нужно указать IP-адрес машины, на которой запущен RabbitMQ, заменив localhost на нужный IP.


```shell script
$ pip install pika

```

Зайдите в веб-интерфейс, найдите очередь под названием hello и сделайте скриншот.
После чего запустите второй скрипт consumer.py и сделайте скриншот результата выполнения скрипта

*В качестве решения домашнего задания приложите оба скриншота, сделанных на этапе выполнения.*

Для закрепления материала можете попробовать модифицировать скрипты, чтобы поменять название очереди и отправляемое сообщение.


### Решение 2
Очередь в веб-интерфейсе:   

![producer](https://github.com/vyacheslav-PA/netology/blob/a5e1306437e3c9977ef718724ab9adcea58dd189/sys-admin/data-storage-systems/rabbitmq/img/img-rabbit-prod-1.png)   
Скрипт обрабатывает сообщения из очереди:   
![consumer](https://github.com/vyacheslav-PA/netology/blob/a5e1306437e3c9977ef718724ab9adcea58dd189/sys-admin/data-storage-systems/rabbitmq/img/img-rabbit-consumer-1.png)   

---

### Задание 3. Подготовка HA кластера

Используя Vagrant или VirtualBox, создайте вторую виртуальную машину и установите RabbitMQ.
Добавьте в файл hosts название и IP-адрес каждой машины, чтобы машины могли видеть друг друга по имени.

Пример содержимого hosts файла:
```shell script
$ cat /etc/hosts
192.168.0.10 rmq01
192.168.0.11 rmq02
```
После этого ваши машины могут пинговаться по имени.

Затем объедините две машины в кластер и создайте политику ha-all на все очереди.

*В качестве решения домашнего задания приложите скриншоты из веб-интерфейса с информацией о доступных нодах в кластере и включённой политикой.*

Также приложите вывод команды с двух нод:

```shell script
$ rabbitmqctl cluster_status
```

Для закрепления материала снова запустите скрипт producer.py и приложите скриншот выполнения команды на каждой из нод:

```shell script
$ rabbitmqadmin get queue='hello'
```

После чего попробуйте отключить одну из нод, желательно ту, к которой подключались из скрипта, затем поправьте параметры подключения в скрипте consumer.py на вторую ноду и запустите его.

*Приложите скриншот результата работы второго скрипта.*

### Решение 3
Две машины в ожном кластере:   
![cluster_status-0](https://github.com/vyacheslav-PA/netology/blob/a5e1306437e3c9977ef718724ab9adcea58dd189/sys-admin/data-storage-systems/rabbitmq/img/img-rabbit-cluster-0.png)   
cluster status rabbit1:   
![cluster_status-1](https://github.com/vyacheslav-PA/netology/blob/ed1c078c0b241422d1201e24a9a065e405bebd34/sys-admin/data-storage-systems/rabbitmq/img/img-rabbit-cluster-1.png)   
cluster status rabbit1:   
![cluster_status-2](https://github.com/vyacheslav-PA/netology/blob/a5e1306437e3c9977ef718724ab9adcea58dd189/sys-admin/data-storage-systems/rabbitmq/img/img-rabbit-cluster-2.png)   
очередь ноды 1:   
![get_queue-1](https://github.com/vyacheslav-PA/netology/blob/a5e1306437e3c9977ef718724ab9adcea58dd189/sys-admin/data-storage-systems/rabbitmq/img/img-rabbit-get_queue-1.png)   
очередь ноды 2:   
![get_queue-2](https://github.com/vyacheslav-PA/netology/blob/a5e1306437e3c9977ef718724ab9adcea58dd189/sys-admin/data-storage-systems/rabbitmq/img/img-rabbit-get_queue-2.png)    

При отключении одной из нод вторя продолжает работать

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### * Задание 4. Ansible playbook

Напишите плейбук, который будет производить установку RabbitMQ на любое количество нод и объединять их в кластер.
При этом будет автоматически создавать политику ha-all.

*Готовый плейбук разместите в своём репозитории.*