# Домашнее задание к занятию «SQL. Часть 2» - Перков Вячеслав

---

Задание можно выполнить как в любом IDE, так и в командной строке.

### Задание 1

Одним запросом получите информацию о магазине, в котором обслуживается более 300 покупателей, и выведите в результат следующую информацию: 
- фамилия и имя сотрудника из этого магазина;
- город нахождения магазина;
- количество пользователей, закреплённых в этом магазине.

### Решение 1

Получение информации о магазине > 300 покупателей:
```
SELECT s2.first_name, s2.last_name, c2.city,  COUNT(*)  as clients
	FROM store s 
JOIN customer c ON s.store_id = c.store_id 
JOIN staff s2 ON s2.store_id = c.store_id 
JOIN address a ON s2.address_id =a.address_id 
JOIN city c2 ON c2.city_id = a.city_id 
GROUP BY s.store_id, s2.last_name, s2.first_name, c2.city 
HAVING clients>300
```
![store>300clients](https://github.com/vyacheslav-PA/netology/blob/d39362217b022e86738e64317abbc821134788e4/sys-admin/database/sql2/img/img-t1-clients-1.png)

---

### Задание 2

Получите количество фильмов, продолжительность которых больше средней продолжительности всех фильмов.

### Решение 2

Получение количества фильмов выше средней продолжительности:

```
SELECT  COUNT(*)
	FROM film  
WHERE length >(SELECT AVG(length)
	FROM film)
```
![length](https://github.com/vyacheslav-PA/netology/blob/d39362217b022e86738e64317abbc821134788e4/sys-admin/database/sql2/img/img-t2-average-1.png)

---

### Задание 3

Получите информацию, за какой месяц была получена наибольшая сумма платежей, и добавьте информацию по количеству аренд за этот месяц.

### Решение 3

Месяц с максимальной суммой платежей:

```
SELECT SUM(amount) as summ, CONCAT(YEAR(r.rental_date ), " ", MONTH (r.rental_date)) as month , COUNT(r.rental_id) as rent
	FROM payment p 
JOIN rental r ON r.rental_id = p.payment_id 
GROUP BY month
ORDER BY summ DESC 
LIMIT 1;
```

![summ payment](https://github.com/vyacheslav-PA/netology/blob/d39362217b022e86738e64317abbc821134788e4/sys-admin/database/sql2/img/img-t3-max-summ-rent-1.png)

---

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### Задание 4*

Посчитайте количество продаж, выполненных каждым продавцом. Добавьте вычисляемую колонку «Премия». Если количество продаж превышает 8000, то значение в колонке будет «Да», иначе должно быть значение «Нет».

### Решение 4*

Подсчет премии, от количества продаж:

```
SELECT  s.first_name ,s.last_name , COUNT(*) as 'количество продаж', 
		CASE	
			WHEN COUNT(*) > 8000 THEN "да"
			WHEN COUNT(*) < 8000 THEN "нет"
		END AS "ПРЕМИЯ"
	FROM payment  p
JOIN staff s ON s.staff_id =p.staff_id 
GROUP BY p.staff_id 
```
![count pay](https://github.com/vyacheslav-PA/netology/blob/d39362217b022e86738e64317abbc821134788e4/sys-admin/database/sql2/img/img-t4-count-payment-1.png)

---

### Задание 5*

Найдите фильмы, которые ни разу не брали в аренду.

### Решение 5*

Фильмы, которые не брали в аренду:

```
SELECT f.title 
	FROM inventory i
LEFT JOIN rental r ON r.inventory_id = i.inventory_id 
JOIN film f ON f.film_id = i.film_id 
where r.rental_id IS NULL
```

![movies without rent](https://github.com/vyacheslav-PA/netology/blob/d39362217b022e86738e64317abbc821134788e4/sys-admin/database/sql2/img/img-t5-no-rent-1.png)