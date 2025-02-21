import producer
def pr(s,ip):
    for i in range(0,s):
        producer.producer(i,ip)
        print (i)
# pr(200,'192.168.1.107')
pr(200,'192.168.1.102')
