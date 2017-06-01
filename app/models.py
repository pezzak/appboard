from app import db

class Environment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), index = True)
    env_info = db.Column(db.String(128), index = True)
    projects = db.relationship('Project', backref='environment', lazy='dynamic')

    def __repr__(self):
        if self.env_info:
            return '<Environment %r[%r]>' % (self.name,self.env_info)
        else:
            return '<Environment %r>' % (self.name)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140))
    current_version = db.Column(db.Integer)
    env_id = db.Column(db.Integer, db.ForeignKey('environment.id'))
    project_info = db.relationship('Project_info', backref='project', lazy='dynamic')

    def __repr__(self):
        return '<Project %r>' % (self.name)

class Project_info(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime)
    revision = db.Column(db.String(100))
    commit = db.Column(db.String(100))
    branch = db.Column(db.String(100))
    build_name = db.Column(db.String(100))
    deploy_user = db.Column(db.String(100))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return '<Project %r>' % (self.project_id)
