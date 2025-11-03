import csv, os, time
from typing import List, Tuple,  Dict, Optional, Callable
from models import Student, Course, Professor, Grade


DATA_DIR = os.path.join(os.path.dirname(__file__),"data")

FILES = {
    "students": os.path.join(DATA_DIR, "students.csv"),
    "courses": os.path.join(DATA_DIR,"courses.csv"),
    "professors": os.path.join(DATA_DIR,"professors.csv"),
    "login":os.path.join(DATA_DIR,"login.csv"),
    "grades": os.path.join(DATA_DIR,"grades.csv"),

}

HEADERS ={
    "students": ["Email_address","First_name","Last_name","Course_id","Grade","Marks"],
    "courses": ["Course_id","Course_name","Description","Credits"],
    "professors": ["Professor_id","Professor_Name","Rank","Course_id"],
    "login": ["User_id","Password","Role"],
    "grades": ["Grade_id","Grade","Marks_range"],
}

# _ st the beginning means this is a internal helper function. Not meant to be called directly by the users. 
# This function is to make sure all the necessary CSV files exist before the program starts using them. 
#os.makedirs() creates a folder. DATA_DIR is the path for data folder. 
# exist_ok = True means, if the folder already exist do not throw  error. just continue.
#.items() let us loop over both the key (Ex: "student") and path (like 'data/students.csv')

def _ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    for key, path in FILES.items():
        if not os.path.exists(path):
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer =csv.writer(f)
                writer.writerow(HEADERS[key])       


_ensure_files()

#CRUD Helpers

