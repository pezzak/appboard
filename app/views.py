from app import app, db
from app.models import Environment, Project, Project_info
from app.exceptions import InvalidUsage
from flask import render_template, jsonify, request
from flask_httpauth import HTTPBasicAuth
from utils import get_or_create, datetimefilter
from flask import abort
from config import REPO_URL, REPO_PROJECT_NAMESPACE, APPS_PER_PAGE
from math import ceil
from flask import make_response
from config import apiusers
import datetime

auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
    if username in apiusers:
        return apiusers.get(username)
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.context_processor
def get_menu():
    res = dict()
    envs = Environment.query.all()
    for env in envs:
        if env.name not in res:
            if env.env_info:
                res[env.name] = [env.env_info]
            else:
                res[env.name] = None
        else:
            if env.env_info:
                res[env.name].append(env.env_info)
    return dict(menu=res)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/', defaults={'env': 'production', 'env_info': None})
@app.route('/<env>', defaults={'env_info': None})
@app.route('/<env>/<env_info>')
def index(env, env_info):
    mode = request.args.get('mode')
    history_page = 1 if not request.args.get('p') else int(request.args.get('p'))
    last_page = None
    menu = get_menu()['menu']
    if env not in menu:
        abort(404)
    if env_info and env_info not in menu[env]:
        abort(404)
    e = Environment.query.filter_by(name=env, env_info=env_info).first()
    projects = Project.query.filter_by(environment=e).all()
    projects_info = dict()
    if mode == 'history':
        project_ids = list()
        for project in projects:
            project_ids.append(project.id)
        projects_info = (Project_info.query
                                        .join(Project)
                                        .filter(Project_info.project_id.in_(project_ids))
                                        .order_by(Project_info.timestamp.desc())
                                        .paginate(history_page, APPS_PER_PAGE, False))
        last_page = int(ceil(projects_info.total / float(APPS_PER_PAGE)))
    else:
        for project in projects:
            projects_info[project.name] = Project_info.query.filter_by(id=project.current_version).first()
    return render_template("env_data.html",
                                             projects=projects,
                                             projects_info=projects_info,
                                             get_env=env,
                                             get_env_info=env_info,
                                             get_mode=mode,
                                             page=history_page,
                                             last_page=last_page)

@app.route('/api/env/project_info', methods=['POST'])
def project():
    if (
        not request.json or
        'project' not in request.json or
        'revision' not in request.json or
        'commit' not in request.json or
        'branch' not in request.json or
        'env' not in request.json or
        'deploy_user' not in request.json
        ):
            raise InvalidUsage('Invalid usage', status_code=400)

    build_name = None
    if 'build_name' in request.json:
        build_name = request.json['build_name']
    env_info = None
    if 'env_info' in request.json:
        env_info = request.json['env_info']

    e = get_or_create(db, Environment, name=request.json['env'], env_info=env_info)
    p = get_or_create(db, Project, name=request.json['project'], environment=e)

    instance = Project_info(revision=request.json['revision'],
                                            commit=request.json['commit'],
                                            branch=request.json['branch'],
                                            build_name=build_name,
                                            deploy_user=request.json['deploy_user'],
                                            timestamp=datetime.datetime.utcnow(),
                                            project=p)

    db.session.add(instance)
    db.session.commit()
    p.current_version = instance.id
    db.session.add(p)
    db.session.commit()

    return jsonify({'project_info': instance.id}), 201

@app.route('/api/env/build_info', methods=['POST'])
def build():
    if (
        not request.json or
        'project' not in request.json or
        'build_name' not in request.json or
        'env' not in request.json or
        'deploy_user' not in request.json
        ):
            raise InvalidUsage('Invalid usage', status_code=400)

    env_info = None
    if 'env_info' in request.json:
        env_info = request.json['env_info']

    e = get_or_create(db, Environment, name=request.json['env'], env_info=env_info)
    p = get_or_create(db, Project, name=request.json['project'], environment=e)

    instance = Project_info(build_name=request.json['build_name'],
                                            deploy_user=request.json['deploy_user'],
                                            timestamp=datetime.datetime.utcnow(),
                                            project=p)

    db.session.add(instance)
    db.session.commit()
    p.current_version = instance.id
    db.session.add(p)
    db.session.commit()

    return jsonify({'project_info': instance.id}), 201

@app.route('/api/get_build/<buildname>')
def get_build(buildname):
    build_info = (Project_info.query
                              .join(Project)
                              .join(Environment)
                              .filter(Project_info.build_name == buildname)
                              .filter(Project_info.revision != None).first())
    res = {}
    if build_info:
        res['environment'] = build_info.project.environment.name
        res['project_name'] = build_info.project.name
        res['revision'] = build_info.revision
        res['commit'] = build_info.commit
        res['branch'] = build_info.branch
        res['build_name'] = build_info.build_name
        res['deploy_user'] = build_info.deploy_user
        res['date'] = datetimefilter(build_info.timestamp)
    else:
        res['error'] = "build not found", 404
    return jsonify(res)

@app.route('/api/get_repo_url/<project>')
def get_repo_url(project):
    res = {}
    if project in REPO_PROJECT_NAMESPACE:
        res['url'] =  REPO_URL + '/' + REPO_PROJECT_NAMESPACE[project]
        return jsonify(res)
    else:
        res['error'] = "project not found"
        return jsonify(res), 404
