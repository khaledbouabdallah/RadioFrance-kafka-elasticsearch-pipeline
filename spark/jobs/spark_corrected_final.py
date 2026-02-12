from pyspark.sql import SparkSession
from pyspark.sql import functions as F

print("=" * 60)
print("SPARK RADIO FRANCE - VERSION CORRIGEE")
print("=" * 60)

try:
    # 1. Create Spark session
    spark = SparkSession.builder \
        .appName("RadioFranceAnalytics") \
        .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:8.12.0") \
        .config("spark.es.nodes", "elasticsearch") \
        .config("spark.es.port", "9200") \
        .config("spark.es.nodes.wan.only", "true") \
        .getOrCreate()
    
    print("✅ Spark session created")
    
    # 2. Create test data
    test_data = [
        ("FRANCEINTER", "France Inter", 25, 3.2, 18),
        ("FRANCECULTURE", "France Culture", 15, 4.1, 12),
        ("FRANCEINFO", "France Info", 35, 2.8, 25),
        ("FRANCEMUSIQUE", "France Musique", 20, 3.5, 15),
        ("FIP", "FIP", 30, 2.5, 20),
    ]
    
    df = spark.createDataFrame(
        test_data,
        ["station_id", "station_brand", "total_broadcasts", "avg_themes", "podcast_count"]
    )
    
    # Add timestamp
    df_with_time = df.withColumn("@timestamp", F.current_timestamp())
    
    print("Test data created:")
    df_with_time.show()
    
    # 3. Save to Elasticsearch - CORRECTION: pas de "/stats"
    print("Saving to Elasticsearch...")
    try:
        # CHANGÉ: "radiofrance-analytics" (sans type)
        df_with_time.write \
            .format("org.elasticsearch.spark.sql") \
            .option("es.resource", "radiofrance-analytics") \
            .mode("overwrite") \
            .save()
        
        print("✅ Data saved to Elasticsearch")
        
        # Read back to verify
        df_read = spark.read \
            .format("org.elasticsearch.spark.sql") \
            .option("es.resource", "radiofrance-analytics") \
            .load()
        
        print(f"Verification: {df_read.count()} documents read")
        df_read.show()
        
    except Exception as e:
        print(f"⚠️ Elasticsearch error: {e}")
        print("Data available locally only")
    
    spark.stop()
    
    print("\n" + "=" * 60)
    print("✅ SPARK JOB COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    exit(1)