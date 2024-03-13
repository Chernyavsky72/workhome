class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades_for_lectures:
                lecturer.grades_for_lectures[course] += [grade]
            else:
                lecturer.grades_for_lectures[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        avg_grade = self.average_grade()
        courses_in_progress_str = ', '.join(self.courses_in_progress)
        finished_courses_str = ', '.join(self.finished_courses)
        return (f'Имя: {self.name}\nФамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg_grade}\n'
                f'Курсы в процессе изучения: {courses_in_progress_str}\n'
                f'Завершенные курсы: {finished_courses_str}')

    def average_grade(self):
        total = []
        for grades in self.grades.values():
            total.extend(grades)
        return round(sum(total) / len(total), 1) if total else 0

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades_for_lectures = {}

    def __str__(self):
        avg_grade = self.average_grade()
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {avg_grade}'

    def average_grade(self):
        total = []
        for grades in self.grades_for_lectures.values():
            total.extend(grades)
        return round(sum(total) / len(total), 1) if total else 0

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Reviewer(Mentor):
    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def average_grade_for_students(students, course):
    total_grades = []
    for student in students:
        if course in student.grades:
            total_grades.extend(student.grades[course])
    return round(sum(total_grades) / len(total_grades), 1) if total_grades else 0


def average_grade_for_lecturers(lecturers, course):
    total_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades_for_lectures:
            total_grades.extend(lecturer.grades_for_lectures[course])
    return round(sum(total_grades) / len(total_grades), 1) if total_grades else 0


# Студенты
student1 = Student('Дмитрий', 'Вдовин', 'male')
student1.finished_courses += ['Введение в программирование']
student1.courses_in_progress += ['Python', 'Git']
student2 = Student('Екатерина', 'Афансьева', 'female')
student2.courses_in_progress += ['Python']
student2.finished_courses += []

# Лекторы
lecturer1 = Lecturer('Виктор', 'Иванов')
lecturer1.courses_attached += ['Python']
lecturer2 = Lecturer('Анатолий', 'Войнов')
lecturer2.courses_attached += ['Git']

# Проверяющие
reviewer1 = Reviewer('Роман', 'Кухарук')
reviewer1.courses_attached += ['Python']
reviewer2 = Reviewer('Сергей', 'Орлов')
reviewer2.courses_attached += ['Git']

# Оценка студентов
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student2, 'Python', 8)
reviewer2.rate_hw(student1, 'Git', 9)
reviewer2.rate_hw(student2, 'Git', 8)

# Оценка Лекторов
student1.rate_lecturer(lecturer1, 'Python', 9)
student2.rate_lecturer(lecturer2, 'Python', 10)
student1.rate_lecturer(lecturer2, 'Git', 10)
student2.rate_lecturer(lecturer1, 'Git', 8)

# Информация о студентах, лекторах и проверяющих
print(f'________\nСтуденты:\n\n{student1}\n\n{student2}')
print(f'\n________\nЛекторы:\n\n{lecturer1}\n\n{lecturer2}')
print(f'\n________\nПроверяющие:\n\n{reviewer1}\n\n{reviewer2}')

# Вывод оценок
print(average_grade_for_students([student1, student2], 'Python'))
print(average_grade_for_lecturers([lecturer1, lecturer2], 'Git'))