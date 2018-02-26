# This is like path_code.py except we will track the follower that
# directly led to the user
# This will significantly expedite determining the explicit shortest path once
# figuring out how the path length from one user to another

from pyspark import SparkConf, SparkContext

def parse_edge(s):    
    user, follower = s.split("\t")
    return (int(user), int(follower))

def step(item):
    prev_v, prev_d, back_v, next_v = item[0], item[1][0][0], item[1][0][1], item[1][1]
    return (next_v, (prev_d + 1, prev_v))

def complete(item):
    v, old_pair, new_pair = item[0], item[1][0], item[1][1]

    if old_pair is not None:
        return (v, old_pair)
    return (v, new_pair)

sc = SparkContext(conf=SparkConf().setAppName("MyApp").setMaster("local"))

n = 400  # number of partitions
edges = sc.textFile("/data/twitter/twitter_sample.txt").map(parse_edge).cache()
forward_edges = edges.map(lambda e: (e[1], e[0])).partitionBy(n).persist()

x = 12 # initial user
y = 34 # end user
d = 0
prev_v = 0
distances = sc.parallelize([(x, (d, prev_v))]).partitionBy(n)
while True:
    outer =  distances.filter(lambda i:i[1][0]==d)
    candidates = outer.join(forward_edges, n).map(step)
    new_distances = distances.fullOuterJoin(candidates, n).map(complete, True).persist()
    count = new_distances.filter(lambda i:i[1][0]==d+1).count()
    count_y = new_distances.filter(lambda i:i[0] == y).count()
    d += 1
    distances = new_distances
    
    if count_y > 0:
        break

# Find the explicit path by capturing the previous vertex starting with the
# end vertex and looping backwards to the starting vertex
path = [y]
curr_user = y
while d > 1:
    curr_user_map = distances.filter(lambda i:i[0]==curr_user).take(1)
    prev_user = curr_user_map[0][1][1]
    path = [prev_user] + path
    curr_user = prev_user
    d = d - 1
path = [x] + path
print ','.join(map(str, path))
