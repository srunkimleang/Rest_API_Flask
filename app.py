from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/testing'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onetoone.db'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


@app.route('/')
@app.route('/home')
def home():
    return 'This is about one to one relationship!!'


###########################   Model  ############################
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    assign_task = db.relationship('Task', backref='user', lazy=True)
    def __init__(self, name, email):
        self.name=name
        self.email=email
    def __repr__(self):
        return str(self.name)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    objective = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    def __init__(self, name, objective, user_id, skill_id):
        self.name=name
        self.objective=objective
        self.user_id=user_id
        self.skill_id=skill_id
    def __repr__(self):
        return str(self.name)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(20))
    task = db.relationship('Task', backref='skill', lazy=True)
    def __init__(self, name, code):
        self.name=name
        self.code=code
    def __repr__(self):
        return str(self.name)


##########################  ModelSchema  #########################
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    assign_task = ma.Nested("TaskSchema", many=True, only=("name","objective",'id', "skill", "skill_id"))

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk=True
    user = ma.Nested('UserSchema', many=False, only=('name','email'))
    skill = ma.Nested('SkillSchema', many=False,  only=('name','code'))

class SkillSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Skill
    task = ma.Nested('TaskSchema', many=True, only=('name','objective',"id"))


#########################   POST_Method  #########################
@app.route('/user', methods=['POST'])
def create_user():
    name = request.json['name']
    email = request.json['email']
    check_name = User.query.filter_by(name=name)
    check_email = User.query.filter_by(email=email)
    if check_name is None and check_email is None:
        new_user= User(name, email)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User is created.'}), 200
    else:
        return jsonify({"message": "User is already taken."}), 400

@app.route('/task', methods=['POST'])
def create_task():
    name = request.json['name']
    objective = request.json['objective']
    user_id = request.json['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": f"User's id={user_id} doesn't exist."}), 400
    skill_id = request.json['skill_id']
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"message": f"Skill's id={skill_id} doesn't exist."}), 400
    new_task= Task(name, objective, user_id, skill_id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task is created.'}), 200

@app.route('/skill', methods=['POST'])
def create_skill():
    name = request.json['name']
    code = request.json['code']
    check_name = Skill.query.filter_by(name=name)
    check_code = Skill.query.filter_by(code=code)
    if check_name is None and check_code is None:
        new_skill= Skill(name, code)
        db.session.add(new_skill)
        db.session.commit()
        return jsonify({'message': 'Skill is created.'}), 200
    else:
        return jsonify({"message": "Skill is already existed."}), 400


#########################  GET_All_Method  ############################
###Get_User###
@app.route('/user', methods=['GET'])
def all_user():
    all_user = User.query.all()
    users_schema = UserSchema(many=True)
    users = users_schema.dump(all_user)
    return jsonify({"Users": users}), 200
    # users = db.session.query(User).all()
    # all_users = users_schema.dump(users)
    # return jsonify({'users': all_users})
@app.route('/user/<id>', methods=['GET'])
def single_user(id):
    user = User.query.get(id)
    user_schema = UserSchema()
    return user_schema.jsonify(user), 200
@app.route('/user/<id>/task', methods=['GET'])
def all_task_in_user(id):
    tasks = []
    for task in Task.query.filter_by(user_id=id):
        tasks.append(task.name)
    return jsonify(tasks), 200
###Get_Task###
@app.route('/task', methods=['GET'])
def all_task():
    all_task = Task.query.all()
    tasks_schema = TaskSchema(many=True)
    tasks = tasks_schema.dump(all_task)
    return jsonify({"Tasks": tasks}), 200
@app.route('/task/<id>', methods=['GET'])
def single_task(id):
    task = Task.query.get(id)
    task_schema = TaskSchema()
    return task_schema.jsonify(task), 200
###Get_Skill###
@app.route('/skill', methods=['GET'])
def all_skill():
    all_skill = Skill.query.all()
    skills_schema = SkillSchema(many=True)
    skills = skills_schema.dump(all_skill)
    return jsonify({"Skills": skills}), 200

@app.route('/skill/<id>', methods=['GET'])
def single_skill(id):
    skill = Skill.query.get(id)
    skill_schema = SkillSchema()
    return skill_schema.jsonify(skill), 200

@app.route('/skill/<id>/task', methods=['GET'])
def all_task_have_skill(id):
    tasks = []
    for task in Task.query.filter_by(skill_id=id):
        tasks.append(task.name)
    return jsonify(tasks), 200

##########################   PUT_Method   ##############################
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    update_user = User.query.get(id) #get user with id=id
    name = request.json['name']
    email = request.json['email']
    update_user.name = name
    update_user.email = email
    db.session.commit()
    user_schema = UserSchema()
    return user_schema.jsonify(update_user), 200

@app.route('/task/<id>', methods=['PUT'])
def update_task(id):
    update_task = Task.query.get(id)
    name = request.json['name']
    objective = request.json['objective']
    user_id = request.json['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": f"User's id={user_id} doesn't exist."}), 400
    skill_id = request.json['skill_id']
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"message": f"Skill's id={skill_id} doesn't exist."}), 400
    update_task.name = name
    update_task.objective = objective
    update_task.user_id = user_id
    update_task.skill_id = skill_id
    db.session.commit()
    task_schema = TaskSchema()
    return task_schema.jsonify(update_task), 200

@app.route('/skill/<id>', methods=['PUT'])
def update_skill(id):
    update_skill = Skill.query.get(id)
    name = request.json['name']
    code = request.json['code']
    update_skill.name = name
    update_skill.code = code
    db.session.commit()
    skill_schema = SkillSchema()
    return skill_schema.jsonify(update_skill), 200


##########################   DELETE_Method   ##############################
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    delete_user = User.query.get(id) #get user with id=id
    if not delete_user:
        return jsonify({"message": f"User's id={id} doesn't exist."}), 400
    else:
        db.session.delete(delete_user)
        db.session.commit()
        user_schema = UserSchema()
        return user_schema.jsonify(delete_user), 200


@app.route('/task/<id>', methods=['DELETE'])
def delete_task(id):
    delete_task = Task.query.get(id)
    if not delete_task:
        return jsonify({"message": f"Task's id={id} doesn't exist."}), 400
    else:
        db.session.delete(delete_task)
        db.session.commit()
        task_schema = TaskSchema()
        return task_schema.jsonify(delete_task), 200

@app.route('/skill/<id>', methods=['DELETE'])
def delete_skill(id):
    delete_skill = Skill.query.get(id)
    if not delete_skill:
        return jsonify({"message": f"Skill's id={id} doesn't exist."}), 400
    else:
        db.session.delete(delete_skill)
        db.session.commit()
        skill_schema = SkillSchema()
        return skill_schema.jsonify(delete_skill), 200

if __name__ == '__main__':
    app.run(debug=True)
