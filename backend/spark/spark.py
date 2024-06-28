from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType

schema = StructType([
    StructField("Time", StringType(), True),
    StructField("V1", FloatType(), True),
    StructField("V2", FloatType(), True),
    StructField("V3", FloatType(), True),
    StructField("V4", FloatType(), True),
    StructField("V5", FloatType(), True),
    StructField("V6", FloatType(), True),
    StructField("V7", FloatType(), True),
    StructField("V8", FloatType(), True),
    StructField("V9", FloatType(), True),
    StructField("V10", FloatType(), True),
    StructField("V11", FloatType(), True),
    StructField("V12", FloatType(), True),
    StructField("V13", FloatType(), True),
    StructField("V14", FloatType(), True),
    StructField("V15", FloatType(), True),
    StructField("V16", FloatType(), True),
    StructField("V17", FloatType(), True),
    StructField("V18", FloatType(), True),
    StructField("V19", FloatType(), True),
    StructField("V20", FloatType(), True),
    StructField("V21", FloatType(), True),
    StructField("V22", FloatType(), True),
    StructField("V23", FloatType(), True),
    StructField("V24", FloatType(), True),
    StructField("V25", FloatType(), True),
    StructField("V26", FloatType(), True),
    StructField("V27", FloatType(), True),
    StructField("V28", FloatType(), True),
    StructField("Amount", FloatType(), True),
    StructField("Class", IntegerType(), True)
])

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'transaction_topic')

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("SparkProcessor") \
    .getOrCreate()

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .load()

# Convert the value column from bytes to string
df = df.selectExpr("CAST(value AS STRING) as json_str")

# Parse the JSON data and convert to DataFrame
df = df.withColumn("data", from_json(col("json_str"), schema)).select("data.*")

query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
