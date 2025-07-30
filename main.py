from flask import Flask, render_template
import yaml
from yaml import Loader, Dumper

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html", recipe_cards=recipe_cards())


@app.route("/recipes/<recipe>")
def recipe(recipe):
    recipe_yml = load_recipe_from_filename(recipe)
    return render_template("recipe.html", recipe=recipe_yml)


def recipe_cards() -> str:
    return [
        load_recipe_from_filename("sushi"),
        load_recipe_from_filename("sushi"),
        load_recipe_from_filename("sushi"),
        load_recipe_from_filename("sushi"),
        load_recipe_from_filename("sushi"),
        load_recipe_from_filename("sushi"),
        load_recipe_from_filename("sushi"),
        load_recipe_from_filename("sushi"),
    ]


def load_recipe_from_filename(filename: str) -> dict:
    with open(f"recipes/{filename}.yml", "r") as f:
        data = yaml.load(f.read(), Loader=Loader)
        data["filename"] = filename
        return data


if __name__ == "__main__":
    app.run(debug=True)
