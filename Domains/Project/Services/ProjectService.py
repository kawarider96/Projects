from Domains.Project.Models.Project import Project
from Domains.Project.Repositories.ProjectRepository import ProjectRepository

from Domains.Task.Models.Task import Task
from Domains.Task.Repositories.TaskRepository import TaskRepository


class ProjectService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        task_repo: TaskRepository
    ):
        self.project_repo = project_repo
        self.task_repo = task_repo

    def build_project_tree(self) -> list[Project]:
        project_rows = self.project_repo.get_all_project_data()
        task_rows = self.task_repo.get_all_tasks()

        projects: dict[int, Project] = {}

        # 1. Project modellek létrehozása
        for row in project_rows:
            project = Project(
                id=row["id"],
                parent_id=row["parent_id"],
                name=row["name"],
                description=row["description"],
                start_date=row["start_date"],
                end_date=row["end_date"],
                level=row["level"]
            )

            projects[project.id] = project

        # 2. Task modellek létrehozása
        # és hozzárendelése a megfelelő projecthez
        for row in task_rows:
            task = Task(
                id=row["id"],
                project_id=row["project_id"],
                name=row["name"],
                description=row["description"],
                start_date=row["start_date"],
                end_date=row["end_date"]
            )

            project = projects.get(task.project_id)

            if project is not None:
                project.tasks.append(task)

        roots: list[Project] = []

        # 3. Project hierarchia felépítése
        for project in projects.values():
            if project.parent_id is None:
                roots.append(project)
                continue

            parent = projects.get(project.parent_id)

            if parent is not None:
                parent.children.append(project)

        return roots