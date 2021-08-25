from app import app,db
from flask import request, jsonify
from app.models import TaskSkills, User, Task, Skill
from app.models_schema import TaskSchema, SkillSchema, TaskSkillsSchema, UserSchema

@app.route('/')
@app.route('/home')
def home():
    return 'Hello, This is our home page!!'
#########################   POST_Method  #########################
@app.route('/user', methods=['POST'])
def create_user():
    name = request.json['name']
    email = request.json['email']
    check_name = User.query.filter_by(name=name).first()
    check_email = User.query.filter_by(email=email).first()
    if check_email is None and check_name is None:
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
    check_name = Task.query.filter_by(name=name).first()    
    check_objective = Task.query.filter_by(objective=objective).first()
    if check_name is None and check_objective is None:   
        skill_obj_list = request.json.get('skill') #get list object from json form of skill
        list_of_skill_id = [obj['id'] for obj in skill_obj_list]
        new_task= Task(name, objective, user_id)
        # To add skills to Model Task
        for skill_id in list_of_skill_id:
            skill = Skill.query.get(skill_id)
            new_task.skills.append(skill)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task is created.'}), 200
    else:
        return jsonify({"message": "Task is already existed."}), 400

@app.route('/skill', methods=['POST'])  
def create_skill():
    name = request.json['name']
    code = request.json['code']
    check_name = Skill.query.filter_by(name=name).first()
    check_code = Skill.query.filter_by(code=code).first()
    if check_code is None and check_name is None:
        task_obj_list = request.json.get('tasks')
        list_of_task_id = [obj['id'] for obj in task_obj_list]
        new_skill= Skill(name, code)
        # To add tasks to Model Skill
        for task_id in list_of_task_id:
            task = Task.query.get(task_id)
            new_skill.tasks.append(task)
        db.session.add(new_skill)
        db.session.commit()
        return jsonify({'message': 'Skill is created.'}), 200
    else:
        return jsonify({"message": "Skill is already existed."}),400


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
    if user:
        user_schema = UserSchema()
        return user_schema.jsonify(user), 200
    else:
        return jsonify({"message": f"User's  id={id} doesn't exit."}),400

@app.route('/user/<id>/task', methods=['GET'])
def all_task_in_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": f"User's id={id} doesn't exist."}), 400
    else:
        # tasks = []
        # for task in Task.query.filter_by(user_id=id):
        #     tasks.append(task.name)
        # return jsonify(tasks), 200
        task = Task.query.filter_by(user_id=id).all()
        tasks = TaskSchema(many=True, only=('id', 'name', 'objective','user')).dump(task)
        return jsonify({f"Tasks with User's id={id}": tasks}), 200

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
    if task:
        task_schema = TaskSchema()
        return task_schema.jsonify(task), 200
    else:
        return jsonify({"message": f"Task's id={id} doesn't exit."}),400

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
    if skill:
        skill_schema = SkillSchema()
        return skill_schema.jsonify(skill), 200
    else:
        return jsonify({"message": f"Skill's id={id} doesn't exit."}),400

@app.route('/skill/<id>/task', methods=['GET'])
def all_task_have_skill(id):
    skill = Skill.query.get(id)
    if skill:
        task_have_skill = Task.query.join(Skill.tasks).filter(Skill.id==id).all()
        tasks = TaskSchema(many=True, only=('name', 'id', 'skills')).dump(task_have_skill)
        return jsonify({f"Task have skill id={id}": tasks}), 200
    else:
        return jsonify({"message": f"Skill's id={id} doesn't exist."}), 400

##########################   PUT_Method   ##############################
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    update_user = User.query.get(id)
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
    skill_obj_list = request.json.get('skills') #get list object from json form of skill
    list_of_skill_id = [obj['id'] for obj in skill_obj_list]
    # To add skills to model Task
    for skill_id in list_of_skill_id:
        skill = Skill.query.get(skill_id)
        update_task.skills.append(skill)
    update_task.name = name
    update_task.objective = objective
    update_task.user_id = user_id
    db.session.commit()
    task_schema = TaskSchema()
    return task_schema.jsonify(update_task), 200

