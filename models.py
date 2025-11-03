from dataclasses import dataclass,field
from typing import List, Dict, Optional, Tuple

# A dataclass is a special feature in Python helps you create classes meant to store data — without writing a lot of repetitive code.

@dataclass
class Student:
    email_address: str
    first_name: str
    last_name: str
    course_id: str
    grade: str
    marks: float


@dataclass
class Course:
    course_id: str
    course_name: str
    description: str = ""
    credits: int = 3   


@dataclass
class Grade:
    grade_id: str
    grade: str
    marks_range: str 


@dataclass
class Professor:
    professor_id: str   
    name: str
    rank: str
    course_id: str
