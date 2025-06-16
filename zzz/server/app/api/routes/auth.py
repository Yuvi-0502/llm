from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.container import Container, get_container
from app.core.security import create_access_token
from app.dto.user import UserRegistrationDTO, UserResponseDTO, TokenResponseDTO

router = APIRouter()

@router.post("/login", response_model=TokenResponseDTO)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    container: Container = Depends(get_container)
):
    """Login endpoint."""
    user = container.user_service.authenticate_user(
        email=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return TokenResponseDTO(access_token=access_token, token_type="bearer")

@router.post("/signup", response_model=UserResponseDTO)
async def signup(
    user: UserRegistrationDTO,
    container: Container = Depends(get_container)
):
    """Signup endpoint."""
    db_user = container.user_service.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return container.user_service.create_user(user=user) 