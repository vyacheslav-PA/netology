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

Если убрать в оконной функции аргумент 'f.title', который не несет полезнойй нагрузки, то скорость выполнения запроса увеличится на ~800 мс

```sql
EXPLAIN analyze
select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount) over (partition by c.customer_id)
	FROM payment p, rental r, customer c, inventory i, film f
where date(p.payment_date) = '2005-07-30' and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id	
--  время выполнения запроса 2258 мс
-> Table scan on <temporary>  (cost=2.5..2.5 rows=0) (actual time=2258..2258 rows=391 loops=1)
    -> Temporary table with deduplication  (cost=0..0 rows=0) (actual time=2258..2258 rows=391 loops=1)
        -> Window aggregate with buffering: sum(p.amount) OVER (PARTITION BY c.customer_id )   (actual time=1005..2181 rows=642000 loops=1)
            -> Sort: c.customer_id  (actual time=1003..1021 rows=642000 loops=1)
                -> Stream results  (cost=10.6e+6 rows=16.7e+6) (actual time=0.449..899 rows=642000 loops=1)
                    -> Nested loop inner join  (cost=10.6e+6 rows=16.7e+6) (actual time=0.444..816 rows=642000 loops=1)
                        -> Nested loop inner join  (cost=8.98e+6 rows=16.7e+6) (actual time=0.439..718 rows=642000 loops=1)
                            -> Nested loop inner join  (cost=7.3e+6 rows=16.7e+6) (actual time=0.432..619 rows=642000 loops=1)
                                -> Inner hash join (no condition)  (cost=1.61e+6 rows=16.1e+6) (actual time=0.419..14.6 rows=634000 loops=1)
                                    -> Filter: (cast(p.payment_date as date) = '2005-07-30')  (cost=1.63 rows=16086) (actual time=0.205..2.62 rows=634 loops=1)
                                        -> Table scan on p  (cost=1.63 rows=16086) (actual time=0.196..1.97 rows=16044 loops=1)
                                    -> Hash
                                        -> Covering index scan on f using idx_fk_language_id  (cost=103 rows=1000) (actual time=0.0977..0.159 rows=1000 loops=1)
                                -> Covering index lookup on r using rental_date (rental_date = p.payment_date)  (cost=0.25 rows=1.04) (actual time=668e-6..879e-6 rows=1.01 loops=634000)
                            -> Single-row index lookup on c using PRIMARY (customer_id = r.customer_id)  (cost=250e-6 rows=1) (actual time=66.1e-6..79.7e-6 rows=1 loops=642000)
                        -> Single-row covering index lookup on i using PRIMARY (inventory_id = r.inventory_id)  (cost=250e-6 rows=1) (actual time=64.4e-6..78e-6 rows=1 loops=642000)
```

В процессе оптимизации запроса необходимо убрать из выборки таблицы не учавствующие в построении результирующей таблицы, что дает прирост в скорости выполнения запроса кратно отличающийся от предыдущего результата на ~ 2200 мс

```sql
EXPLAIN analyze
select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount) over (partition by c.customer_id)
	FROM payment p, customer c
where date(p.payment_date) = '2005-07-30' and p.customer_id = c.customer_id 
-- время выполнения запроса 7.92 мс 
-> Table scan on <temporary>  (cost=2.5..2.5 rows=0) (actual time=7.92..7.94 rows=391 loops=1)
    -> Temporary table with deduplication  (cost=0..0 rows=0) (actual time=7.92..7.92 rows=391 loops=1)
        -> Window aggregate with buffering: sum(p.amount) OVER (PARTITION BY c.customer_id )   (actual time=7.28..7.81 rows=634 loops=1)
            -> Sort: c.customer_id  (actual time=7.26..7.28 rows=634 loops=1)
                -> Stream results  (cost=7263 rows=16086) (actual time=0.577..7.11 rows=634 loops=1)
                    -> Nested loop inner join  (cost=7263 rows=16086) (actual time=0.571..6.84 rows=634 loops=1)
                        -> Filter: (cast(p.payment_date as date) = '2005-07-30')  (cost=1633 rows=16086) (actual time=0.548..5.96 rows=634 loops=1)
                            -> Table scan on p  (cost=1633 rows=16086) (actual time=0.533..4.61 rows=16044 loops=1)
                        -> Single-row index lookup on c using PRIMARY (customer_id = p.customer_id)  (cost=0.25 rows=1) (actual time=0.00118..0.0012 rows=1 loops=634)
```

Если вместо оконной функции применить объединение таблиц время получения выборки увеличится на ~ 10 мс

```sql 
EXPLAIN analyze
select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount)
	FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
where date(p.payment_date) = date('2005-07-30')
GROUP BY p.customer_id
-- время выполнения запроса 17.6 мс 
-> Sort with duplicate removal: `name`, `sum(p.amount)`  (actual time=17.6..17.6 rows=391 loops=1)
    -> Table scan on <temporary>  (actual time=17.4..17.5 rows=391 loops=1)
        -> Aggregate using temporary table  (actual time=17.4..17.4 rows=391 loops=1)
            -> Nested loop inner join  (cost=5691 rows=16086) (actual time=0.136..17.1 rows=634 loops=1)
                -> Table scan on c  (cost=61.2 rows=599) (actual time=0.0342..0.17 rows=599 loops=1)
                -> Filter: (cast(p.payment_date as date) = DATE'2005-07-30')  (cost=6.72 rows=26.9) (actual time=0.0259..0.0282 rows=1.06 loops=599)
                    -> Index lookup on p using idx_fk_customer_id (customer_id = c.customer_id)  (cost=6.72 rows=26.9) (actual time=0.0235..0.0267 rows=26.8 loops=599)
```


## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### Задание 3*

Самостоятельно изучите, какие типы индексов используются в PostgreSQL. Перечислите те индексы, которые используются в PostgreSQL, а в MySQL — нет.

*Приведите ответ в свободной форме.*