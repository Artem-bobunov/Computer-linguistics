from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import IDF
from pyspark.ml.feature import Word2Vec

spark = SparkSession\
    .builder\
    .appName("SimpleApplication")\
    .getOrCreate()


    # Построчная загрузка файла в RDD

    input_file = spark.sparkContext.textFile('/home/vagrant/spark_app/Samples/1.txt') #передача файлф
    print(input_file.collect()) #вывод коллекции
    prepared = input_file.map(lambda x: ([x]))      #преобразование rdd(замена на списки из одного элемента)
    df = prepared.toDF()                            #
    prepared_df = df.selectExpr('_1 as text')       #замена имени столбца _1 на text

    # Разбить на токены
    tokenizer = Tokenizer(inputCol='text', outputCol='words')
    words = tokenizer.transform(prepared_df)

    # Удалить стоп-слова
    stop_words = StopWordsRemover.loadDefaultStopWords('russian')                               #подгрузка русских слов
    remover = StopWordsRemover(inputCol='words',outputCol='filtered', stopWords=stop_words)     #удаление слов
    filtered = remover.transform(words)                                                         #внесение слов в таблицу
   
    # Вывести стоп-слова для русского языка
    print(stop_words)

    # Вывести таблицу filtered
    filtered.show()

    # Вывести столбец таблицы words с токенами до удаления стопслов
    words.select('words').show(truncate=False, vertical=True)
    
    # Вывести столбец "filtered" таблицы filtered с токенами после удаления стоп-слов
    filtered.select('filtered').show(truncate=False, vertical=True)
    
    # Посчитать значения TF
    vectorizer = CountVectorizer(inputCol='filtered',outputCol='raw_features').fit(filtered)
                #В fit() передается таблица, частоту встречаемости термов которой необходимо найти.
    featurized_data = vectorizer.transform(filtered)
    featurized_data.cache()
    vocabulary = vectorizer.vocabulary          #получение списка термов
    
    # Вывести таблицу со значениями частоты встречаемости термов.
    featurized_data.show()
    
    # Вывести столбец "raw_features" таблицы featurized_data
    featurized_data.select('raw_features').show(truncate=False,vertical=True)
    
    # Вывести список термов в словаре
    print(vocabulary)
    
    # Посчитать значения DF
    idf = IDF(inputCol='raw_features', outputCol='features')
    idf_model = idf.fit(featurized_data)
    rescaled_data = idf_model.transform(featurized_data)
    
    # Вывести таблицу rescaled_data
    rescaled_data.show()

    # Вывести столбец "features" таблицы featurized_data
    rescaled_data.select('features').show(truncate=False,vertical=True)
    
    # Построить модель Word2Vec
    word2Vec = Word2Vec(vectorSize=3, minCount=0, inputCol='words',outputCol='result')
    model = word2Vec.fit(words)
    w2v_df = model.transform(words)
    w2v_df.show()
spark.stop()
