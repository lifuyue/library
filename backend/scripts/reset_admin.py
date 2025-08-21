"""Utility script to (re)create or update the default admin user.

Usage (from project root):

  python -m backend.scripts.reset_admin \
      --username admin --email admin@example.com --password newpass123 --force

If --force is provided and the admin user exists, password/email & flags will be updated.
If no admin (is_admin=1) exists, a new one will be created regardless of --force.
Environment variable fallbacks:
  ADMIN_DEFAULT_USERNAME, ADMIN_DEFAULT_EMAIL, ADMIN_DEFAULT_PASSWORD
"""
from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path

# Ensure project root & backend on sys.path when executed from repo root
CURRENT_FILE = Path(__file__).resolve()
BACKEND_DIR = CURRENT_FILE.parents[1]
PROJECT_ROOT = BACKEND_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.database import SessionLocal

def ensure_admin(username: str, email: str, password: str, force: bool=False):
    from app.core.auth import get_password_hash  # local to avoid early import issues
    from app.models import models
    with SessionLocal() as session:
        admin = session.query(models.User).filter(models.User.username == username).first()
        any_admin = session.query(models.User).filter(models.User.is_admin == True).first()
        if not any_admin and not admin:
            # create new admin
            print(f"[reset_admin] No admin found, creating new admin '{username}'")
            hashed = get_password_hash(password)
            user = models.User(username=username, email=email, hashed_password=hashed, is_active=True, is_admin=True)
            session.add(user)
            session.commit()
            print("[reset_admin] Admin created.")
            return
        if admin:
            if force:
                print(f"[reset_admin] Updating existing admin '{username}' (force mode)")
                admin.email = email
                admin.hashed_password = get_password_hash(password)
                admin.is_active = True
                admin.is_admin = True
                session.commit()
                print("[reset_admin] Admin updated.")
            else:
                print(f"[reset_admin] Admin '{username}' already exists. Use --force to update.")
        else:
            if force or not any_admin:
                print(f"[reset_admin] Creating admin '{username}' (no user with that username)")
                hashed = get_password_hash(password)
                user = models.User(username=username, email=email, hashed_password=hashed, is_active=True, is_admin=True)
                session.add(user)
                session.commit()
                print("[reset_admin] Admin created.")
            else:
                print("[reset_admin] Another admin already exists; not creating new one. Use --force with that username to update it.")

def parse_args():
    p = argparse.ArgumentParser(description="Create or reset an admin user")
    p.add_argument('--username', default=os.getenv('ADMIN_DEFAULT_USERNAME', 'admin'))
    p.add_argument('--email', default=os.getenv('ADMIN_DEFAULT_EMAIL', 'admin@example.com'))
    p.add_argument('--password', default=os.getenv('ADMIN_DEFAULT_PASSWORD', 'admin123'))
    p.add_argument('--force', action='store_true', help='Update existing admin if present')
    return p.parse_args()

if __name__ == '__main__':
    args = parse_args()
    ensure_admin(args.username, args.email, args.password, args.force)
