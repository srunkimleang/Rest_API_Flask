from app import ma
from app.models import User, Task, Skill

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

class SkillSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Skill
    tasks = ma.Nested('TaskSchema', many=True, only=('name',"id", 'objective'))

