from ..extensions import db
from ..models.user import User

def ensure_admin():
    """
    Create default admin if not present. Admin credentials are printed on first run.
    """
    if User.query.filter_by(role="admin").first():
        return
    admin_username = "admin"
    admin_email = "admin@example.com"
    admin_password = "Admin@123"  # change in production through environment or override logic

    admin = User(username=admin_username, email=admin_email, role="admin")
    admin.set_password(admin_password)
    db.session.add(admin)
    db.session.commit()
    print(f"Created default admin -> username: {admin_username} password: {admin_password}")
