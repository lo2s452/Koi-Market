import argparse
import asyncio
import getpass

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.db import SessionLocal, engine, init_db
from app.models import Role, User
from app.schemas import Credentials
from app.security import hash_password


async def create_admin(username: str) -> None:
    password = getpass.getpass("Password: ")
    if getpass.getpass("Repeat password: ") != password:
        raise SystemExit("passwords do not match")
    try:
        creds = Credentials(username=username, password=password)
    except ValidationError as e:
        raise SystemExit(str(e))

    await init_db()
    try:
        async with SessionLocal() as db:
            db.add(
                User(
                    username=creds.username,
                    password_hash=await hash_password(creds.password),
                    role=Role.admin,
                )
            )
            await db.commit()
    except IntegrityError:
        raise SystemExit(f"user {username!r} already exists")
    finally:
        await engine.dispose()
    print(f"admin {username!r} created")


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("create-admin").add_argument("username")
    args = parser.parse_args()
    asyncio.run(create_admin(args.username))


if __name__ == "__main__":
    main()
