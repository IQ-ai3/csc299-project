import json
import os
import click

# File to store names
DATA_FILE = "names.json"

# Ensure the JSON file exists
def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

# Add a name to the JSON file
@click.command()
@click.argument("name")
def add(name):
    "Add a name to the storage."
    ensure_data_file()
    with open(DATA_FILE, "r") as f:
        names = json.load(f)
    names.append(name)
    names = sorted(names, key=lambda x: x.lower())  # Sort names alphabetically, case insensitive
    with open(DATA_FILE, "w") as f:
        json.dump(names, f)
    click.echo(f"Added: {name}")

# List all names in the JSON file
@click.command()
def list_names():
    "List all stored names."
    ensure_data_file()
    with open(DATA_FILE, "r") as f:
        names = json.load(f)
    if names:
        click.echo("\n".join(names))
    else:
        click.echo("No names found.")

# Main CLI group
@click.group()
def cli():
    pass

cli.add_command(add)
cli.add_command(list_names)

if __name__ == "__main__":
    cli()
