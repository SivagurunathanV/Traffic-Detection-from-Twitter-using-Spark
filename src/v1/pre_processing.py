from pyspark.ml.feature import Tokenizer, RegexTokenizer
from pyspark.sql.functions import col, udf
from pyspark.sql.types import IntegerType
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
from pyspark.mllib.util import MLUtils
from pyspark.ml.feature import HashingTF, IDF

sc = SparkContext('local')
spark = SparkSession(sc)
sentenceDataFrame = spark.createDataFrame([
    (0, "Hi I heard about Spark /fjhgj/ :p"),
    (1, "I wish Java could use case classes"),
    (2, "Logistic,regression,models,are,neat")
], ["id", "text"])
tokenizer = Tokenizer(inputCol="text", outputCol="words")
regexTokenizer = RegexTokenizer(inputCol="text", outputCol="words", pattern="\\W")
countTokens = udf(lambda words: len(words), IntegerType())
tokenized = tokenizer.transform(sentenceDataFrame)
tokenized_words=tokenized.select("words")
tokenized_words.show()
regexTokenized = regexTokenizer.transform(sentenceDataFrame)
regexTokenized.select("text", "words") \
    .withColumn("tokens", countTokens(col("words"))).show(truncate=False)
re_tokenized_words=regexTokenized.select("words")
remover = StopWordsRemover(inputCol="words", outputCol="filtered")
removed=remover.transform(re_tokenized_words)
cv = CountVectorizer(inputCol="words", outputCol="features", vocabSize=3, minDF=2.0)
model = cv.fit(removed)
result = model.transform(removed)
result.show(truncate=False)
features=result.select("features")

