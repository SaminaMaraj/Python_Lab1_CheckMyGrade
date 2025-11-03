#CheckMyGrade(Console App)

A console-based, object-oriented python application for managing students, courses, professors, grades, and user login with CSV persistence.

## Features
- OOP classes: Students, Course, professor, Grade, LoginUser
-CSVstorage: students.csv, courses.csv, professors.csv, login,csv
- CRUD (add/delete/modify) for all entities
- Search and sort with timing 
- Statistics: average and median marks per course
- Reports: course-wise, professor-wise, student-wise
- Simple reversible password encryption 
- Unit Tests including 1000 record scenarios
- GitHub - ready layout

## Run
```bash
python app.py
```
The app uses the `data/` folder for CSV files. First run will create the CSVs with headers if missing.

## Notes
- Encryption uses a simple XOR + Base64 approach for didactic purposes. Do **not** use in production.
- Sorting and searching print runtime in seconds 



