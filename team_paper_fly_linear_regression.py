# -*- coding: utf-8 -*-
"""TEAM PAPER-FLY LINEAR REGRESSION.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14XdDB1m5iIWFG0U3wyyILG4t8qhZAiok
"""

!apt-get update
!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q http://archive.apache.org/dist/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz
!tar xf spark-3.1.1-bin-hadoop3.2.tgz
!pip install -q findspark

import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.1.1-bin-hadoop3.2"

import findspark
findspark.init()

from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[1]").appName("RDD").getOrCreate()
spark

from pyspark.ml.regression import LinearRegression
df = spark.read.csv("/content/heart.csv", inferSchema=True, header =True)
df.show(6)

print(df.count(), len(df.columns))

df.printSchema()

from pyspark.sql.functions import corr
df.select(corr('age', 'target')).show

from pyspark.ml.feature import VectorAssembler
vec_assembler= VectorAssembler(inputCols= ['sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang','oldpeak','slope','ca','thal'], outputCol="features")
features_df = vec_assembler.transform(df)

features_df.show(5)

features_df.select("features").show(5, truncate= False)
model_df= features_df.select("features", "age")
model_df.show(5)

train_df, test_df = model_df.randomSplit([0.8, 0.2])
print(train_df.count())
print(test_df.count())

train_df.describe().show()

lin_reg = LinearRegression(labelCol= 'age')
lin1 = lin_reg.fit(train_df)
lin1.intercept
print(lin1.coefficients)

train_pred =lin1.evaluate(train_df)
train_pred.meanSquaredError

test_rest = lin1.evaluate(test_df)
test_rest.meanSquaredError