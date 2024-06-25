import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="mvoemel",
    password="mvoemel",
    auth_plugin="mysql_native_password"
    # database=""
)

mycursor = db.cursor()

#mycursor.execute("CREATE DATABASE testdatabase")
#mycursor.execute("DROP DATABASE testdatabase")
#mycursor.execute("SHOW DATABASES")

db.close()