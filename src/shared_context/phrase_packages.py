import yaml
from typing import List
from src.shared_context.types import PhrasePackage
from src.shared_context.learning_phrases import LearningPhrases
import csv

learning_phrases = LearningPhrases()


def load_config():
    with open("src/shared_context/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


def init_phrase_packages() -> List[PhrasePackage]:
    """
    Initialize the phrase_packages based on the loaded configuration.

    This function should be called to load config and ready do be used as a reference to load the packages when required.
    """
    config = load_config()
    phrase_packages = []
    for pp in config.get("phrase_packages", []):
        # Initialize each database connection here
        phrase_packages.append(
            PhrasePackage(
                id=pp.get("id"),
                name=pp.get("name"),
                description=pp.get("description"),
                goal_type=pp.get("goal_type", {}),
                source=pp.get("source", ""),
                path=pp.get("path", ""),
            )
        )
    if not phrase_packages:
        print("No phrase_package available. Please check your configuration.")
    return phrase_packages


def get_phrase_packages(language: str, level: str, context: str) -> List[PhrasePackage]:
    matching_packages = [
        pp
        for pp in phrase_packages
        if pp.goal_type.language.lower() == language.lower()
        and pp.goal_type.level.lower() == level.lower()
        and pp.goal_type.context.lower() == context.lower()
    ]
    return matching_packages


def add_a_package_to_learning_phrases(
    user_id: str, goal_id: str, phrase_package_id: str
):
    phrase_package = next(
        (pp for pp in phrase_packages if pp.id == phrase_package_id), None
    )
    if not phrase_package:
        raise ValueError(f"Phrase package with id '{phrase_package_id}' not found.")

    phrases = []
    with open(phrase_package.path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if "phrase" in row:
                phrases.append(row["phrase"])

    if not phrases:
        raise ValueError(f"No phrases found in CSV at '{phrase_package.path}'.")

    learning_phrases.add_to_learning_phrases(
        user_id,
        goal_id,
        phrases,
        source_id=phrase_package_id,
        source_type="phrase_package",
    )


phrase_packages = init_phrase_packages()
