import os
import inflect
from flask.cli import with_appcontext
import click

p = inflect.engine()


@click.command("make:model")
@click.option("--model_name", prompt="Name of the model", help="Name of the model")
@with_appcontext
def make_model(model_name):
    model_name = model_name.strip()

    # -----------------------------
    # FORMAT NAMES
    # -----------------------------
    model_name_title = model_name.title()
    model_name_lower = model_name.lower()
    model_name_plural = p.plural(model_name_lower)

    # -----------------------------
    # PATHS
    # -----------------------------
    base_path = os.getcwd()

    model_stub_path = os.path.join(base_path, "app", "Stub", "Model.stub")
    controller_stub_path = os.path.join(base_path, "app", "Stub", "Controller.stub")

    model_output_path = os.path.join(base_path, "app", "Models", f"{model_name_title}.py")
    controller_output_path = os.path.join(base_path, "app", "Controller", f"{model_name_title}Controller.py")

    init_file_path = os.path.join(base_path, "app", "Models", "__init__.py")

    # -----------------------------
    # READ STUBS
    # -----------------------------
    with open(model_stub_path, "r") as f:
        model_stub = f.read()

    with open(controller_stub_path, "r") as f:
        controller_stub = f.read()

    # -----------------------------
    # REPLACE PLACEHOLDERS
    # -----------------------------
    replacements = {
        "{model_name_title}": model_name_title,
        "{model_name_lower}": model_name_lower,
        "{model_name_plural}": model_name_plural,
    }

    for key, value in replacements.items():
        model_stub = model_stub.replace(key, value)
        controller_stub = controller_stub.replace(key, value)

    # -----------------------------
    # CREATE FILES
    # -----------------------------
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(controller_output_path), exist_ok=True)

    with open(model_output_path, "w") as f:
        f.write(model_stub)

    with open(controller_output_path, "w") as f:
        f.write(controller_stub)

    click.echo(f"✅ Model created: {model_output_path}")
    click.echo(f"✅ Controller created: {controller_output_path}")

    # -----------------------------
    # AUTO IMPORT IN __init__.py
    # -----------------------------
    import_line = f"from .{model_name_title} import {model_name_title}\n"

    if not os.path.exists(init_file_path):
        with open(init_file_path, "w") as f:
            f.write(import_line)
    else:
        with open(init_file_path, "r") as f:
            content = f.read()

        if import_line not in content:
            with open(init_file_path, "a") as f:
                f.write(import_line)

    # -----------------------------
    # CREATE MIGRATION
    # -----------------------------
    try:
        migration_message = f"create_table_{model_name_lower}"

        os.system(f'flask db migrate -m "{migration_message}"')

        click.echo(f"✅ Migration created: {migration_message}")

    except Exception as e:
        click.echo("❌ Migration failed")
        click.echo(str(e))
