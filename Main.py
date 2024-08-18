import GradesK2
import Grades35


var = str(input("Are you in grades K-2 or 3-5: ")).strip().lower()

if var == "k-2":
    GradesK2.main()
elif var == '3-5':
    Grades35.main()