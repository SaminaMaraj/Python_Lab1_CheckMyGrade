import unittest, random, string
from models import Student, Course, Professor, Grade
import storages as storage
from security import encrypt_password, decrypt_password


def rand_email(prefix="user"):
    return f"{prefix}_{''.join(random.choices(string.ascii_lowercase+string.digits,k=8))}@example.com"


class TestCheckMyGrade(unittest.TestCase):

    def test_student_crud_and_sort_search(self):
        # ensure course exists
        cid = "DATA200"
        try:
            storage.add_course(Course(cid, "Data Science", "Intro DS & Python", 3))
            
           
        except Exception:
            pass

        # add 1000 students
        emails = []
        for i in range(1000):
            email = rand_email("s")
            emails.append(email)
            storage.add_student(Student(email, "First", "Last", cid, "A", random.uniform(50, 100)))

        # search timing
        term = emails[500].split("@")[0]
        results, t = storage.search_students(lambda r: term.lower() in r['Email_address'].lower())
        self.assertGreaterEqual(len(results), 1)
        print(f"Search time for 1000 records: {t:.6f}s")

        # sort by marks desc timing
        rows, t =storage.sort_students(by="Marks", reverse=True)
        self.assertGreaterEqual(len(rows), 1000)

        print(f"Sort time for 1000 records: {t:.6f}s")

        # update one
        storage.update_student(emails[0], marks=99.99)
        results, _ =storage.search_students(lambda r: r['Email_address']==emails[0])
        self.assertEqual(results[0]['Marks'], '99.99')

        # delete few
        storage.delete_student(emails[1])
        results, _ =storage.search_students(lambda r: r['Email_address']==emails[1])
        self.assertEqual(len(results), 0)

    def test_course_professor_crud(self):
        cid = "DATA201"
        storage.add_course(Course(cid, "ML", "Machine Learning", 4))
        storage.update_course(cid, course_name="ML Basics", credits=5)
        storage.delete_course(cid)

        pid = rand_email("prof")
        storage.add_professor(Professor(pid, "Prof X", "Senior", "DATA200"))
        storage.update_professor(pid, name="Prof Y")
        storage.delete_professor(pid)

    def test_login_encryption(self):
        uid = rand_email("login")
        pw = "Welcome12#_"
        token = encrypt_password(pw)
        storage.add_login(uid, token, "student")
        rec =storage.get_login(uid)
        self.assertEqual(decrypt_password(rec['Password']), pw) 

if __name__ == "__main__":
    unittest.main() 





