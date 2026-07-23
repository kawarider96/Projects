from Project.Repositories.ProjectRepository import ProjectRepository

class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo
        self.rows = self.repo.get_all_project_data()

    def build_project_tree(self):
        projects = {}

        # Először minden projektet eltárolunk ID alapján
        for row in self.rows:
            row["children"] = []
            projects[row["id"]] = row

        roots = []

        # Utána összekötjük a szülőkkel
        for project in projects.values():
            parent_id = project["parent_id"]

            if parent_id is None:
                roots.append(project)
            else:
                parent = projects.get(parent_id)

                if parent is not None:
                    parent["children"].append(project)

        return roots
        