@app.route('/skill/<id>', methods=['PUT'])
def update_skill(id):
    update_skill = Skill.query.get(id)
    name = request.json['name']
    code = request.json['code']
    task_obj_list = request.json.get('tasks')  #get list off task obj
    list_of_task_id = [obj['id'] for obj in task_obj_list]
    # To add tasks to Model Skill
    for task_id in list_of_task_id:
        task = Task.query.get(task_id)
        update_skill.tasks.append(task)
    update_skill.name = name
    update_skill.code = code
    db.session.commit()
    skill_schema = SkillSchema()
    return skill_schema.jsonify(update_skill), 200


##########################   DELETE_Method   ##############################
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    delete_user = User.query.get(id)
    if not delete_user:
        return jsonify({"message": f"User's id={id} doesn't exist."}), 400
    else:
        db.session.delete(delete_user)
        db.session.commit()
        return jsonify({"message": "User is deleted."}), 200

@app.route('/task/<id>', methods=['DELETE'])
def delete_task(id):
    delete_task = Task.query.get(id)
    if not delete_task:
        return jsonify({"message": f"Task's id={id} doesn't exist."}), 400
    else:
        db.session.delete(delete_task)
        db.session.commit()
        return jsonify({"message": "Task is deleted."}), 200

@app.route('/skill/<id>', methods=['DELETE'])
def delete_skill(id):
    delete_skill = Skill.query.get(id)
    if not delete_skill:
        return jsonify({"message": f"Skill's id={id} doesn't exist."}), 400
    else:
        db.session.delete(delete_skill)
        db.session.commit()
        return jsonify({"message": "Skill is deleted."}), 200


#################################   Skill_Status   ####################################
@app.route('/status/skill/primary', methods=['GET'])
def get_all_skill_status_primary():
    task_skill = TaskSkills.query.filter_by(skill_status='primary').all()
    skills_status = TaskSkillsSchema(many=True).dump(task_skill)
    return jsonify(skills_status), 200

@app.route('/status/skill/secondary', methods=['GET'])
def get_all_skill_status_secondary():
    task_skill = TaskSkills.query.filter_by(skill_status='secondary').all()
    skills_status = TaskSkillsSchema(many=True).dump(task_skill)
    return jsonify(skills_status), 200

@app.route('/status/skill/<id>', methods=['GET'])
def get_single_skill_status(id):
    skill_status = TaskSkills.query.filter_by(skill_id=id).first()
    return TaskSkillsSchema(many=False, exclude=('skill', 'task')).jsonify(skill_status), 200

@app.route('/status/skill/<id>/update', methods=['PUT'])
def update_status_skill(id):
    skill_status_update = TaskSkills.query.filter_by(skill_id=id).all()
    check_skill_id = Skill.query.get(id)
    if check_skill_id:
        for i in skill_status_update:
            if i.skill_status == 'secondary':
                i.skill_status = "primary"
                # db.session.commit()
            elif i.skill_status == 'primary':
                i.skill_status = 'secondary'
                # db.session.commit()
            else:
                return jsonify({"message": f"{i.skill_status} doesn't exist."}), 400
        db.session.commit()
        return jsonify('Alter skill_status is successful.'), 200
    else:
        return jsonify({"message": f"Skill's id={id} doesn't exist."}), 400

@app.route('/task<int:task_id>/change_skill_status<int:skill_id>', methods=['PUT'])
def update_skill_status_in_task(task_id, skill_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return jsonify({"message": f"Task's id={task_id} doesn't exist."}), 400
    status = TaskSkills.query.filter_by(skill_id = skill_id, task_id=task_id).first()
    if status is None:
        return jsonify({"message": f"Task's id={task_id} doesn't skill's id={skill_id}"}), 400

    if status.skill_status == "primary":
        status.skill_status = 'secondary'
        # db.session.commit()
        return jsonify({"message": f"Successfully alter the skill's id={skill_id} status to secondary."}), 200
    elif status.skill_status == 'secondary':
        status.skill_status = "primary"
        # db.session.commit()
        return jsonify({"message": f"Successfully alter the skill's id={skill_id} status to primary."}), 200
    db.session.commit()
    
@app.route('/status/skill', methods=['GET'])
def status():
    status = request.json['status']
    if status == '1':
        task_skill = TaskSkills.query.filter_by(skill_status='secondary').all()
        skills_status = TaskSkillsSchema(many=True).dump(task_skill)
        return jsonify(skills_status), 200
    elif status == '2':
        task_skill = TaskSkills.query.filter_by(skill_status='primary').all()
        skills_status = TaskSkillsSchema(many=True).dump(task_skill)
        return jsonify(skills_status), 200