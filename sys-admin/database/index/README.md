# Домашнее задание к занятию «Индексы» - Перков Вячеслав

### Задание 1

Напишите запрос к учебной базе данных, который вернёт процентное отношение общего размера всех индексов к общему размеру всех таблиц.

### Решение 1

Процентное соотношение объема данных к объему индексов:

```
SELECT ((SUM(index_length)/ sum(data_length))*100) as '%'
	FROM INFORMATION_SCHEMA.TABLES
WHERE table_schema = 'sakila';
```

![percent](https://github.com/vyacheslav-PA/netology/blob/1c722c9e23168b19f73f6e8926061f90e305c326/sys-admin/database/index/img/img-t1-percent-1.png)

---

### Задание 2

Выполните explain analyze следующего запроса:
```sql
select distinct concat(c.last_name, ' ', c.first_name), sum(p.amount) over (partition by c.customer_id, f.title)
from payment p, rental r, customer c, inventory i, film f
where date(p.payment_date) = '2005-07-30' and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id
```
- перечислите узкие места;
- оптимизируйте запрос: внесите корректировки по использованию операторов, при необходимости добавьте индексы.


### Решение 2

Получение строк запроса занимает около 3000 мс.

```sql
EXPLAIN analyze
select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount) over (partition by c.customer_id, f.title)
	FROM payment p, rental r, customer c, inventory i, film f
where date(p.payment_date) = '2005-07-30' and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id	

-- время выполнения запроса 2928 мс
-> Table scan on <temporary>  (cost=2.5..2.5 rows=0) (actual time=2928..2928 rows=391 loops=1)
    -> Temporary table with deduplication  (cost=0..0 rows=0) (actual time=2928..2928 rows=391 loops=1)
        -> Window aggregate with buffering: sum(p.amount) OVER (PARTITION BY c.customer_id,f.title )   (actual time=1312..2836 rows=642000 loops=1)
            -> Sort: c.customer_id, f.title  (actual time=1312..1340 rows=642000 loops=1)
                -> Stream results  (cost=10.6e+6 rows=16.7e+6) (actual time=1.17..980 rows=642000 loops=1)
                    -> Nested loop inner join  (cost=10.6e+6 rows=16.7e+6) (actual time=1.16..859 rows=642000 loops=1)
                        -> Nested loop inner join  (cost=8.98e+6 rows=16.7e+6) (actual time=1.15..761 rows=642000 loops=1)
                            -> Nested loop inner join  (cost=7.3e+6 rows=16.7e+6) (actual time=1.14..662 rows=642000 loops=1)
                                -> Inner hash join (no condition)  (cost=1.61e+6 rows=16.1e+6) (actual time=1.11..20.4 rows=634000 loops=1)
                                    -> Filter: (cast(p.payment_date as date) = '2005-07-30')  (cost=1.68 rows=16086) (actual time=0.498..3 rows=634 loops=1)
                                        -> Table scan on p  (cost=1.68 rows=16086) (actual time=0.48..2.31 rows=16044 loops=1)
                                    -> Hash
                                        -> Covering index scan on f using idx_title  (cost=103 rows=1000) (actual time=0.0547..0.453 rows=1000 loops=1)
                                -> Covering index lookup on r using rental_date (rental_date = p.payment_date)  (cost=0.25 rows=1.04) (actual time=719e-6..938e-6 rows=1.01 loops=634000)
                            -> Single-row index lookup on c using PRIMARY (customer_id = r.customer_id)  (cost=250e-6 rows=1) (actual time=68.8e-6..81.9e-6 rows=1 loops=642000)
                        -> Single-row covering index lookup on i using PRIMARY (inventory_id = r.inventory_id)  (cost=250e-6 rows=1) (actual time=66.4e-6..79.5e-6 rows=1 loops=642000)

```
Таблица film в формировани запроса не учавстует,удаляем ее из запроса и время получения выборки находится в диапазоне 3-15 мс.


```sql
EXPLAIN analyze
select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount) over (partition by c.customer_id)
	FROM payment p, rental r, customer c, inventory i
where date(p.payment_date) = '2005-07-30' and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id	

-> Table scan on <temporary>  (cost=2.5..2.5 rows=0) (actual time=8.09..8.12 rows=391 loops=1)
    -> Temporary table with deduplication  (cost=0..0 rows=0) (actual time=8.09..8.09 rows=391 loops=1)
        -> Window aggregate with buffering: sum(p.amount) OVER (PARTITION BY c.customer_id )   (actual time=7.37..7.95 rows=642 loops=1)
            -> Sort: c.customer_id  (actual time=7.35..7.38 rows=642 loops=1)
                -> Stream results  (cost=19017 rows=16702) (actual time=0.428..7.23 rows=642 loops=1)
                    -> Nested loop inner join  (cost=19017 rows=16702) (actual time=0.421..7.03 rows=642 loops=1)
                        -> Nested loop inner join  (cost=13171 rows=16702) (actual time=0.414..6.12 rows=642 loops=1)
                            -> Nested loop inner join  (cost=7325 rows=16702) (actual time=0.404..5.47 rows=642 loops=1)
                                -> Filter: (cast(p.payment_date as date) = '2005-07-30')  (cost=1633 rows=16086) (actual time=0.385..4.27 rows=634 loops=1)
                                    -> Table scan on p  (cost=1633 rows=16086) (actual time=0.37..3.25 rows=16044 loops=1)
                                -> Covering index lookup on r using rental_date (rental_date = p.payment_date)  (cost=0.25 rows=1.04) (actual time=0.00137..0.00176 rows=1.01 loops=634)
                            -> Single-row index lookup on c using PRIMARY (customer_id = r.customer_id)  (cost=0.25 rows=1) (actual time=853e-6..877e-6 rows=1 loops=642)
                        -> Single-row covering index lookup on i using PRIMARY (inventory_id = r.inventory_id)  (cost=0.25 rows=1) (actual time=0.00126..0.00128 rows=1 loops=642)

```

Если вместо оконной функции применить объединение таблиц время получения выборки будет колебаться примерно в тех же значениях - около 3-15 мс.
Точно определить какой вариант запроса работает быстрее не представляется возможным, для этого необходимо олучить больше статистических данных.


```sql 
EXPLAIN analyze
select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount)
	FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
JOIN payment p ON r.rental_date = p.payment_date  
where date(p.payment_date) = date('2005-07-30')
GROUP BY c.customer_id

-> Sort with duplicate removal: `name`, `sum(p.amount)`  (actual time=4.49..4.5 rows=391 loops=1)
    -> Table scan on <temporary>  (actual time=4.34..4.37 rows=391 loops=1)
        -> Aggregate using temporary table  (actual time=4.34..4.34 rows=391 loops=1)
            -> Nested loop inner join  (cost=13171 rows=16702) (actual time=0.181..4.09 rows=642 loops=1)
                -> Nested loop inner join  (cost=7325 rows=16702) (actual time=0.175..3.64 rows=642 loops=1)
                    -> Filter: (cast(p.payment_date as date) = DATE'2005-07-30')  (cost=1633 rows=16086) (actual time=0.166..2.81 rows=634 loops=1)
                        -> Table scan on p  (cost=1633 rows=16086) (actual time=0.159..2.14 rows=16044 loops=1)
                    -> Covering index lookup on r using rental_date (rental_date = p.payment_date)  (cost=0.25 rows=1.04) (actual time=918e-6..0.00122 rows=1.01 loops=634)
                -> Single-row index lookup on c using PRIMARY (customer_id = r.customer_id)  (cost=0.25 rows=1) (actual time=601e-6..615e-6 rows=1 loops=642)

```
Для сбора статистики используем python:
На выполнение 10000 запросов с использованием оконной функции затрачено 54.4 секунды, среднее время выполнения запроса составляет - 5.4 микросекунд.
На аналогичную операцию с использованием inner join потребуется 42.4 секунды, среднее время - 4.2 микросекунд, исходя из чего можно сделать вывод о том что inner join работает быстрее оконнной функции в рамках рассматриваемой задачи.

Для дальнейшей оптимизации запроса проиндексируем столбец, содержащий дату по которому происходит агрегация:

```sql

EXPLAIN analyze
select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount) over (partition by c.customer_id)
	FROM payment p, rental r, customer c, inventory i
where p.payment_date >= '2005-07-30' and p.payment_date < DATE_ADD('2005-07-30', INTERVAL 1 DAY)  and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id	

-> Table scan on <temporary>  (cost=2.5..2.5 rows=0) (actual time=7.36..7.39 rows=391 loops=1)
    -> Temporary table with deduplication  (cost=0..0 rows=0) (actual time=7.36..7.36 rows=391 loops=1)
        -> Window aggregate with buffering: sum(p.amount) OVER (PARTITION BY c.customer_id )   (actual time=6.41..7.18 rows=642 loops=1)
            -> Sort: c.customer_id  (actual time=6.39..6.44 rows=642 loops=1)
                -> Stream results  (cost=798 rows=645) (actual time=0.125..6.14 rows=642 loops=1)
                    -> Nested loop inner join  (cost=798 rows=645) (actual time=0.12..5.66 rows=642 loops=1)
                        -> Nested loop inner join  (cost=575 rows=645) (actual time=0.113..4.41 rows=642 loops=1)
                            -> Nested loop inner join  (cost=349 rows=634) (actual time=0.0998..1.96 rows=634 loops=1)
                                -> Filter: ((r.rental_date >= TIMESTAMP'2005-07-30 00:00:00') and (r.rental_date < <cache>(('2005-07-30' + interval 1 day))))  (cost=127 rows=634) (actual time=0.0882..0.623 rows=634 loops=1)
                                    -> Covering index range scan on r using rental_date over ('2005-07-30 00:00:00' <= rental_date < '2005-07-31 00:00:00')  (cost=127 rows=634) (actual time=0.0861..0.302 rows=634 loops=1)
                                -> Single-row index lookup on c using PRIMARY (customer_id = r.customer_id)  (cost=0.25 rows=1) (actual time=0.00192..0.00194 rows=1 loops=634)
                            -> Index lookup on p using index_date (payment_date = r.rental_date)  (cost=0.254 rows=1.02) (actual time=0.00306..0.00368 rows=1.01 loops=634)
                        -> Single-row covering index lookup on i using PRIMARY (inventory_id = r.inventory_id)  (cost=0.246 rows=1) (actual time=0.00172..0.00174 rows=1 loops=642)
                   
```
При использовании индекса на 10000 запросов с оконной функции затрачено 35.9 секунд, среднее время - 3.5 микросекунд
Для запроса с использование join время выполнения 10000 запросов составляет 25.9 секунд, среднее значение 2.3 микросекунд


| Запрос| Время выполнения 10000 запросов, секунд | Среднее врямя одного запроса, микросекунд |
|------------------|-----------------------|--------------------------------------------------|
| Оконная функция, без индексирования      |   54.4   | 5.4 |
| inner join, без индексирования           |    42.4 | 4.2  |
| Оконная функция, c индексированием даты  | 35.9 | 3.5 |
| Оконная функция, c индексированием даты  | 25.9 | 2.3 |

Исходя из полученных результатов можно сделать вывод что использование индексирования в занчительной степени повышает скорость выборки дынных из таблицы.

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### Задание 3*

Самостоятельно изучите, какие типы индексов используются в PostgreSQL. Перечислите те индексы, которые используются в PostgreSQL, а в MySQL — нет.

*Приведите ответ в свободной форме.*