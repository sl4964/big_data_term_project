from __future__ import print_function
import sys
from operator import add
from pyspark import SparkContext
from csv import reader

'''Run using command spark-submit by_date_pickup_green.py'''

if __name__ == "__main__":
    sc = SparkContext()
    lines = sc.textFile('new_schema/green_*.csv,old_schema/green_*.csv')
    lines = lines.mapPartitions(lambda x: reader(x)).filter(lambda x: len(x) >= 1)

    counts = lines.filter(lambda x: x[1] != 'lpep_pickup_datetime').map(lambda x: (x[1][:-9],1)).reduceByKey(add).sortByKey(ascending=True).map(lambda x: str(x[0]) + '\t' + str(x[1]))

    counts.saveAsTextFile('by_date_pickup_green.out')

    sc.stop()