from fastapi import APIRouter
from Global.Dependencies import project_controller
from Domains.Project.DTOs.ProjectCreateDTO import ProjectCreateDTO
from Domains.Project.DTOs.ProjectResponseDTO import ProjectResponseDTO
from Domains.Project.DTOs.ProjectUpdateDTO import ProjectUpdateDTO

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Project Manager API is running."
    }


@router.get("/projects", response_model=list[ProjectResponseDTO])
def list_all_projects():
    return project_controller.get_all_project()