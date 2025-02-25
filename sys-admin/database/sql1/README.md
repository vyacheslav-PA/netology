# Домашнее задание к занятию «SQL. Часть 1» - Перков Вячеслав

---

Задание можно выполнить как в любом IDE, так и в командной строке.

### Задание 1

Получите уникальные названия районов из таблицы с адресами, которые начинаются на “K” и заканчиваются на “a” и не содержат пробелов.

### Решение 1
Получение уникальных названий районов:

```
SELECT DISTINCT district
    FROM address
WHERE LEFT(district,1) = 'K' AND  right(district,1) = "a" AND district NOT LIKE('% %');
```
![select district]()

---

### Задание 2

Получите из таблицы платежей за прокат фильмов информацию по платежам, которые выполнялись в промежуток с 15 июня 2005 года по 18 июня 2005 года **включительно** и стоимость которых превышает 10.00.

### Решение 2

Выбборка из временного интервала:

```
SELECT *
	FROM payment
WHERE amount >10   AND (CAST(payment_date AS DATE)) >= CAST('2005-06-15' AS DATE) AND (CAST(payment_date AS DATE)) <= CAST('2005-06-18' AS DATE);
```

![select payments]()

---

### Задание 3

Получите последние пять аренд фильмов.

### Решение 3

Выборка последних 5 аренд:

```
SELECT * 
	FROM rental
ORDER BY rental_date DESC
LIMIT 5;
```

![last 5 rental]()

---

### Задание 4

Одним запросом получите активных покупателей, имена которых Kelly или Willie. 

Сформируйте вывод в результат таким образом:
- все буквы в фамилии и имени из верхнего регистра переведите в нижний регистр,
- замените буквы 'll' в именах на 'pp'.

---

### Решение 4
Выборка покупетелей по именам и работа со строками:

```
SELECT REPLACE(LOWER(first_name),'ll','pp') as 'first name', LOWER(first_name) as 'first name'
	FROM customer c 
WHERE first_name IN ('Kelly','Willie')
```
![lower+replace]()

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### Задание 5*

Выведите Email каждого покупателя, разделив значение Email на две отдельных колонки: в первой колонке должно быть значение, указанное до @, во второй — значение, указанное после @.

### Решение 5*
Разделение адреса электронной почты:

```
SELECT email, LEFT(email,POSITION('@' IN email)-1) , RIGHT(email,(CHAR_LENGTH(email) - POSITION('@' IN email)))
	FROM customer
```

![split email]()

---

### Задание 6*
Доработайте запрос из предыдущего задания, скорректируйте значения в новых колонках: первая буква должна быть заглавной, остальные — строчными.


### Решение 6*
Разделение адреса и изменение регистра букв:
```
SELECT email, LEFT(CONCAT(UPPER(SUBSTR(email,1,1)), LOWER(SUBSTR(email,2,(LENGTH(email))))),POSITION('@' IN email)-1),
CONCAT(UPPER(LEFT(RIGHT(email,(CHAR_LENGTH(email) - POSITION('@' IN email))),1)),
LOWER(RIGHT(RIGHT(email,(CHAR_LENGTH(email) - POSITION('@' IN email))),(CHAR_LENGTH(email) - POSITION('@' IN email)-1))))
	FROM customer
```

![split email-2 ]()