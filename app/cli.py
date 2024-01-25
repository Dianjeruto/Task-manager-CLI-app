import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Project, Task

engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('username')
def add_user(username):
    session = Session()
    user = User(username=username)
    session.add(user)
    session.commit()
    print(f'User "{username}" added successfully.')

@cli.command()
@click.argument('username')
def list_projects(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user:
        projects = user.projects
        for project in projects:
            print(f'Project ID: {project.id}, Name: {project.name}')
    else:
        print(f'User "{username}" not found.')

@cli.command()
@click.argument('username')
@click.argument('project_name')
def add_project(username, project_name):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user:
        project = Project(name=project_name, user=user)
        session.add(project)
        session.commit()
        print(f'Project "{project_name}" added successfully.')
    else:
        print(f'User "{username}" not found.')

@cli.command()
@click.argument('project_id', type=int)
@click.argument('task_description')
def add_task(project_id, task_description):
    session = Session()
    project = session.query(Project).filter_by(id=project_id).first()
    if project:
        task = Task(description=task_description, project=project)
        session.add(task)
        session.commit()
        print(f'Task "{task_description}" added to project "{project.name}" successfully.')
    else:
        print(f'Project with ID {project_id} not found.')

if __name__ == '__main__':
    cli()
