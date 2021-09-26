from invoke import task


@task
def migration(c, name):
    """Create a migration alembic migration."""
    source_cmd = 'source venv/bin/activate'
    migration_command = f"alembic revision -m {name}"

    c.run(source_cmd)
    result = c.run(migration_command)
    print(result.stdout.splitlines())


@task
def migrate(c):
    """Run Alembic migrations."""
    cmd = 'alembic upgrade head'
    result = c.run(cmd)
    print(result.stdout.splitlines())


@task
def rollback(c, version):
    """Rollback migrations to either the last migration or to the version specified."""

    cmd = f"alembic downgrade {version}"
    result = c.run(cmd)
    print(result.stdout.splitlines())


@task
def history(c):
    """Get history of alembic versions."""
    cmd = 'alembic history'
    result = c.run(cmd)
    print(result.stdout.splitlines())

@task
def freeze(c):
    """Freeze pip requirements."""
    cmd = 'pip freeze > requirements.txt'
    result = c.run(cmd)
    print(result.stdout.splitlines())
