from random import randint
from typing import List

class CourseMemberWithGrades:
    def __init__(self):
        self.grades = {}

    @staticmethod
    def average_grade(grades):
        if not grades.values():
            return 0
        all_grades = [grade for grade_list in grades.values() for grade in grade_list]
        if len(all_grades) == 0:
            return 0
        return sum(all_grades) / len(all_grades)

    @classmethod
    def check_isinstance(cls, obj):
        if isinstance(obj, cls):
            return True
        else:
            raise TypeError(f'Error object type is not {cls.__name__}')

    def __eq__(self, other):
        self.check_isinstance(other)
        if (self.average_grade(self.grades) == other.average_grade(other.grades)):
            return True
        else:
            return False

    def __lt__(self, other):
        self.check_isinstance(other)
        if self.average_grade(self.grades) < other.average_grade(other.grades):
            return True
        else:
            return False

    def __gt__(self, other):
        self.check_isinstance(other)
        if (self.average_grade(self.grades) > other.average_grade(other.grades)):
            return True
        else:
            return False


class Student(CourseMemberWithGrades):
    def __init__(self, name, surname, gender):
        super().__init__()
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if (
                isinstance(lecturer, Lecturer)
                and course in self.courses_in_progress
                and course in lecturer.courses_attached
        ):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: {self.average_grade(self.grades)}\n'
            f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
            f'Завершенные курсы: {", ".join(self.finished_courses)}\n'
        )


class Mentor():
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor, CourseMemberWithGrades):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}


    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: {self.average_grade(self.grades)}\n'
        )


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
        )


def get_average_garde(course_members: List[Student | Lecturer], course: str):
    all_grades = []
    for member in course_members:
        if not isinstance(member, Student) and not isinstance(member, Lecturer):
            raise TypeError('Error object type is not Student or Lecturer')
    if len(course_members) == 0:
        return 0
    if type(course_members[0]) == Student:
        all_grades = (
            [
                sum(grades) / len(grades)
                for student in course_members if course in student.courses_in_progress and
                len(grades := student.grades.get(course)) > 0
            ]
        )
    elif type(course_members[0]) == Lecturer:
        all_grades = (
            [
                sum(grades) / len(grades)
                for lecturer in course_members if course in lecturer.courses_attached and
                len(grades := lecturer.grades.get(course)) > 0
            ]
        )
    return sum(all_grades) / len(all_grades)


lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
print(isinstance(lecturer, Mentor))
print(lecturer.courses_attached)
print(reviewer.courses_attached)

lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')
student_one = Student('Алёхин', 'Олег', 'М')

student.courses_in_progress += ['Python', 'Java']
student_one.courses_in_progress += ['Java', 'C++']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++', 'Git']

print(student.rate_lecture(lecturer, 'Python', 7))  # None
print(student.rate_lecture(lecturer, 'Python', 8))  # None
print(student.rate_lecture(lecturer, 'Java', 8))  # Ошибка
print(student.rate_lecture(lecturer, 'С++', 8))  # Ошибка
print(student.rate_lecture(reviewer, 'Python', 6))  # Ошибка

print(lecturer.grades)
print(reviewer)
print(lecturer)
student.finished_courses += ['Введение в программирование']
student.finished_courses += ['Python']
reviewer.rate_hw(student, 'Python', 9)
reviewer.rate_hw(student, 'Python', 8)
reviewer.rate_hw(student, 'Java', 6)
reviewer.rate_hw(student, 'Java', 5)
reviewer.rate_hw(student_one, 'C++', 5)
reviewer.rate_hw(student_one, 'C++', 5)
print(student)
print(student_one)

students = [
    Student("Алексей", "Иванов", "мужской"),
    Student("Мария", "Петрова", "женский"),
    Student("Дмитрий", "Сидоров", "мужской"),
    Student("Анна", "Кузнецова", "женский"),
    Student("Иван", "Смирнов", "мужской"),
    Student("Елена", "Васильева", "женский"),
    Student("Сергей", "Попов", "мужской"),
    Student("Ольга", "Новикова", "женский"),
    Student("Андрей", "Федоров", "мужской"),
    Student("Наталья", "Морозова", "женский")
]

all_courses = ["Python", "C++", "Git"]
for student in students:
    student.courses_in_progress += all_courses
for student in students:
    reviewer.rate_hw(student, all_courses[0], randint(1, 10))

print(get_average_garde(students, all_courses[0]))
all_lecturers = [lecturer]
print(get_average_garde(all_lecturers, all_courses[0]))
student.grades['Git'] = [10, 9, 8, 10, 10, 10, 10, 10, 10, 10, 10]
print(student.grades)
print(student)
print(student_one)
print(student < student_one)

print(lecturer > lecturer)
print(lecturer != lecturer)