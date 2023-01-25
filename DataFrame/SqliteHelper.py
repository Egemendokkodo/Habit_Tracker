import sqlite3 as sql

"""

    SQL CLASS
    ---------
bu classta tabloya ekleme, çıkarma, silme işlemleri
ve ayrıca weekly ve daily işlemlerini burada gerçekleştiririz:

    addTable():
        basit olarak, eğer kullanıcı habit eklemek isterse bu fonksiyon çağırılır.
        tabloya kullanıcının girdiği verileri ekler.
        
    deleteFromTable():
        kullanıcı tablodan habit silmek isterse bu fonksiyon çağırılır.
        
    addHabitStreak():
        buraya bir habit ismi gönderilir. 
        gönderilen habit ismi daily veya weekly bir frekansa sahip mi kontrol edilir.
        eğer daily ise son check off tarihinden sadece 1 gün geçmişse streak day e 1 eklenir
        eğer daily ise ve son check off tarihinden 1 günden fazla geçmişse streakler ve weekler sıfırlanır ama record sabit kalır.
        eğer streak day her 7 güne vurduğunda week kısmı 1 artar
        
        eğer weekly ise son check off tarihinden sadece 7 gün geçmişse streak day e 7 eklenir
        eğer weekly ise ve son check off tarihinden 7 günden fazla geçmişse streakler ve weekler sıfırlanır ama record sabit kalır.
        eğer week her arttığında streak days kısmı 7 artar
        
        
        findLongestHabit(self):
            returns the longest day streak of a habit.

        findAllDailyHabits(self):
            returns the all daily habits
        findNumberOfHabits(self):
            returns how many habits you have
        longestHabitStreak(self):
            returns longest habit streak by day 
        sumOfAllDays(self): 
            returns the sum of all days in column
        
        sumOfAllWeeks(self):
            returns the sum of all weeks in column


        printTable(self): (not necessary, just to make sure that table works)
        
        deleteTable(self): (not necessary, just to make sure that delete table works)




"""

