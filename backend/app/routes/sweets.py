from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..schemas import SweetBase, SweetResponse, User as UserSchema
from ..models import Sweet as SweetModel
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[SweetResponse])
def get_sweets(db: Session = Depends(get_db)):
    """
    Retrieves a list of all sweets.
    """
    return db.query(SweetModel).all()

@router.post("/", response_model=SweetResponse, status_code=status.HTTP_201_CREATED)
def add_sweet(
    sweet: SweetBase, 
    db: Session = Depends(get_db), 
    current_user: UserSchema = Depends(get_current_user)
):
    """
    Adds a new sweet to the inventory (requires authentication).
    """
    # Check if the user has admin privileges
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can add sweets")
    
    new_sweet = SweetModel(**sweet.dict())
    db.add(new_sweet)
    db.commit()
    db.refresh(new_sweet)
    return new_sweet

@router.get("/search", response_model=List[SweetResponse])
def search_sweets(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(0.0),
    max_price: Optional[float] = Query(1000.0),
):
    """
    Searches for sweets by name, category, or price range.
    """
    query = db.query(SweetModel)
    if name:
        query = query.filter(SweetModel.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(SweetModel.category.ilike(f"%{category}%"))
    query = query.filter(SweetModel.price >= min_price, SweetModel.price <= max_price)
    
    return query.all()

@router.put("/{sweet_id}", response_model=SweetResponse)
def update_sweet(
    sweet_id: int,
    sweet: SweetBase,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """
    Updates a sweet's details (requires authentication).
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can update sweets")
        
    db_sweet = db.query(SweetModel).filter(SweetModel.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
        
    for key, value in sweet.dict(exclude_unset=True).items():
        setattr(db_sweet, key, value)
        
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

@router.delete("/{sweet_id}")
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """
    Deletes a sweet (requires authentication).
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete sweets")
        
    db_sweet = db.query(SweetModel).filter(SweetModel.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
        
    db.delete(db_sweet)
    db.commit()
    return {"message": "Sweet deleted successfully"}

# New endpoint to purchase a sweet
@router.post("/{sweet_id}/purchase", status_code=status.HTTP_200_OK)
def purchase_sweet(
    sweet_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserSchema = Depends(get_current_user)
):
    """
    Purchases a sweet, decreasing its quantity (requires authentication).
    """
    if current_user.role not in ["user", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication required to purchase sweets")

    db_sweet = db.query(SweetModel).filter(SweetModel.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    if db_sweet.quantity <= 0:
        raise HTTPException(status_code=400, detail="Sweet is out of stock")

    db_sweet.quantity -= 1
    db.commit()
    db.refresh(db_sweet)
    return {"message": "Purchase successful", "new_quantity": db_sweet.quantity}

# New endpoint to restock a sweet
@router.post("/{sweet_id}/restock", status_code=status.HTTP_200_OK)
def restock_sweet(
    sweet_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """
    Restocks a sweet, increasing its quantity (requires admin authentication).
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can restock sweets")

    db_sweet = db.query(SweetModel).filter(SweetModel.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    db_sweet.quantity += quantity
    db.commit()
    db.refresh(db_sweet)
    return {"message": "Restock successful", "new_quantity": db_sweet.quantity}
