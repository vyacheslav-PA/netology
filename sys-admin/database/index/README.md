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

#### Оригинальный запрос

```sql
EXPLAIN analyze
select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount) over (partition by c.customer_id, f.title)
	FROM payment p, rental r, customer c, inventory i, film f
where date(p.payment_date) = '2005-07-30' and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id	

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

#### Оптимизированный запрос - оконная функция заменена на объединение с группировкой, добавлен индекс на поле  `payment_date`  

```sql
EXPLAIN analyze
select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount)
	FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
JOIN payment p ON r.rental_date = p.payment_date  
where p.payment_date >= '2005-07-30' and p.payment_date < DATE_ADD('2005-07-30', INTERVAL 1 DAY)
GROUP BY c.customer_id
                        
-> Sort with duplicate removal: `name`, `sum(p.amount)`  (actual time=6.35..6.37 rows=391 loops=1)
    -> Table scan on <temporary>  (actual time=6.15..6.19 rows=391 loops=1)
        -> Aggregate using temporary table  (actual time=6.15..6.15 rows=391 loops=1)
            -> Nested loop inner join  (cost=575 rows=645) (actual time=0.0686..5.11 rows=642 loops=1)
                -> Nested loop inner join  (cost=349 rows=634) (actual time=0.0583..2.25 rows=634 loops=1)
                    -> Filter: ((r.rental_date >= TIMESTAMP'2005-07-30 00:00:00') and (r.rental_date < <cache>(('2005-07-30' + interval 1 day))))  (cost=127 rows=634) (actual time=0.0508..0.667 rows=634 loops=1)
                        -> Covering index range scan on r using rental_date over ('2005-07-30 00:00:00' <= rental_date < '2005-07-31 00:00:00')  (cost=127 rows=634) (actual time=0.0492..0.298 rows=634 loops=1)
                    -> Single-row index lookup on c using PRIMARY (customer_id = r.customer_id)  (cost=0.25 rows=1) (actual time=0.00226..0.00229 rows=1 loops=634)
                -> Index lookup on p using index_date (payment_date = r.rental_date)  (cost=0.254 rows=1.02) (actual time=0.0035..0.00418 rows=1.01 loops=634)
                   
```

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### Задание 3*

Самостоятельно изучите, какие типы индексов используются в PostgreSQL. Перечислите те индексы, которые используются в PostgreSQL, а в MySQL — нет.

*Приведите ответ в свободной форме.*