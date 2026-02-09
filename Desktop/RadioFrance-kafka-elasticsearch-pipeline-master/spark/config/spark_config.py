from pyspark.sql import SparkSession
from pyspark import SparkConf

def create_spark_session(app_name="RadioFranceAnalytics", master="spark://spark-master:7077"):
    """
    Crée et configure une session Spark avec Elasticsearch
    """
    conf = SparkConf() \
        .setAppName(app_name) \
        .setMaster(master) \
        .set("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:8.12.0") \
        .set("spark.es.nodes", "elasticsearch") \
        .set("spark.es.port", "9200") \
        .set("spark.es.nodes.wan.only", "true") \
        .set("spark.sql.shuffle.partitions", "2") \
        .set("spark.driver.memory", "1g") \
        .set("spark.executor.memory", "1g")
    
    spark = SparkSession.builder \
        .config(conf=conf) \
        .getOrCreate()
    
    return spark