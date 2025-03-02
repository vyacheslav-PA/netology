import mysql.connector
from mysql.connector import Error
import datetime

def create_connection(host_name, user_name, user_password, db_name): # подключение к БД mySql
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_read_query(connection, query): # обращение к БД
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

connection = create_connection("172.19.0.2", "sys_temp","password", "sakila")
select = "EXPLAIN analyze "\
"select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount) over (partition by c.customer_id, f.title)" \
"	FROM payment p, rental r, customer c, inventory i, film f " \
"where date(p.payment_date) = '2005-07-30' and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id	"

select2 = "EXPLAIN analyze "\
"select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount) over (partition by c.customer_id) "\
"	FROM payment p, rental r, customer c, inventory i "\
"where date(p.payment_date) = '2005-07-30' and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id	"

join = "EXPLAIN analyze "\
"select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount) "\
"	FROM customer c "\
"JOIN rental r ON c.customer_id = r.customer_id "\
"JOIN payment p ON r.rental_date = p.payment_date  "\
"where date(p.payment_date) = date('2005-07-30') "\
"GROUP BY c.customer_id"

select2_index_date = "EXPLAIN analyze "\
"select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount) over (partition by c.customer_id) "\
"	FROM payment p, rental r, customer c, inventory i "\
"where p.payment_date >= '2005-07-30' and p.payment_date < DATE_ADD('2005-07-30', INTERVAL 1 DAY) "\
"and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id	"

join_index_date = "EXPLAIN analyze "\
"select distinct concat(c.last_name, ' ', c.first_name) as name, sum(p.amount) "\
"	FROM customer c "\
"JOIN rental r ON c.customer_id = r.customer_id "\
"JOIN payment p ON r.rental_date = p.payment_date  "\
"where p.payment_date >= '2005-07-30' and p.payment_date < DATE_ADD('2005-07-30', INTERVAL 1 DAY) "\
"GROUP BY c.customer_id"

def repeat_select(r,connection,select): # подсчет времени выполнения запросов
    init_time = datetime.datetime.now()
    for i in range(r):
        query = execute_read_query(connection, select)
        # for s in query:
        #     print(s)
    end_time = datetime.datetime.now()
    exec_time =  end_time - init_time
    return exec_time

s=10000
# подсчет времени без индексов
# over=repeat_select(s,connection,select2)
# join=repeat_select(s,connection,join)
# print("over - ",over, "average - " , over/s)
# print("join - ",join, "average - " , join/s)

# подсчет времени с индексами

over_index=repeat_select(s,connection,select2_index_date)
join_index=repeat_select(s,connection,join_index_date)
print("over + index- ",over_index, "average - " , over_index/s)
print("join + index - ",join_index, "average - " , join_index/s)