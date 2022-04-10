import sqlite3

con = sqlite3.connect("Crime_Management.db")

con.execute("CREATE TABLE Ulogin_table3(name varchar(255) primary key,address varchar(255) ,email Varchar(255),phone bigint ,password varchar(255) not null)")
# con.execute("CREATE TABLE crime_report1(description varchar(255),remark varchar(255) ,Report_Date date ,name varchar(255) primary key)")
con.close()