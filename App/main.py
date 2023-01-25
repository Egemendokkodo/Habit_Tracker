from DataFrame.DataModel import Data
from DataFrame.SqliteHelper import SQL

"""
    APP CLASS
    ---------
    
main.py dosyasının içinde bulunan app class ilk çağırılan class tır
uygulamanın çalışması için main.py'ın çalışması gerekir.




"""




class App:
    def __init__(self):
        self.sql = SQL()

    def mainMenu(self):

        # init e almamamın sebebi, her seferinde main menuye dönüldüğünde tablonun yenilenmesi lazım, eğer inite alsaydım class sadece 1 kere çağırıldığından tabloyu yenilemeyecekti.
        Data().showData()

        print(" / WELCOME TO HABIT TRACKER \ ".center(90))
        print("  | Please Select an Option  |  ".center(90))
        print("   (1) Check Off Habit    ".center(90))
        print("   (2) Manage Habits    ".center(90))
        print("   (3) Analyze Habits   ".center(90))
        print("   (4) Exit    ".center(90))
        choice = input("\nYour Choice: ")

        if choice == "1":
            self.checkOff()
        if choice == "2":
            self.manageHabits()
        if choice == "3":
            print("(1) What's my longest habit?\n(2) What's the list of my current daily habits?\n"
                  "(3) What's the number of habits\n(4) What's my longest habit streak?\n"
                  "(5) What's the sum of all days in my tracker\n(6) What's the sum of all weeks in my tracker\n")
            analyzeChoice = input("Please select a choice: ")
            # this if statements returns the answer of picked options from above
            if analyzeChoice == "1":
                print(self.sql.findLongestHabit())
                self.mainMenu()
            if analyzeChoice == "2":
                print("Your daily habits are: ")
                print(self.sql.findAllDailyHabits())
                self.mainMenu()
            if analyzeChoice == "3":
                print(f"You have {self.sql.findNumberOfHabits()} habits")
                self.mainMenu()
            if analyzeChoice == "4":
                print("Your longest habit streak is: ", self.sql.longestHabitStreak())
                self.mainMenu()
            if analyzeChoice == "5":
                print("Sum of all days is: ", self.sql.sumOfAllDays())
                self.mainMenu()
            if analyzeChoice == "6":
                print("Sum of all weeks is: ", self.sql.sumOfAllWeeks())
                self.mainMenu()
            #--------------------------------------------------------------
    def checkOff(self):
        # bu fonksiyon eğer habit'i check off yapmak isterseniz çağırılır.
        habitName = input("Please enter a habit name so i can add to your Habit Streak (0 for main menu): ")
        if habitName == 0:
            self.mainMenu()
        else:
            self.sql.addHabitStreak(f"{habitName}") # addHabitStreak fonksiyonu içerideki işlemleri tamamladıktan sonra--
            # ---bize sonucu verir, bu işlemleri SqliteHelper.py dosyasında anlattım.
            self.mainMenu()

    def manageHabits(self):
        print("What do you want to do on your habit tracker? ".center(90))
        print("(1) Add New Habit".center(90))
        print("(2) Delete a Habit".center(90))
        print("(3) Back to main menu".center(90))
        choiceHabits = input("\nYour Choice: ")
        if choiceHabits == "1":
            backChoice = input("Add Habits (you can go back by pressing 1 to continue, press any button): ")
            if backChoice == "1":
                self.mainMenu()
            else:
                #burada sql tablosuna eklediğimiz verileri bizden ister. ve sql e ekler.
                habitName = input("Your habit name: ")
                habitDesc = input("Enter a description for your habit: ")
                dayOrWeek = input("Daily or Weekly?: ").lower()
                startDay = input("Start Date YYYY-MM-DD: ")

                self.sql.addTable(habitName, habitDesc, dayOrWeek, startDay)
                print(f"{habitName} Has Been Successfully Added to your habits".upper())
                self.mainMenu() # son olarak main menuye döner
                #----------------------------------------------------------------------
        if choiceHabits == "2":
            choice = input("Which habit would you like to delete? (1 for main menu): ")
            if choice == "1":
                self.mainMenu()
            else:
                # eğer tablodan habit ismine göre satır silmek istersek bu fonksiyonu(deleteFromTable) çağırırız
                self.sql.deleteFromTable(f"{choice}")
                print(f"Successfully Deleted {choice} from your habit table".upper())
                self.mainMenu()
                #-------------------------------------------------
        if choiceHabits == "3":
            self.mainMenu()


if __name__ == "__main__":
    App().mainMenu()  # program burada başlar
