from Database.database import Database

from Domains.Project.Repositories.ProjectRepository import ProjectRepository
from Domains.Project.Services.ProjectService import ProjectService
from Domains.Project.Controller.ProjectController import ProjectController
from Domains.Task.Repositories.TaskRepository import TaskRepository


db = Database()

project_repository = ProjectRepository(db)
task_repository = TaskRepository(db)

project_service = ProjectService(
    project_repository,
    task_repository
)

project_controller = ProjectController(
    project_service
)