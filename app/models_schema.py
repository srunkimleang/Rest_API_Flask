from app import ma
from app.models import TaskSkills, User, Task, Skill

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    assign_task = ma.Nested("TaskSchema", many=True, only=("name","objective",'id'))

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk=True
    user = ma.Nested('UserSchema', many=False, only=('name','email'))
    skills = ma.Nested('SkillSchema', many=True,  only=('name','code','id'))
    task_skills = ma.Nested('TaskSkillsSchema', many=True, exclude=('task_id', 'skill_id', 'task', 'id'))

class SkillSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Skill
    tasks = ma.Nested('TaskSchema', many=True, only=('name',"id", 'objective'))
    task_skills = ma.Nested('TaskSkillsSchema', many=True, exclude=('skill_id', 'task_id','skill', 'id'))

class TaskSkillsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskSkills
        include_fk=True
    #task_id
    #skill_id
    """making skill and task can access each other via this task_skills"""
    task = ma.Nested('TaskSchema', many=False, only=('name', 'id'))
    skill = ma.Nested('SkillSchema', many=False, only=('name', 'id'))