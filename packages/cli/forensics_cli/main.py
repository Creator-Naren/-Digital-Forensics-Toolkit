import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Forensic Toolkit - Digital evidence collection and analysis."""


@cli.group()
def case():
    """Case management commands."""


@case.command()
@click.option("--name", required=True, help="Case name")
@click.option("--investigator", help="Investigator name")
def create(name, investigator):
    """Create a new case."""
    from forensics_core.database import Database
    from forensics_core.models import Case
    import uuid

    try:
        db = Database()
        case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
        new_case = Case(id=case_id, name=name, investigator=investigator)
        db.create_case(new_case)
        console.print(f"[green]Created case: {case_id}")
    except Exception as e:
        console.print(f"[red]Failed to create case: {e}")
        raise click.ClickException(str(e))


@case.command(name="list")
def list_cases():
    """List all cases."""
    from forensics_core.database import Database

    db = Database()
    cases = db.list_cases()
    table = Table(title="Cases")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Investigator")
    table.add_column("Status")
    for c in cases:
        table.add_row(c.id, c.name, c.investigator or "-", c.status)
    console.print(table)


@cli.group()
def imaging():
    """Disk imaging commands."""


from forensics_imaging.cli import image, verify, list_images

imaging.add_command(image, "image")
imaging.add_command(verify, "verify")
imaging.add_command(list_images, "list")
