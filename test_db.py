from app.database import SessionLocal
from app.models import User
import uuid

# Create a session
db = SessionLocal()

# Create a test user
test_user = User(
    id=uuid.uuid4(),
    email="test@example.com",
    hashed_password="fake_hash_123",
    first_name="John",
    last_name="Doe"
)

# Add to database
db.add(test_user)
db.commit()
db.refresh(test_user)

print(f"✅ User created with ID: {test_user.id}")
print(f"✅ Email: {test_user.email}")
print(f"✅ Created at: {test_user.created_at}")

# Clean up
db.delete(test_user)
db.commit()
db.close()

print("✅ Test passed! Database is working.")