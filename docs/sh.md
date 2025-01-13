## NETWORK
- ip link set enp0s3 up - включить интерфейс
- ip addr add 192.168.1.111/255.255.255.0 dev enp0s3- прописать ip
- ip route add default via 192.168.1.1  -  прописать gateway
- systemctl restart networking - перезапустить сетевую службу
   
## 
- hostname - посмотреть имя хоста
- useradd <username> - создать пользователя
-    
## АРХИВ
- tar -xvf filename.tar.gz -C /tmp/yourdir - распаковать архив

