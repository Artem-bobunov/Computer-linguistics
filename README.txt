Установка Python
sudo apt-get update 
sudo apt-get install python 3.7
sudo apt install python3-pip 

Установка  java
sudo apt install openjdk-8-jdk 

Установка  pyspark
sudo pip3 –no-cache-dir install pyspark
mkdir spark245 
cd spark245 
wget http://apache-mirror.rbc.ru/pub/apache/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz
sudo tar -zxvf spark-2.4.5-bin-hadoop2.7.tgz

Установим значения переменных среды
sudo nano /etc/environment 

Добавить новую строку
JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64" 

Сохраним
source /etc/environment 

Установка  pyspark на python
sudo nano .bashrc 

В конце файла написать:
source /etc/environment 
export PYSPARK_PYTHON=/usr/bin/python3 
export PYSPARK_DRIVER_PYTHON=python3 
export SPARK_HOME="/home/vagrant/spark245/spark-2.4.5-binhadoop2.7" export PATH="$SPARK_HOME/bin:$PATH" 

Проверка
source ~/.bashrc 
pyspark 

Выполнение файла...