import typer
from .commands.migrate import app as migrate_app
from .commands.scan import app as scan_app
from .commands.docs import app as docs_app
from .commands.health import app as health_app
from .commands.review import app as review_app

app = typer.Typer()

app.add_typer(migrate_app, name="migrate")
app.add_typer(scan_app, name="scan")
app.add_typer(docs_app, name="docs")
app.add_typer(health_app, name="health")
app.add_typer(review_app, name="review")

if __name__ == "__main__":
    app()