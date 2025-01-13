<details>
<summary>Debug kubernetes</summary>
![debug KUBE](https://github.com/vyacheslav-PA/netology/blob/cbf32afc02a5af7cf7fe5213b6a4514484d8643c/docs/img/debug.png)
</details>
kubeadm init --pod-network-cidr=10.244.0.0/16 - инициализация кластера
kubeadm token create --print-join-command - получить токен для присоединения ноды к кластеру
