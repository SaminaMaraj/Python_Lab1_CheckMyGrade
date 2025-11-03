import sys, time
from models import Student, Course, Professor, Grade
import storages as storage 
from security import encrypt_password, decrypt_password 



def prompt(msg):
    return input(msg).strip()



def add_sample_grade_scale():
    try:
       storage.add_grade(Grade("A", "A", "90-100"))
       storage.add_grade(Grade("B", "B", "80-89"))
       storage.add_grade(Grade("C", "C", "70-79"))
       storage.add_grade(Grade("D", "D", "60-69"))
       storage.add_grade(Grade("F", "F", "<60"))
    except Exception:
        pass



def menu():
    add_sample_grade_scale()
    while True:
        print("\n=== CheckMyGrade ===")
        print("1) Add Student  2) Delete Student  3) Update Student  4) Search Students")
        print("5) Sort Students 6) Courses CRUD   7) Professors CRUD 8) Login/Users")
        print("9) Reports/Stats 0) Exit")
        choice = prompt("Select: ")
        if choice == "1":
            email = prompt("Email: ")
            first = prompt("First name: ")
            last = prompt("Last name: ")
            course = prompt("Course ID: ")
            grade = prompt("Grade (A-F): ")
            marks = float(prompt("Marks (0-100): "))
            storage.add_student(Student(email, first, last, course, grade, marks))
            print("Added.")


        elif choice == "2":
            email = prompt("Email to delete: ")
            storage.delete_student(email)
            print("Deleted.")


        elif choice == "3":
            email = prompt("Email to update: ")
            field = prompt("Field (first_name,last_name,course_id,grade,marks): ")
            value = prompt("New value: ")
            if field == "marks":
                value = float(value)
            storage.update_student(email, **{field: value})
            print("Updated.")

        elif choice == "4":
            term = prompt("Search term (matches first/last/email/course): ").lower()
            results, t =storage.search_students(lambda r: term in r['First_name'].lower()
                                                 or term in r['Last_name'].lower()
                                                 or term in r['Email_address'].lower()
                                                 or term in r['Course_id'].lower())
            print(f"Found {len(results)} students in {t:.6f}s")
            for r in results[:20]:
                print(r)

        elif choice == "5":
            by = prompt("Sort by (Marks or Email_address): ")
            reverse = prompt("Descending? (y/n): ").lower() == "y"
            rows, t = storage.sort_students(by=by, reverse=reverse)
            print(f"Sorted {len(rows)} students in {t:.6f}s (showing top 20)")
            for r in rows[:20]:
                print(r)

        elif choice == "6":
            sub = prompt("(a)dd (d)elete (u)pdate course? ")
            if sub == "a":
                cid = prompt("Course ID: ")
                name = prompt("Course name: ")
                desc = prompt("Description: ")
                credits = int(prompt("Credits: "))
                storage.add_course(Course(cid, name, desc, credits))
                print("Course added.")

            elif sub == "d":
                cid = prompt("Course ID: ")
                storage.delete_course(cid)
                print("Course deleted.")

            elif sub == "u":
                cid = prompt("Course ID: ")
                field = prompt("Field (course_name,description,credits): ")
                value = prompt("New value: ")
                if field == "credits":
                    value = int(value)
                storage.update_course(cid, **{field: value})
                print("Course updated.")

        elif choice == "7":
            sub = prompt("(a)dd (d)elete (u)pdate professor? ")
            if sub == "a":
                pid = prompt("Professor email (id): ")
                name = prompt("Name: ")
                rank = prompt("Rank: ")
                cid = prompt("Course ID: ")
                storage.add_professor(Professor(pid, name, rank, cid))
                print("Professor added.")
            elif sub == "d":
                pid = prompt("Professor id: ")
                storage.delete_professor(pid)
                print("Professor deleted.")
            elif sub == "u":
                pid = prompt("Professor id: ")
                field = prompt("Field (name,rank,course_id): ")
                value = prompt("New value: ")
                storage.update_professor(pid, **{field: value})
                print("Professor updated.")
                
        elif choice == "8":
            sub = prompt("(r)egister (l)ogin (c)hange password? ")   
            if sub == "r":
                uid = prompt("User id (email): ")
                pw = prompt("Password: ")
                role = prompt("Role (student/professor/admin): ")
                token = encrypt_password(pw)
                storage.add_login(uid, token, role)
                print("User registered (password encrypted).")
            elif sub == "l":
                uid = prompt("User id: ")
                pw = prompt("Password: ")
                rec =storage.get_login(uid)
                if rec and decrypt_password(rec['Password']) == pw:
                    print("Login success.")
                else:
                    print("Login failed.")
            elif sub == "c":
                uid = prompt("User id: ")
                newpw = prompt("New password: ")
                token = encrypt_password(newpw)
                storage.update_login(uid, password=token)
                print("Password updated.")
        elif choice == "9":
            sub = prompt("(c)ourse-wise (p)rofessor-wise (s)tudent-wise stats/report? ")
            if sub == "c":
                cid = prompt("Course ID: ")
                stats =storage.course_statistics(cid)
                rows =storage.report_by_course(cid)
                print("Stats:", stats)
                print("Students (first 20):")
                for r in rows[:20]:
                    print(r)
            elif sub == "p":
                pid = prompt("Professor id: ")
                rows =storage.report_by_professor(pid)
                print(f"{len(rows)} students (first 20):")
                for r in rows[:20]:
                    print(r)
            elif sub == "s":
                email = prompt("Student email: ")
                rows =storage.report_by_student(email)
                print(f"{len(rows)} record(s):")
                for r in rows:
                    print(r)
        elif choice == "0":
            print("Bye.")
            break
        else:
            print("Invalid choice.")   



if __name__ == "__main__":
    menu()
