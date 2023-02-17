"""Console script for opencdms."""
import pathlib
import sys
import click
import yaml

@click.group()
def main(args=None):
    """Console script for opencdms."""
    # See click documentation at https://click.palletsprojects.com/
    pass


@click.command(name="relocate-schema")
@click.argument("filepath")
@click.argument("resource")
def relocate_schema(filepath, resource):
    """
    Relocates local definitions to the document root of OpenAPI config file
    """
    if not pathlib.Path(filepath).exists():
        click.echo("OpenAPI config file does not exist.", err=True)
        return

    with open(filepath, "r") as stream:
        openapi_config = yaml.load(stream, yaml.Loader)
        root_definitions = openapi_config.get("definitions", {})
        path_config = openapi_config.get("paths", {}).get(
            f"/collections/{resource}/items/{{featureId}}"
        )
        put_request_definitions = (
            path_config.get("put", {})
            .get("requestBody", {})
            .get("content", {})
            .get("application/json", {})
            .get("schema", {})
            .get("definitions", {})
        )
        get_responses_definitions = (
            path_config.get("get", {})
            .get("responses", {})
            .get("200", {})
            .get("content", {})
            .get("application/json", {})
            .get("schema", {})
            .get("definitions", {})
        )
        openapi_config["definitions"] = {
            **root_definitions,
            **put_request_definitions,
            **get_responses_definitions,
        }

    with open(filepath, "w") as stream:
        yaml.dump(openapi_config, stream)


main.add_command(relocate_schema)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
