import yaml
from yaml import Loader, Dumper
import os


def main():
    with open("index.html", "w+") as f:
        f.write(generate_index())

    try:
        os.mkdir("r")
    except FileExistsError:
        pass

    with open("r/sushi.html", "w+") as f:
        f.write(generate_recipe_html())


def generate_recipe_html() -> str:
    recipe_yml = load_recipe_yml_from_filename("sushi")

    html = load_template("recipe")
    html = html.replace("{{ RECIPE_TITLE }}", recipe_yml["Title"])
    html = html.replace("{{ RECIPE_DESCRIPTION }}", recipe_yml["Description"])

    html = html.replace(
        "{{ INGREDIENTS }}", generate_li_from_list(recipe_yml["Ingredients"])
    )
    html = html.replace(
        "{{ INSTRUCTIONS }}", generate_li_from_list(recipe_yml["Instructions"])
    )

    return html


def generate_li_from_list(items: list[str]) -> str:
    return "\n".join([f"<li>{d}</li>" for d in items])


def generate_index() -> str:
    html = load_template("index")
    html = html.replace(
        "{{ RECIPE_CARDS }}",
        generate_recipe_card(load_recipe_yml_from_filename("sushi")),
    )
    return html


def generate_recipe_card(recipe_yml: dict) -> str:
    html = load_template("recipe_card")
    html = html.replace("{{ FILENAME }}", f"{recipe_yml["filename"]}.html")
    html = html.replace("{{ CARD_TITLE }}", recipe_yml["Title"])
    html = html.replace("{{ CARD_DESCRIPTION }}", recipe_yml["Description"])
    return html


def load_template(name: str) -> str:
    with open(f"templates/{name}.html") as f:
        return f.read()


def load_recipe_yml_from_filename(filename: str) -> dict:
    with open(f"recipes/{filename}.yml", "r") as f:
        data = yaml.load(f.read(), Loader=Loader)
        data["filename"] = filename
        return data


if __name__ == "__main__":
    main()
