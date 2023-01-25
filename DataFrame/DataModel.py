import sqlite3
import pandas as pd
from tabulate import tabulate
from DataFrame.SqliteHelper import SQL

"""
        DATA MODEL CLASS 
        ----------------
        
        
bu class tablodan çektiğimiz verilerin nasıl görünmesi, ne şekilde görünmesi, ne sırayla görünmesi gerektiğini belirler.
    
    showData():
        bu fonksiyon, tabloya tabulate modülü aracılığıyla şekil verir ve verileri ekler.


"""
class Data:
    def __init__(self):
        self.sql = SQL()
        self.conn = sqlite3.connect("HabitTracker.db") # database connection

        # kolon isimlerini ve içerisine gelecek değerleri key value şeklinde bir dictionary e ekliyorum
        self.data = {'Description': [], 'Daily/Weekly': [],
                     'Date Started': [], 'Streak (Days)': [],
                     'Streak (Weeks)': [], 'Record': [],'Last Updated':[]}

        # burada habit tablosundan çektiğimiz verileri satır isimleri habit'ler olacak şekilde ayarladık
        self.df = pd.read_sql_query("SELECT * FROM habits", self.conn, index_col="habit")
        # burası sql tablosundan çektiğimiz kolon isimlerini self. data değişkenindeki kolon isimleri yapmak için
        #--bu kodu yazdım.
        self.df = self.df.rename(
            columns={'desc': 'Description', 'week_or_daily': 'Daily/Weekly', 'date': 'Date Started',
                     'streak_days': 'Streak (Days)',
                     'streak_weeks': 'Streak (Weeks)', 'record': 'Record','last_updated':'Last Updated'})

        #çektiğimiz verileri tablodaki kolonlara yazıyoruz
        self.data['Description'] = self.df['Description'].tolist()
        self.data['Daily/Weekly'] = self.df['Daily/Weekly'].tolist()
        self.data['Date Started'] = self.df['Date Started'].tolist()
        self.data['Streak (Days)'] = self.df['Streak (Days)'].tolist()
        self.data['Streak (Weeks)'] = self.df['Streak (Weeks)'].tolist()
        self.data['Record'] = self.df['Record'].tolist()
        self.data['Last Updated']=self.df['Last Updated'].tolist()
    #TABLONUN ŞEKLİNİ BELİRLEYELİM
    def showData(self):
        print(tabulate(self.df, tablefmt="rounded_grid", headers="keys"))
