import yaml
from yaml import Loader, Dumper
import os


def main():
    recipe_name_list = get_recipe_name_list()

    with open("index.html", "w+") as f:
        f.write(generate_index(recipe_name_list))

    try:
        os.mkdir("r")
    except FileExistsError:
        pass

    for recipe_name in recipe_name_list:
        with open(f"r/{recipe_name}.html", "w+") as f:
            f.write(generate_recipe_html(recipe_name))


def get_recipe_name_list() -> list[str]:
    return [name.split(".")[0] for name in os.listdir("recipes")]


def generate_recipe_html(name: str) -> str:
    recipe_yml = load_recipe_yml_from_filename(name)

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


def generate_index(recipe_names: list[str]) -> str:
    html = load_template("index")
    html = html.replace(
        "{{ RECIPE_CARDS }}",
        "\n".join(
            [
                generate_recipe_card(load_recipe_yml_from_filename(recipe_name))
                for recipe_name in recipe_names
            ]
        ),
    )
    return html


def generate_recipe_card(recipe_yml: dict) -> str:
    html = load_template("recipe_card")
    html = html.replace("{{ FILENAME }}", f"{recipe_yml["filename"]}.html")
    html = html.replace("{{ CARD_TITLE }}", recipe_yml["Title"])
    html = html.replace("{{ IMAGE }}", f"images/{recipe_yml["Image"]}")
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
