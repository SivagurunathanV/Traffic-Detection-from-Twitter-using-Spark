import pyspark.sql as sql
from model_building import getModel, getSparkContext
from pyspark.sql import SQLContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from utilities import index_to_elasticsearch
import os
# # SUBMIT_ARGS = "--packages org.apache.spark:park-streaming-kafka-0-8-assembly_2.11:2.3.0-palantir.15-sources.jar pyspark-shell"
# SUBMIT_ARGS = "$ bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8:2.3.0 pyspark-shell"
# os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS


model, pipelineFit = getModel()


def formatData(jsonString):
    return jsonString[1].encode("ascii", "ignore")


def process(time, rdd):
    rdd = rdd.map(lambda r: str(r).decode("utf-8"))
    data = spark.read.json(rdd)
    if data.count() > 0:
        dataset = pipelineFit.transform(data)
        predictions = model.transform(dataset)
        predictions.show(10)
        predicted_traffic_data = predictions \
            .filter(predictions['prediction'] == 1.0)
        predicted_text = predicted_traffic_data.select(["text", "coordinates", "created_at"]).toJSON()
        elastic_data = predicted_text.map(lambda line: index_to_elasticsearch(line))
        elastic_data.count()


if __name__ == "__main__":
    sc = getSparkContext()
    spark = sql.SparkSession(sc)
    sqlContext = SQLContext(sc)
    ssc = StreamingContext(sc, 1)
    topic = 'trafficnyc'
    zkQuorum = 'localhost:2181'
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(formatData)
    lines.foreachRDD(process)
    ssc.start()
    ssc.awaitTermination()
