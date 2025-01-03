# Домашнее задание к занятию «Что такое DevOps. СI/СD»

### Задание 1

**Что нужно сделать:**

1. Установите себе jenkins по инструкции из лекции или любым другим способом из официальной документации. Использовать Docker в этом задании нежелательно.
2. Установите на машину с jenkins [golang](https://golang.org/doc/install).
3. Используя свой аккаунт на GitHub, сделайте себе форк [репозитория](https://github.com/netology-code/sdvps-materials.git). В этом же репозитории находится [дополнительный материал для выполнения ДЗ](https://github.com/netology-code/sdvps-materials/blob/main/CICD/8.2-hw.md).
3. Создайте в jenkins Freestyle Project, подключите получившийся репозиторий к нему и произведите запуск тестов и сборку проекта ```go test .``` и  ```docker build .```.

В качестве ответа пришлите скриншоты с настройками проекта и результатами выполнения сборки.
   
### Решение 1   

Jenkins установлен локально   
![jenkins settings](https://github.com/vyacheslav-PA/netology/blob/a95dd095d169e471fe3bc933ae47df14ce5b40ff/sys-admin/automatization/CICD-1/img/img-settings-git-jenkins.png)
![jenkins settings](https://github.com/vyacheslav-PA/netology/blob/c7f61e9b13f482fabf9f3ead3191f35f822e926f/sys-admin/automatization/CICD-1/img/img-settings-script-jenkins.png)   

nexus развернут в кубернетес   
![kube-nexus](https://github.com/vyacheslav-PA/netology/blob/a95dd095d169e471fe3bc933ae47df14ce5b40ff/sys-admin/automatization/CICD-1/img/img-nexus.png)   

сборки 7,8,9 завершились удачной сборкой контенера   
![docker-images](https://github.com/vyacheslav-PA/netology/blob/a95dd095d169e471fe3bc933ae47df14ce5b40ff/sys-admin/automatization/CICD-1/img/img-docker-images.png)   


##### Вывод консоли jenkins после успешной сборки всего проекта (#9)   
```
Started by user admin
Running as SYSTEM
Building in workspace /var/lib/jenkins/workspace/freestyle1
The recommended git tool is: NONE
No credentials specified
 > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/freestyle1/.git # timeout=10
Fetching changes from the remote Git repository
 > git config remote.origin.url https://github.com/vyacheslav-PA/gojenkins.git # timeout=10
Fetching upstream changes from https://github.com/vyacheslav-PA/gojenkins.git
 > git --version # timeout=10
 > git --version # 'git version 2.43.0'
 > git fetch --tags --force --progress -- https://github.com/vyacheslav-PA/gojenkins.git +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git rev-parse refs/remotes/origin/main^{commit} # timeout=10
Checking out Revision 683c31a61b456e4cbe9488760179560d2675ee66 (refs/remotes/origin/main)
 > git config core.sparsecheckout # timeout=10
 > git checkout -f 683c31a61b456e4cbe9488760179560d2675ee66 # timeout=10
Commit message: "rm files"
 > git rev-list --no-walk 683c31a61b456e4cbe9488760179560d2675ee66 # timeout=10
[freestyle1] $ /bin/sh -xe /tmp/jenkins14079452769450189845.sh
+ /usr/bin/go test .
ok  	github.com/netology-code/sdvps-materials	(cached)
+ docker build . -t my-repo-docker:8082/hello-world:v9
#1 [internal] load .dockerignore
#1 transferring context: 2B done
#1 DONE 0.0s

#2 [internal] load build definition from Dockerfile
#2 transferring dockerfile: 350B done
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/alpine:latest
#3 DONE 0.0s

#4 [internal] load metadata for docker.io/library/golang:1.16
#4 DONE 3.7s

#5 [builder 1/4] FROM docker.io/library/golang:1.16@sha256:5f6a4662de3efc6d6bb812d02e9de3d8698eea16b8eb7281f03e6f3e8383018e
#5 DONE 0.0s

#6 [stage-1 1/3] FROM docker.io/library/alpine:latest
#6 DONE 0.0s

#7 [internal] load build context
#7 transferring context: 13.07kB 0.0s done
#7 DONE 0.0s

#8 [stage-1 2/3] RUN apk -U add ca-certificates
#8 CACHED

#9 [builder 4/4] RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix nocgo -o /app .
#9 CACHED

#10 [builder 3/4] COPY . ./
#10 CACHED

#11 [builder 2/4] WORKDIR /go/src/github.com/netology-code/sdvps-materials
#11 CACHED

#12 [stage-1 3/3] COPY --from=builder /app /app
#12 CACHED

#13 exporting to image
#13 exporting layers done
#13 writing image sha256:8e1cabd1e065aa08f0f5b9fb4d33f0f936f9a479e34e2e5c825c635db5e531cd done
#13 naming to my-repo-docker:8082/hello-world:v9 done
#13 DONE 0.0s
+ docker login my-repo-docker:8082 -u admin -p admin
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
WARNING! Your password will be stored unencrypted in /var/lib/jenkins/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
+ docker push my-repo-docker:8082/hello-world:v9
The push refers to repository [my-repo-docker:8082/hello-world]
fe160372a0f2: Preparing
ffe8d6dc65d7: Preparing
3e01818d79cd: Preparing
3e01818d79cd: Layer already exists
ffe8d6dc65d7: Layer already exists
fe160372a0f2: Layer already exists
v9: digest: sha256:3a8f1cf0daf7fade5cd5901e0e134d72486fcb1dcbccfcceb1c5dcbec0da3c91 size: 950
+ docker logout
Removing login credentials for https://index.docker.io/v1/
Finished: SUCCESS

```   


---

### Задание 2

**Что нужно сделать:**

1. Создайте новый проект pipeline.
2. Перепишите сборку из задания 1 на declarative в виде кода.

В качестве ответа пришлите скриншоты с настройками проекта и результатами выполнения сборки.


### Решение 2   

Код скрипта для pipeline   
![docker-images](https://github.com/vyacheslav-PA/netology/blob/c78edbd4cc1beb348ae691640bfc4004614061bf/sys-admin/automatization/CICD-1/img/img-script-pipeline.png)   


docker image загружен в локальный репозиторий   
![nexus-pipeline](https://github.com/vyacheslav-PA/netology/blob/c78edbd4cc1beb348ae691640bfc4004614061bf/sys-admin/automatization/CICD-1/img/img-nexus-pipeline-image.png)   

##### вывод консоли Jenkins, после удачной сборки   

```
Started by user admin

[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins
 in /var/lib/jenkins/workspace/pipeline1
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Git)
[Pipeline] git
The recommended git tool is: NONE
No credentials specified
 > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/pipeline1/.git # timeout=10
Fetching changes from the remote Git repository
 > git config remote.origin.url https://github.com/vyacheslav-PA/gojenkins.git # timeout=10
Fetching upstream changes from https://github.com/vyacheslav-PA/gojenkins.git
 > git --version # timeout=10
 > git --version # 'git version 2.43.0'
 > git fetch --tags --force --progress -- https://github.com/vyacheslav-PA/gojenkins.git +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git rev-parse refs/remotes/origin/main^{commit} # timeout=10
Checking out Revision 683c31a61b456e4cbe9488760179560d2675ee66 (refs/remotes/origin/main)
 > git config core.sparsecheckout # timeout=10
 > git checkout -f 683c31a61b456e4cbe9488760179560d2675ee66 # timeout=10
 > git branch -a -v --no-abbrev # timeout=10
 > git branch -D main # timeout=10
 > git checkout -b main 683c31a61b456e4cbe9488760179560d2675ee66 # timeout=10
Commit message: "rm files"
 > git rev-list --no-walk 683c31a61b456e4cbe9488760179560d2675ee66 # timeout=10
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Test)
[Pipeline] sh
+ go test .
ok  	github.com/netology-code/sdvps-materials	(cached)
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Build)
[Pipeline] sh
+ docker build . -t my-repo-docker:8082/hello-world-pipeline:v3
#1 [internal] load .dockerignore
#1 transferring context: 2B done
#1 DONE 0.0s

#2 [internal] load build definition from Dockerfile
#2 transferring dockerfile: 350B done
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/alpine:latest
#3 DONE 0.0s

#4 [internal] load metadata for docker.io/library/golang:1.16
#4 DONE 2.0s

#5 [builder 1/4] FROM docker.io/library/golang:1.16@sha256:5f6a4662de3efc6d6bb812d02e9de3d8698eea16b8eb7281f03e6f3e8383018e
#5 DONE 0.0s

#6 [stage-1 1/3] FROM docker.io/library/alpine:latest
#6 DONE 0.0s

#7 [internal] load build context
#7 transferring context: 101.96kB 0.0s done
#7 DONE 0.1s

#8 [builder 2/4] WORKDIR /go/src/github.com/netology-code/sdvps-materials
#8 CACHED

#9 [builder 3/4] COPY . ./
#9 DONE 0.1s

#10 [builder 4/4] RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix nocgo -o /app .
#10 DONE 1.6s

#11 [stage-1 2/3] RUN apk -U add ca-certificates
#11 CACHED

#12 [stage-1 3/3] COPY --from=builder /app /app
#12 CACHED

#13 exporting to image
#13 exporting layers done
#13 writing image sha256:8e1cabd1e065aa08f0f5b9fb4d33f0f936f9a479e34e2e5c825c635db5e531cd done
#13 naming to my-repo-docker:8082/hello-world-pipeline:v3 done
#13 DONE 0.0s
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Push)
[Pipeline] sh
+ docker login my-repo-docker:8082 -u admin -p admin
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
WARNING! Your password will be stored unencrypted in /var/lib/jenkins/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
+ docker push my-repo-docker:8082/hello-world-pipeline:v3
The push refers to repository [my-repo-docker:8082/hello-world-pipeline]
fe160372a0f2: Preparing
ffe8d6dc65d7: Preparing
3e01818d79cd: Preparing
ffe8d6dc65d7: Layer already exists
3e01818d79cd: Layer already exists
fe160372a0f2: Layer already exists
v3: digest: sha256:3a8f1cf0daf7fade5cd5901e0e134d72486fcb1dcbccfcceb1c5dcbec0da3c91 size: 950
+ docker logout
Removing login credentials for https://index.docker.io/v1/
[Pipeline] }
[Pipeline] // stage
[Pipeline] }
[Pipeline] // node
[Pipeline] End of Pipeline
Finished: SUCCESS


```   

---

### Задание 3

**Что нужно сделать:**

1. Установите на машину Nexus.
1. Создайте raw-hosted репозиторий.
1. Измените pipeline так, чтобы вместо Docker-образа собирался бинарный go-файл. Команду можно скопировать из Dockerfile.
1. Загрузите файл в репозиторий с помощью jenkins.

В качестве ответа пришлите скриншоты с настройками проекта и результатами выполнения сборки.

### Решение 3  

Скрипт компиляции и зарузки в репозиторий bin файла   
![nexus-pipeline](https://github.com/vyacheslav-PA/netology/blob/79fbe1dfb427b1d19806e1d807dc4c5ccbdbdbc6/sys-admin/automatization/CICD-1/img/img-script-pipeline-raw.png)

Файл загружен в репозиторий   
![nexus-pipeline-raw-hosted](https://github.com/vyacheslav-PA/netology/blob/79fbe1dfb427b1d19806e1d807dc4c5ccbdbdbc6/sys-admin/automatization/CICD-1/img/img-nexus-build-go.png)   

Вывод консоли после завершения выполнения pipeline   

```

Started by user admin
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/lib/jenkins/workspace/raw-hosted
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Git)
[Pipeline] git
The recommended git tool is: NONE
No credentials specified
Cloning the remote Git repository
Cloning repository https://github.com/vyacheslav-PA/gojenkins.git
 > git init /var/lib/jenkins/workspace/raw-hosted # timeout=10
Fetching upstream changes from https://github.com/vyacheslav-PA/gojenkins.git
 > git --version # timeout=10
 > git --version # 'git version 2.43.0'
 > git fetch --tags --force --progress -- https://github.com/vyacheslav-PA/gojenkins.git +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git config remote.origin.url https://github.com/vyacheslav-PA/gojenkins.git # timeout=10
 > git config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/* # timeout=10
Avoid second fetch
 > git rev-parse refs/remotes/origin/main^{commit} # timeout=10
Checking out Revision 683c31a61b456e4cbe9488760179560d2675ee66 (refs/remotes/origin/main)
 > git config core.sparsecheckout # timeout=10
 > git checkout -f 683c31a61b456e4cbe9488760179560d2675ee66 # timeout=10
 > git branch -a -v --no-abbrev # timeout=10
 > git checkout -b main 683c31a61b456e4cbe9488760179560d2675ee66 # timeout=10
Commit message: "rm files"
First time build. Skipping changelog.
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Test)
[Pipeline] sh
+ go test .
ok  	github.com/netology-code/sdvps-materials	0.001s
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Build)
[Pipeline] sh
+ go build -o main:v1 main.go
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Push)
[Pipeline] sh
+ curl -u admin:admin http://10.43.122.151:8081/repository/raw-hosted/ --upload-file main:v1 -v
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying 10.43.122.151:8081...
* Connected to 10.43.122.151 (10.43.122.151) port 8081
* Server auth using Basic with user 'admin'
> PUT /repository/raw-hosted/main%3av1 HTTP/1.1
> Host: 10.43.122.151:8081
> Authorization: Basic YWRtaW46YWRtaW4=
> User-Agent: curl/8.5.0
> Accept: */*
> Content-Length: 2011538
> Expect: 100-continue
> 
< HTTP/1.1 100 Continue
} [65536 bytes data]
* We are completely uploaded and fine
< HTTP/1.1 201 Created
< Date: Fri, 03 Jan 2025 15:56:09 GMT
< Server: Nexus/3.75.1-01 (OSS)
< X-Content-Type-Options: nosniff
< Content-Security-Policy: sandbox allow-forms allow-modals allow-popups allow-presentation allow-scripts allow-top-navigation
< X-XSS-Protection: 1; mode=block
< Content-Length: 0
< 

100 1964k    0     0  100 1964k      0  58.5M --:--:-- --:--:-- --:--:-- 59.9M
* Connection #0 to host 10.43.122.151 left intact
[Pipeline] }
[Pipeline] // stage
[Pipeline] }
[Pipeline] // node
[Pipeline] End of Pipeline
Finished: SUCCESS

```

---

## Дополнительные задания* (со звёздочкой)

Их выполнение необязательное и не влияет на получение зачёта по домашнему заданию. Можете их решить, если хотите лучше разобраться в материале.

---

### Задание 4*

Придумайте способ версионировать приложение, чтобы каждый следующий запуск сборки присваивал имени файла новую версию. Таким образом, в репозитории Nexus будет храниться история релизов.

Подсказка: используйте переменную BUILD_NUMBER.

В качестве ответа пришлите скриншоты с настройками проекта и результатами выполнения сборки.