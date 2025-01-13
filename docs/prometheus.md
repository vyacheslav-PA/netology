## Install Prometheus
-  useradd prometheus  - создат пользователя
- https://github.com/prometheus/prometheus/releases/download/v3.1.0/prometheus-3.1.0.linux-amd64.tar.gz -скачать архив
- sudo tar -xzf prometheus*.tar.gz - распаковать архив
- sudo groupadd --system prometheus - создать группу
- sudo useradd -s /sbin/nologin --system -g prometheus prometheus - создать пользователя
- sudo mv prometheus /usr/local/bin - переместить исполняемые файлы
- sudo mv promtool /usr/local/bin - переместить исполняемые файлы
- sudo chown prometheus:prometheus /usr/local/bin/prometheus - дать права владения файлами пользователю
- sudo chown prometheus:prometheus /usr/local/bin/promtool - дать права владения файлами пользователю
- sudo mkdir /etc/prometheus - каталог для конфигурации
- sudo mkdir /var/lib/prometheus - каталог для конфигурации
- sudo mv consoles /etc/prometheus - переместить конфиги
- sudo mv console_libraries /etc/prometheus - переместить конфиги
- sudo mv prometheus.yml /etc/prometheus - копировать конфиг файл
- sudo chown prometheus:prometheus /etc/prometheus - права доступа
- sudo chown -R prometheus:prometheus /etc/prometheus/consoles - права доступа
- sudo chown -R prometheus:prometheus /etc/prometheus/console_libraries - права доступа
- sudo chown -R prometheus:prometheus /var/lib/prometheus - права доступа
host:9090  

## Install grafana
- sudo apt-get install -y adduser libfontconfig1 musl
- wget https://dl.grafana.com/oss/release/grafana_11.4.0_amd64.deb
- sudo dpkg -i grafana_11.4.0_amd64.deb
- sudo /bin/systemctl daemon-reload
- sudo /bin/systemctl enable grafana-server
- sudo /bin/systemctl start grafana-server   
host:3000(admin/admin)   


## Install NodeExporter
- wget https://github.com/prometheus/node_exporter/releases/download/v1.8.2/node_exporter-1.8.2.linux-amd64.tar.gz
- tar -xzf *node*
- mkdir /etc/prometheus/node-exporter
- cp *node-exporter* /etc/prometheus/node-exporter/node-exporter
- nano /etc/systemd/system/node-exportet.service   

``` 
[Unit]
Description=Node Exporter
After=network.target
[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/etc/prometheus/node-exporter/node-exporter
[Install]
WantedBy=multi-user.target
```
- nano /etc/prometeus/prometheus.yaml
```
    static_configs:
      - targets: ["localhost:9090", "localhost:9100"]
```
- systemctl restart prometheus   
host:9100   