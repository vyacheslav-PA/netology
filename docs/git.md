https://git-scm.com/book/ru/v2/Инструменты-Git-Продвинутое-слияние   

---  
### Команды   
- git clone - скачать репозиторий
- git remote update, git fetch, 
- git pull - скачать изменения из репозитория
- git pull - подтянуть изменения
- git push - отпрвить изменения на сервер
- git init - инициализировать репозиторий
- git merge - слить ветки
- git status - просмотр текущего статуса
- git add - добавить файлы
- git restore --staged  file - убрать из индекса
- git log - посмотреть историю
    - --oneline - корткий вывод
- git diff - посмотреть изменения
- git show - выводит информацию об одном коммите
- git commit - внести изменения 
    - -m - комментарий
    - -a - заменяет add .
- git push - залить изменения на сервер
- git reset [hard, soft,..] (hash) - откатить изменения на указанный коммит
    - --soft откатить на укзанный коммит, с сохранением кода
    - --hard - откатить на указанный коммит, при этом все изменения удаляться без возможности восстановления
- git revert (hash) - откатиться на укзанный коммит, делает новый коммит на основе указанного коммита
    - -git reset HEAD~1 - откат на одну ветку
    - git revert HEAD~2  - создание нового коммита на основе указанного номера отката
- git branch  - работа с ветками
    - -v - отобразить ветки
    - git branch dev - создать ветку dev
- git checkout dev - перейти на ветку dev
    - -b создать и перейти на созданную ветку
- git merge (source) - слияние веток
- git checkout (hash) - переход к работе с указанным коммитом
- git switch -c newbranch - создать новую ветку на основе текущегго состояния