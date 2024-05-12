
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Model(DeclarativeBase):
    pass


class User(Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

    employees = relationship('Employee', back_populates='user')

class Company(Model):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='companies')
    employees = relationship('Employee', back_populates='company')
    departments = relationship('Department', back_populates='company')
    bank_accounts = relationship('BankAccount', back_populates='company')

class Employee(Model):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    fullName = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'))
    dept_id = Column(Integer, ForeignKey('departments.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    acc_id = Column(Integer, ForeignKey('bank_accounts.id'))
    salary = Column(Integer)

    user = relationship('User', back_populates='employees')
    company = relationship('Company', back_populates='employees')
    department = relationship('Department', back_populates='employees')
    bank_account = relationship('BankAccount', back_populates='employees')

class Department(Model):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'))
    manager_id = Column(Integer, ForeignKey('employees.id'))

    company = relationship('Company', back_populates='departments')
    manager = relationship('Employee', foreign_keys=[manager_id])
    employees = relationship('Employee', foreign_keys=[Employee.dept_id])

class BankAccount(Model):
    __tablename__ = 'bank_accounts'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    bank = Column(String)
    name = Column(String)

    company = relationship('Company', back_populates='bank_accounts')
    employees = relationship('Employee', back_populates='bank_account')

