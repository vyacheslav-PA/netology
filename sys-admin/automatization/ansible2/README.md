# Домашнее задание к занятию "`Ansible.Часть 2" - `Перков Вячеслав`

---

### Задание 1   

**Выполните действия, приложите файлы с плейбуками и вывод выполнения.**

Напишите три плейбука. При написании рекомендуем использовать текстовый редактор с подсветкой синтаксиса YAML.

Плейбуки должны: 

1. Скачать какой-либо архив, создать папку для распаковки и распаковать скачанный архив. Например, можете использовать [официальный сайт](https://kafka.apache.org/downloads) и зеркало Apache Kafka. При этом можно скачать как исходный код, так и бинарные файлы, запакованные в архив — в нашем задании не принципиально.
2. Установить пакет tuned из стандартного репозитория вашей ОС. Запустить его, как демон — конфигурационный файл systemd появится автоматически при установке. Добавить tuned в автозагрузку.
3. Изменить приветствие системы (motd) при входе на любое другое. Пожалуйста, в этом задании используйте переменную для задания приветствия. Переменную можно задавать любым удобным способом.

### Решение 1  

1. playbook1 - скачать и распаковать архив

```
- hosts: ansible72
  tasks:
         - name: Ping hosts
           ansible.builtin.ping:
         - name: Download kafka.tgz
           ansible.builtin.get_url:
             url: https://dlcdn.apache.org/kafka/3.9.0/kafka-3.9.0-src.tgz
             dest: /home/ubuntu/kafka.tgz
         - name: Extract kafka.tgz
           ansible.builtin.unarchive:  
             src: /home/ubuntu/kafka.tgz
             dest: /home/ubuntu/
             remote_src: yes

```
![download&unzip](https://github.com/vyacheslav-PA/7-1-ansible-hw/blob/f407bd9edccf5dc1f65bba080a40a7e279c96c71/ansible72/img/ansible-72-1-1.png)

2. playbook2 - установить пакет и добавит в автозагрузку

```
- hosts: ansible72
  become: yes
  tasks:
        - name: Install tuned
          ansible.builtin.apt:
            name: tuned
            state: present
            update_cache: yes
        - name: Start tuned
          service:
            name: tuned
            state: started
            enabled: true

```
![service](https://github.com/vyacheslav-PA/7-1-ansible-hw/blob/2046c70de4c715c48574b53d410be828f36afc29/ansible72/img/ansible-72-1-2.png)

3. playbook3 - изменить приветствие системы

```
- hosts: ansible72
  become: yes
  vars:
    helloUbuntu: printf "a new line for motd"
  tasks:
  - name: Add a line to a file if the file does not exist, without passing regexp
    ansible.builtin.lineinfile:
      path: /etc/update-motd.d/00-header 
      line: "{{ helloUbuntu }}"

```
![motd](https://github.com/vyacheslav-PA/7-1-ansible-hw/blob/2046c70de4c715c48574b53d410be828f36afc29/ansible72/img/ansible-72-1-3.png)

---

### Задание 2

**Выполните действия, приложите файлы с модифицированным плейбуком и вывод выполнения.** 

Модифицируйте плейбук из пункта 3, задания 1. В качестве приветствия он должен установить IP-адрес и hostname управляемого хоста, пожелание хорошего дня системному администратору.  

### Решение 2  

playbook

```
- hosts: ansible72
  gather_facts: yes
  become: yes
  vars:
    scriptline1: '#!/bin/sh'
    scriptline2: 'Пожелание хорошего дня системному администратору)'
    pathfilesmotd: "/etc/update-motd.d"
    pathnewfilemotd: "/etc/update-motd.d/01-newmotd"
  tasks:
  - name: change file permission #убрать права на исполнение дефолтных скриптов
    ansible.builtin.file:
      state: directory
      recurse: yes
      path: "{{ pathfilesmotd }}"
      mode: -x
  - name: Creating a script #создать файл скрипта приветствия
    copy:
      dest: "{{ pathnewfilemotd }}"
      mode: 0774
      content: |
          {{ scriptline1 }}
          echo '{{ scriptline2 }}'
          echo 'имя хоста: {{ ansible_facts['hostname'] }}'
          echo 'ip адрес хоста: {{ ansible_facts['default_ipv4']['address']}}'

```
![new-motd](https://github.com/vyacheslav-PA/7-1-ansible-hw/blob/9a14dfc551e2eb914e635f9301aaffd00725c735/ansible72/img/ansible-72-2-1.png)
---

### Задание 3

**Выполните действия, приложите архив с ролью и вывод выполнения.**

Ознакомьтесь со статьёй [«Ansible - это вам не bash»](https://habr.com/ru/post/494738/), сделайте соответствующие выводы и не используйте модули **shell** или **command** при выполнении задания.

Создайте плейбук, который будет включать в себя одну, созданную вами роль. Роль должна:

1. Установить веб-сервер Apache на управляемые хосты.
2. Сконфигурировать файл index.html c выводом характеристик каждого компьютера как веб-страницу по умолчанию для Apache. Необходимо включить CPU, RAM, величину первого HDD, IP-адрес.
Используйте [Ansible facts](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_vars_facts.html) и [jinja2-template](https://linuxways.net/centos/how-to-use-the-jinja2-template-in-ansible/). Необходимо реализовать handler: перезапуск Apache только в случае изменения файла конфигурации Apache.
4. Открыть порт 80, если необходимо, запустить сервер и добавить его в автозагрузку.
5. Сделать проверку доступности веб-сайта (ответ 200, модуль uri).

В качестве решения:
- предоставьте плейбук, использующий роль;
- разместите архив созданной роли у себя на Google диске и приложите ссылку на роль в своём решении;
- предоставьте скриншоты выполнения плейбука;
- предоставьте скриншот браузера, отображающего сконфигурированный index.html в качестве сайта.
  
### Решение 3  

main.yaml
```
- hosts: ansible72
  gather_facts: yes
  become: yes
  tasks:
      - include_tasks: "{{ ansible_os_family }}.yaml"

```
Debian.yaml
```
  - name: Install web server
    ansible.builtin.apt:
      name: "apache2"
      state: present
  - name: Start Apache 
    ansible.builtin.service:
      name: apache2
      state: started
      enabled: true
  - include_tasks: "debianconfig.yaml"

```
debianconfig.yaml
```
- name: Create index.html using Jinja2
  template:
    src: ../templates/index.j2
    dest: /var/www/html/index.html

```

###### Запуск playbook
![role](https://github.com/vyacheslav-PA/7-1-ansible-hw/blob/0d726d5647e74cafc99b84953e65e1dd46ddeecf/ansible72/img/ansible-72-3-1.png)  
###### Страница в браузере
![browser](https://github.com/vyacheslav-PA/7-1-ansible-hw/blob/0d726d5647e74cafc99b84953e65e1dd46ddeecf/ansible72/img/ansible-72-3-2.png)

---