def _read_all(key: str) -> List[dict]:
    items = []
    with open(FILES[key], newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(row)
    return items

# f => is the file object opened earlier (ex: students.csv). 
# HEADER[key]=>  List of column names for that file (ex: "Email_address") 

'''for r in rows, loop go through a list of dictionaries , where each dictionary represent one record. 
EX: rows = [
    {"Email_address": "samina@sjsu.edu", "First_name": "samina", "Last_name": "maraj", "Course_id": "DATA200", "Grade": "A", "Marks": "95"},
    {"Email_address": "shaila@sjsu.edu", "First_name": "Shaila", "Last_name": "mery", "Course_id": "DATA200", "Grade": "B", "Marks": "85"}
]'''

def _write_all(key: str, rows: List[dict]):
    with open(FILES[key], "w", newline="", encoding="utf-8") as f:
        # This line creates a writer object that knows what columns to expect (field name )
        writer = csv.DictWriter(f, fieldnames=HEADERS[key])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


# Here we are referring the Student class inside the add_student fn. 
def add_student(s: Student):
    rows = _read_all("students")
    # Here email must be unique
    # rows is a list of dictionaries which is representing all the students are already stored in the CSV file

    # r["Email_address"].lower() gets the email address from each record r, and converts it into a lowercase (to make comparison case- insensitive)
    # s.email_address.lower() gets the email address from the new student object we are trying to add (s) and also makes it lower case
    if any(r["Email_address"].lower() == s.email_address.lower( ) for r in rows):
        raise ValueError("Student email must be unique and not null.")
    rows.append({
        "Email_address": s.email_address,
        "First_name": s.first_name,
        "Last_name": s.last_name,
        "Course_id": s.course_id,
        "Grade": s.grade,
        "Marks": f"{float(s.marks):.2f}",
        })
    _write_all("students", rows)



def delete_student(email: str):
    rows = _read_all("students")
    # making a new list that will include only records whose email does not match the one we are trying to delete.
    new_rows = [r for r in rows if r["Email_address"].lower() != email.lower()]
    # If the number of rows did not change after filtering (EX: Before 2 rows, after one rows => not same length, means student was found and deleted )
    if len(new_rows) == len(rows):
        raise ValueError("Student not found.")
    _write_all("students", new_rows)

# **updates means we can pass any number of keyword arguments (EX: update_student("sam@mycsu.edu", grade="B", marks=88.5))
'''updates.items() when we call function like this, update_student("samina@sjsu.edu", grade="A", marks=90).
 The updates parameter becomes a dictionary: updates ={ "grade": "A", "markes": 90}, which means when we will call updates.items(), 
 it will give us key value pairs like ("grade", "A") and ("marks", 90)'''

'''r[key_map[k]] = str(v), here for example, k= "grade", v ="A". then key_map[k]=> "Grade". r[Grade]= "B". 
for the next pair ("marks", 90), it will become: r["Marks"] = "90"'''
# str(v), when writing CSV files, everything should be stored as a text 

def update_student(email: str, **updates):
    rows = _read_all("students")
    found = False
    for r in rows:
        if r["Email_address"].lower() == email.lower():
            found = True
            for k, v in updates.items():
                key_map = {
                    "first_name": "First_name",
                    "last_name": "Last_name",
                    "course_id": "Course_id",
                    "grade": "Grade",
                    "marks": "Marks",
                }
                if k in key_map:
                    r[key_map[k]] = str(v)
    if not found:
        raise ValueError("Student not found.")
    _write_all("students", rows)


# predict is a function parameter which is a function that decides whether a student record matches the search condition. 
# start = time.perf_counter(), will record the current time. which will used to measure how long the search takes .
#  perf_counter() is preferred over time.time() because it is more accurate for timing the code .

'''predicate(r) returns True or False. When we call search_students(), it passes such function for ex: term = "Samina"
search_students(lambda r: term in r["First_name"].lower()), here for each record r,
 lambda checks whether "samina" shows in the first name. if it does, predict(r) will return True. '''

'''elapsed = time.perf_counter() - start, when the loop finises it calculates the time difference, which means that how long the search took.'''
'''results => returns a list of matching students. elapsed => returns, how long the search took'''

def search_students(predicate)->Tuple[List[dict], float]:
    start = time.perf_counter()
    rows= _read_all("students")
    results = [r for r in rows if predicate(r)]
    elapsed = time.perf_counter() - start
    return results, elapsed

def sort_students(by: str= "Marks", reverse: bool = False):
    start = time.perf_counter()
    rows = _read_all("students")
    if by == "Marks":
        rows.sort(key=lambda r: float(r["Marks"]), reverse=reverse)
    else:
        rows.sort(key=lambda r: r.get(by, "").lower(), reverse=reverse)
    elapsed = time.perf_counter() - start
    return rows, elapsed

#course
def add_course(c: Course):
    rows =_read_all("courses")
    if any (r["Course_id"].lower() == c.course_id.lower() for r in rows):
        raise ValueError("Course_id must be unique and not null.")
    rows.append({
        "Course_id": c.course_id,
        "Course_name": c.course_name,
        "Description": c.description,
        "Credits": str(c.credits)
    })
    _write_all("courses", rows)


def delete_course(course_id: str):
    rows =_read_all("courses")
    new_rows = [r for r in rows if r["Course_id"].lower() != course_id.lower()]
    if len(new_rows)==len(rows):
        raise ValueError("Course not found.")
    _write_all("courses", new_rows)

'''''if k in key_map,  checks whether the update field (ex: course_name) is a valid key in key_map.

 If it is then will change the column in the CSV record.
r[key_map[k]] = str(v), r is dictionary represents the current course record.
key_map[k] gets the exact CSV column name.
v is the new value passed. str(v),  converts it to a string (because CSVs store text)'''

def update_course(course_id: str, **updates):
    rows= _read_all("courses")
    found =False
    for r in rows:
        if r["Course_id"].lower()== course_id.lower():
            found = True
            for k, v in updates.items():
                key_map = {
                    "course_name": "Course_name",
                    "description": "Description",
                    "credits": "Credits"
                }
                if k in key_map:
                    r[key_map[k]] = str(v)
    if not found:
        raise ValueError("Course not found.")
    _write_all("courses", rows)



#professors

def add_professor(p: Professor):
    rows= _read_all("professors")
    if any (r["Professor_id"].lower()== p.professor_id.lower() for r in rows):
        raise ValueError("Professor_id must be unique and not null.")
    rows.append({
        "Professor_id": p.professor_id,
        "Professor_Name": p.name,
        "Rank": p.rank,
        "Course_id": p.course_id,
    })
    _write_all("professors", rows)


def delete_professor(professor_id: str):
    rows = _read_all("professors")
    new_rows = [r for r in rows if r["Professor_id"].lower() != professor_id.lower()]
    if len(new_rows) == len(rows):
        raise ValueError("Professor not found.")
    _write_all("professors", new_rows) 



def update_professor(professor_id: str, **updates):
    rows = _read_all("professors")
    found = False
    for r in rows:
        if r["Professor_id"].lower() == professor_id.lower():
            found = True
            for k, v in updates.items():
                key_map = {
                    "name": "Professor_Name",
                    "rank": "Rank",
                    "course_id": "Course_id",
                }
                if k in key_map:
                    r[key_map[k]] = str(v)
    if not found:
        raise ValueError("Professor not found.")
    _write_all("professors", rows)

#grades

def add_grade(g: Grade):
    rows= _read_all("grades")
    if any (r["Grade_id"].lower()== g.grade_id.lower() for r in rows):
        raise ValueError("Grade_id must be unique and not null.")
    rows.append({
        "Grade_id": g.grade_id,
        "Grade": g.grade,
        "Marks_range": g.marks_range,
    })
    _write_all("grades", rows)


def delete_grade(grade_id: str):
    rows = _read_all("grades")
    new_rows = [r for r in rows if r["Grade_id"].lower() != grade_id.lower()]
    if len(new_rows) == len(rows):
        raise ValueError("Grade not found.")
    _write_all("grades", new_rows)  


def update_grade(grade_id: str, **updates):
    rows = _read_all("grades")
    found = False
    for r in rows:
        if r["Grade_id"].lower() == grade_id.lower():
            found = True
            for k, v in updates.items():
                key_map = {
                    "grade": "Grade",
                    "marks_range": "Marks_range",
                }
                if k in key_map:
                    r[key_map[k]] = str(v)
    if not found:
        raise ValueError("Grade not found.")
    _write_all("grades", rows)


# login

def add_login(user_id: str, password_token: str, role: str):
    rows = _read_all("login")
    if any(r["User_id"].lower() == user_id.lower() for r in rows):
        raise ValueError("User_id must be unique and not null.")
    rows.append({"User_id": user_id, "Password": password_token, "Role": role})
    _write_all("login", rows)


def get_login(user_id: str):
    rows = _read_all("login")
    for r in rows:
        if r["User_id"].lower() == user_id.lower():
            return r
    return None


def update_login(user_id: str, **updates):
    rows = _read_all("login")
    found = False
    for r in rows:
        if r["User_id"].lower() == user_id.lower():
            found = True
            for k, v in updates.items():
                key_map = {"password": "Password", "role": "Role"}
                if k in key_map:
                    r[key_map[k]] = str(v)
    if not found:
        raise ValueError("User not found.")
    _write_all("login", rows)


# Reports and stats

def course_statistics(course_id: str):
    rows = _read_all("students")
    marks = [float(r["Marks"]) for r in rows if r["Course_id"].lower() == course_id.lower()]
    if not marks:
        return None
    avg = sum(marks) / len(marks)
    med = sorted(marks)[len(marks)//2] if len(marks)%2==1 else (sorted(marks)[len(marks)//2-1] + sorted(marks)[len(marks)//2]) / 2
    return {"count": len(marks), "average": avg, "median": med}

def report_by_course(course_id: str):
    rows = _read_all("students")
    return [r for r in rows if r["Course_id"].lower() == course_id.lower()] 

def report_by_professor(professor_id: str):
    pros = _read_all("professors")
    courses = [p["Course_id"] for p in pros if p["Professor_id"].lower() == professor_id.lower()]
    rows = _read_all("students")
    return [r for r in rows if r["Course_id"] in courses]

def report_by_student(email: str):
    rows = _read_all("students")
    return [r for r in rows if r["Email_address"].lower() == email.lower()]