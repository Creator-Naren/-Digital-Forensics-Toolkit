import click
from rich.console import Console

console = Console()

@click.group()
def imaging():
    """Disk imaging commands using FTK Imager."""

@imaging.command()
@click.option("--case-id", required=True, help="Case ID")
@click.option("--evidence-id", required=True, help="Evidence ID")
@click.option("--source", required=True, type=click.Path(exists=True), help="Source disk path")
@click.option("--output", required=True, type=click.Path(), help="Output directory")
@click.option("--format", type=click.Choice(["E01", "RAW", "DD"]), default="E01")
def image(case_id, evidence_id, source, output, format):
    """Create a disk image."""
    from pathlib import Path
    from forensics_core.database import Database
    from forensics_core.models import ImageFormat
    from forensics_imaging.ftk_wrapper import FTKImagerCommand
    from forensics_imaging.command import ValidationError

    db = Database()
    cmd = FTKImagerCommand(
        source=Path(source),
        output_dir=Path(output),
        image_format=ImageFormat(format),
        case_id=case_id,
        evidence_id=evidence_id,
        db=db
    )

    try:
        with console.status("[bold green]Creating disk image..."):
            result = cmd.run()
    except ValidationError as e:
        console.print(f"[bold red]Validation failed: {e}")
        raise click.ClickException(str(e))

    if result["success"]:
        console.print("[bold green]Image created successfully!")
        console.print(f"Source hash: {result['source_hash']}")
        console.print(f"Output hash: {result['output_hash']}")
    else:
        raise click.ClickException(f"Image creation failed: {result.get('errors', ['Unknown error'])}")

@imaging.command()
@click.option("--case-id", required=True, help="Case ID")
@click.option("--evidence-id", required=True, help="Evidence ID")
def verify(case_id, evidence_id):
    """Verify image integrity."""
    console.print(f"Verifying evidence {evidence_id} for case {case_id}...")

@imaging.command(name="list")
@click.option("--case-id", required=True, help="Case ID")
def list_images(case_id):
    """List images in a case."""
    console.print(f"Listing images for case {case_id}...")
