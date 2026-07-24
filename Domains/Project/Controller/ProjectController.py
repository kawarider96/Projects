from Domains.Project.Services.ProjectService import ProjectService

class ProjectController:
    def __init__(self, service: ProjectService):
        self.service = service

    def get_all_project(self):
        return self.service.build_project_tree()