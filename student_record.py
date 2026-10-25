"""
File 1: student_record.py
Description: Data model and custom exception definitions for Student Record management.
"""

class DatabaseException(Exception):
    """Base exception class for Database Engine errors."""
    pass

class DuplicateKeyException(DatabaseException):
    """Raised when an insertion violates Student ID uniqueness."""
    pass

class RecordNotFoundException(DatabaseException):
    """Raised when a point search fails to locate a Student ID."""
    pass

class InvalidRecordException(DatabaseException):
    """Raised when record initialization fails validation rules."""
    pass

class InvalidQueryRangeException(DatabaseException):
    """Raised when range query bounds are logically invalid."""
    pass


class StudentRecord:
    """Represents a validated Student Record in the database."""
    def __init__(self, student_id: int, name: str, gpa: float, department: str, enrollment_year: int):
        self._validate(student_id, name, gpa, department, enrollment_year)
        self.student_id = int(student_id)
        self.name = str(name).strip()
        self.gpa = float(gpa)
        self.department = str(department).strip()
        self.enrollment_year = int(enrollment_year)

    @staticmethod
    def _validate(student_id: int, name: str, gpa: float, department: str, enrollment_year: int):
        if not isinstance(student_id, int) or student_id <= 0:
            raise InvalidRecordException(f"Invalid Student ID: '{student_id}'. ID must be a positive integer.")
        if not name or not isinstance(name, str) or len(name.strip()) == 0:
            raise InvalidRecordException("Student name cannot be empty.")
        if not isinstance(gpa, (int, float)) or not (0.0 <= gpa <= 4.0):
            raise InvalidRecordException(f"Invalid GPA: '{gpa}'. GPA must be a float between 0.0 and 4.0.")
        if not department or not isinstance(department, str):
            raise InvalidRecordException("Department field cannot be empty.")
        if not isinstance(enrollment_year, int) or enrollment_year < 1900 or enrollment_year > 2100:
            raise InvalidRecordException(f"Invalid Enrollment Year: '{enrollment_year}'.")

    def display(self) -> None:
        """Formats and prints the record details."""
        print(f"ID: {self.student_id:<6} | Name: {self.name:<16} | GPA: {self.gpa:.2f} | "
              f"Dept: {self.department:<6} | Year: {self.enrollment_year}")

    def __repr__(self) -> str:
        return f"StudentRecord(ID={self.student_id}, Name='{self.name}', GPA={self.gpa})"
    
    