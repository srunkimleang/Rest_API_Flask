from sqlalchemy.orm import backref
from app import db


# TaskSkills = db.Table('task_skills',
#                         db.Column('id', db.Integer, primary_key=True),
#                         db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
#                         db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
# )
   
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    assign_task = db.relationship('Task',backref='user', lazy=True)
    def __init__(self, name, email):
        self.name=name
        self.email=email
    def __repr__(self):
        return str(self.name)

class Task(db.Model):
    __tablename__='task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    objective = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    skills = db.relationship('Skill' , secondary='task_skills')
    def __init__(self, name, objective, user_id):
        self.name=name
        self.objective=objective
        self.user_id=user_id
    def __repr__(self):
        return str(self.name)

class Skill(db.Model):
    __tablename__='skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(20))
    tasks = db.relationship('Task', secondary='task_skills')
    def __init__(self, name, code):
        self.name=name
        self.code=code
    def __repr__(self):
        return str(self.name)

class TaskSkills(db.Model):  ## similar to association table of taskskills(many to many)
    __tablename__='task_skills'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task = db.relationship('Task', backref=db.backref('task_skills'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    skill = db.relationship('Skill', backref=db.backref('task_skills'))
    skill_status = db.Column(db.String(50), default='1')
