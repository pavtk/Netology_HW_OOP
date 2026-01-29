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

    def __eq__(self, other):
        return (
            self.average_grade(self.grades) == other.average_grade(other.grades)
            if isinstance(self, type(other)) else NotImplemented
        )

    def __lt__(self, other):
        return (
            self.average_grade(self.grades) < other.average_grade(other.grades)
            if isinstance(self, type(other)) else NotImplemented
        )


    def __gt__(self, other):
        return (
            self.average_grade(self.grades) > other.average_grade(other.grades)
            if isinstance(self, type(other)) else NotImplemented
        )


class Student(CourseMemberWithGrades):
    def __init__(self, name, surname, gender):
        super().__init__()
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []

    def rate_lecture(self, lecturer, course, grade):
        if (
                isinstance(lecturer, Lecturer)
                and course in self.courses_in_progress
                and course in lecturer.courses_attached
                and grade in range(1, 11)
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
        CourseMemberWithGrades.__init__(self)
        super().__init__(name, surname)

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: {self.average_grade(self.grades)}\n'
        )


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (
                isinstance(student, Student)
                and course in self.courses_attached
                and course in student.courses_in_progress
                and grade in range(1, 11)
        ):
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


def get_average_grade(course_members: List[Student | Lecturer], course: str):
    all_grades = []
    total_len = 0
    if len(course_members) == 0:
        return 0
    for member in course_members:
        if not isinstance(member, Student) and not isinstance(member, Lecturer):
            raise TypeError('Error object type is not Student or Lecturer')
    if type(course_members[0]) == Student:
        for student in course_members:
            if course in student.courses_in_progress:
                all_grades += student.grades.get(course)
                total_len += len(student.grades.get(course))
    elif type(course_members[0]) == Lecturer:
        for lecturer in course_members:
            if course in lecturer.courses_attached:
                all_grades += lecturer.grades.get(course)
                total_len += len(lecturer.grades.get(course))
    return sum(all_grades) / total_len


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

print(lecturer > lecturer)
print(lecturer != lecturer)
python_student = Student('Олег', 'Олегов', 'мужской')
java_student = Student('Ольга', 'Ольгова', 'женский')
python_student.courses_in_progress += ['Python']
python_student.finished_courses += ['Java']
java_student.courses_in_progress += ['Java']
java_student.finished_courses += ['Python']

python_lecturer = Lecturer('Иван', 'Иванов')
java_lecturer = Lecturer('Пётр', 'Петров')
python_lecturer.courses_attached += ['Python']
java_lecturer.courses_attached += ['Java']
python_reviewer = Reviewer('Фёдор', 'Фёдоров')
java_reviewer = Reviewer('Александр', 'Александров')
python_reviewer.courses_attached += ['Python']
java_reviewer.courses_attached += ['Java']
print(python_student.rate_lecture(python_lecturer, 'Python', 8))
print(python_student.rate_lecture(python_lecturer, 'Python', 5))
print(python_student.rate_lecture(java_lecturer, 'Python', 9))
print(java_student.rate_lecture(java_lecturer, 'Java', 7))
print(java_student.rate_lecture(java_lecturer, 'Java', 9))
print(python_reviewer.rate_hw(python_student, 'Python', 7))
print(python_reviewer.rate_hw(python_student, 'Python', 4))
print(python_reviewer.rate_hw(java_student, 'Python', 8))
print(java_reviewer.rate_hw(java_student, 'Java', 7))
print(java_reviewer.rate_hw(java_student, 'Java', 6))
print(python_student)
print(java_student)
print(python_student > java_student)
print(python_student < java_student)
print(python_student == java_student)

print(python_lecturer)
print(java_lecturer)
print(java_lecturer > python_lecturer)
print(java_lecturer < python_lecturer)
print(java_lecturer == java_lecturer)
print(java_lecturer == 5)
print(get_average_grade([python_student, java_student], 'Python'))
print(get_average_grade([python_lecturer, java_lecturer], 'Python'))