class SQL:
    def __init__(self):
        self.conn = sql.connect("HabitTracker.db")
        self.cursor = self.conn.cursor()
        # eğer tablo yoksa sql tablosunu oluşturur CREATE TABLE IF NOT EXISTS
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS habits (habit TEXT,desc TEXT,
        week_or_daily TEXT,date TEXT,streak_days INTEGER,streak_weeks INTEGER,record INTEGER,last_updated TEXT)""")
        self.conn.commit()

    def addTable(self, habitName, habitDesc, weekOrDaily, date, streak=0, streak_weeks=0, record=0):
        self.cursor.execute(
            f"INSERT INTO habits (habit,desc,week_or_daily,date,streak_days,streak_weeks,record,last_updated) VALUES {habitName, habitDesc, weekOrDaily, date, streak, streak_weeks, record, date}")
        self.conn.commit()

    def deleteFromTable(self, habitName):

        self.cursor.execute(f"DELETE FROM habits WHERE habit='{habitName}'")
        self.conn.commit()

    def addHabitStreak(self, habitName):
        from datetime import datetime
        from App.main import App

        # BU KISIM LAST UPDATED VE ŞİMDİKİ ZAMANDAN ÇIKARIR VE BİZE BİR İNT DEĞER DÖNDÜRÜR
        days = 0
        weeks = 0
        format = "%Y-%m-%d"
        currentTime = str(datetime.now().date())
        lastUpdated = None
        self.cursor.execute(f"SELECT last_updated FROM habits WHERE habit='{habitName}'")
        for last in self.cursor:
            lastUpdated = str(last[0])
        self.conn.commit()
        lastFormatted = datetime.strptime(lastUpdated, format)
        nowFormatted = datetime.strptime(currentTime, format)
        delta = nowFormatted - lastFormatted # ŞİMDİKİ ZAMANDAN LAST UPDATE İ ÇIKARIR
        #print("delta days:  ", delta.days)
        #-------------------------------------------------------------------------

        self.cursor = self.conn.execute(f"SELECT week_or_daily from habits WHERE habit='{habitName}'")
        for row in self.cursor:
            if row[0] == "daily": # BU İF BLOĞU EĞER DAİLY HABİT Mİ DİYE KONTROL EDER
                if delta.days <= 1: # EĞER DAİLY HABİTE TAM ZAMANINDA CHECK OFF YAPĞARSAK BURASI ÇALIŞIR

                    # BURASI STREAK DAYS E 1 EKLER.
                    self.cursor = self.conn.execute(f"SELECT week_or_daily from habits WHERE habit='{habitName}'")
                    for row in self.cursor:
                        if row[0] == "daily":
                            self.cursor = self.conn.execute(
                                f"SELECT streak_days FROM habits WHERE habit = '{habitName}'")
                            for row in self.cursor:
                                days = int(row[0])
                            days += 1
                    #---------------------------------------------------------------------------------------
                            # BURASI EĞER STREAKLERİMİZ RECORD DAN BÜYÜK MÜ DİYE KONTROL EDER
                            self.cursor = self.conn.execute(f"SELECT record FROM habits WHERE habit = '{habitName}'")
                            for row in self.cursor:
                                if days > int(row[0]):
                                    self.cursor.execute(
                                        f"UPDATE habits SET record = '{days}' WHERE habit = '{habitName}'")
                                    self.conn.commit()
                            self.cursor.execute(f"UPDATE habits SET streak_days = '{days}' WHERE habit = '{habitName}'")
                            self.conn.commit()
                            #-----------------------------------------------------------------------

                            # EN SONUNDA LAST UPDATED KISMINI ŞİMDİKİ ZAMAN YAPAR.
                            self.cursor = self.conn.execute(f"SELECT streak_days FROM habits WHERE habit='{habitName}'")
                            for row in self.cursor:
                                if int(row[0]) % 7 == 0:
                                    self.cursor = self.conn.execute(
                                        f"SELECT streak_weeks FROM habits WHERE habit='{habitName}'")
                                    for i in self.cursor:
                                        weeks = int(i[0])
                                    weeks += 1
                                    self.cursor.execute(
                                        f"UPDATE habits SET streak_weeks = '{weeks}' WHERE habit = '{habitName}'")
                            self.cursor.execute(
                                f"UPDATE habits SET last_updated='{currentTime}' WHERE habit='{habitName}'")
                            self.conn.commit()
                            #------------------------------------------------------------------
                else: # EĞER GÜNLÜK OLARAK DAİLY HABİTİ CHECK OFF YAPMAZSANIZ BURASI ÇALIŞIR.
                    print("You have broken your habit your daily streak and week has been reset to 0 ")
                    self.cursor.execute(
                        f"UPDATE habits SET streak_days='{0}', streak_weeks='{0}',last_updated='{nowFormatted.now().date()}' WHERE habit='{habitName}'")
                    self.conn.commit()
            if row[0] == "weekly": # BU İF BLOĞU WEEEKLY HABİT Mİ DİYE KONTROL EDER
                if delta.days >= 8: # EĞER HAFTADA BİR CHECK OFF YAPMAZSANIZ BU BLOK DEVREYE GİRER.
                    print("You have broken your habit your daily streak and week has been reset to 0 ")
                    # STREAK DAY VE WEEKS İ 0 A EŞİTLER VE LAST UPDATED İ ŞİMDİKİ ZAMAN YAPAR
                    self.cursor.execute(
                        f"UPDATE habits SET streak_days='{0}', streak_weeks='{0}',last_updated='{currentTime}' WHERE habit='{habitName}'")
                    self.conn.commit()
                if delta.days < 7: # EĞER 7 GÜNDEN ÖNCE CHECK OFF YAPARSANIZ SİZE SÜRENİN DOLMADIĞINI SÖYLER.
                    print(f"You have {delta.days} days past since last check-off")
                    App().mainMenu() # bizi ana menüye döndürür
                if delta.days == 7: # EĞER TAM ZAMANINDA GELİRSENİZ BURASI DEVREYE GİRER.
                    days=0
                    weeks=0

                    # WEEK İ 1 ARTIRIR
                    self.cursor.execute(F"SELECT streak_weeks FROM habits WHERE habit='{habitName}'")
                    for row in self.cursor:
                        weeks = int(row[0])
                    weeks += 1
                    self.cursor.execute(f"UPDATE habits SET streak_weeks = '{weeks}' WHERE habit = '{habitName}'")
                    self.conn.commit()
                    # ------------------------------------------------

                    # WEEK 1 GÜN ARTTIĞI İÇİN STREAK DAYS'İ DE 7 GÜN ARTIRMIŞ OLURUZ.
                    self.cursor.execute(f"SELECT streak_days FROM habits WHERE habit='{habitName}'")
                    seven_days_added = 7
                    for row in self.cursor:
                        seven_days_added += row[0]
                    self.cursor.execute(
                        f"UPDATE habits SET streak_days = '{seven_days_added}' WHERE habit = '{habitName}'")
                    self.conn.commit()
                    #--------------------------------------------------------

                    # LAST UPDATED ŞİMDİKİ ZAMAN OLUR.
                    self.cursor.execute(f"UPDATE habits SET last_updated='{currentTime}' WHERE habit='{habitName}'")
                    self.conn.commit()
                    #-----------------------------------------------


                    # EĞER REKORUNUZU AŞMIŞ OLURSANIZ BURASI DEVREYE GİRER.
                    self.cursor.execute(f"SELECT record FROM habits WHERE habit='{habitName}'")
                    for row in self.cursor:
                        self.conn.commit()
                        self.cursor.execute(f"SELECT streak_days FROM habits WHERE habit='{habitName}'")
                        for i in self.cursor:
                            if int(i[0]) >= row[0]:
                                self.cursor.execute(
                                    f"UPDATE habits SET record='{int(i[0])}' WHERE habit='{habitName}'")
                                self.conn.commit()
                        else:
                            App().mainMenu() # bizi ana menüye döndürür
                    #-----------------------------------------------------------


    def findLongestHabit(self):
        self.cursor.execute("SELECT habit, record FROM habits WHERE record = (SELECT MAX(record) FROM habits)")
        result=self.cursor.fetchone()
        return "Habit:", result[0], "Record:", result[1]

    def findAllDailyHabits(self):
        self.cursor.execute("SELECT habit FROM habits WHERE week_or_daily='daily'")
        habits = [row[0] for row in self.cursor.fetchall()]
        return habits
    def findNumberOfHabits(self):
        self.cursor.execute("SELECT COUNT(habit) FROM habits")
        result=self.cursor.fetchone()
        return result[0]
    def longestHabitStreak(self):
        self.cursor.execute("SELECT habit, streak_days FROM habits WHERE streak_days = (SELECT MAX(streak_days) FROM habits)")
        result = self.cursor.fetchone()
        return "Habit:", result[0], "Streak:", result[1]
    def sumOfAllDays(self):
        self.cursor.execute("SELECT SUM(streak_days) FROM habits")
        result=self.cursor.fetchone()
        return result[0]
    def sumOfAllWeeks(self):
        self.cursor.execute("SELECT SUM(streak_weeks) FROM habits")
        result = self.cursor.fetchone()
        return result[0]



    def printTable(self):
        self.cursor.execute("SELECT * FROM habits")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)






    def deleteTable(self):
        self.cursor.execute("DELETE FROM habits")
        self.conn.commit()
