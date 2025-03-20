from fastapi import APIRouter, Depends, HTTPException
from ..services.auth import get_current_user, get_current_admin_user
from ..models.user import User
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectOut
from tortoise.expressions import Q

router = APIRouter(tags=["Projects"])


@router.post("/projects", response_model=ProjectOut)
async def create_project(
        project: ProjectCreate,
        user: User = Depends(get_current_user)
):
    if await user.projects.count() >= 5:
        raise HTTPException(
            status_code=400,
            detail="Maximum 5 projects allowed"
        )
    return await create_user_project(user, project.name)


@router.get("/me/projects", response_model=list[ProjectOut])
async def read_own_projects(
        user: User = Depends(get_current_user),
        page: int = 1,
        page_size: int = 10
):
    return await ProjectOut.from_queryset(
        user.projects.all()
        .offset((page - 1) * page_size)
        .limit(page_size)
    )


@router.get("/admin/all-projects", response_model=list[ProjectOut])
async def get_all_projects(
        admin: User = Depends(get_current_admin_user),
        search: str = None
):
    query = Project.all().prefetch_related("user")
    if search:
        query = query.filter(Q(name__icontains=search))
    return await ProjectOut.from_queryset(query)
