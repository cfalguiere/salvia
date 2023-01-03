"""This module contains helper functions to create reports.
"""
import json
import logging


class BaseReport:
    """This class is an abstract class used as a base class for other reports."""

    def __init__(self):
        # instance variable unique to each instance
        # self.name = name

        # initializations
        pass

    def generate_report(self):
        pass

    def write_json_report(self, filepath: str, json_report: dict) -> None:
        """Writes down the dict onto the local file system.

        Parameters
        ----------
        filepath: str
            The name of the file to be created.
        json_report: dict
            The associative array created by create_combined_json_report.
        """
        logging.info(f"writing json report file to {filepath}")
        with open(filepath, "w") as f:
            json.dump(json_report, f, default=str)

    def load_json_report(self, filepath: str) -> dict:
        """Loads the JSON report into a dict.

        Parameters
        ----------
        filepath: str
            The name of the file to be loaded.
        json_report: dict
            The associative array created by create_combined_json_report.

        Returns
        -------
        dict
            the json document.
        """
        logging.info("loading json data from {filepath}")
        try:
            with open(filepath) as json_data:
                data = json.load(json_data)
            return data
        except FileNotFoundError as exc:
            raise ValueError(
                f"Could not load data from file {filepath} - reason: {exc}"
            )

    def write_markdown_report(self, filepath: str, content: str) -> None:
        """Writes down the Markdown content onto the local file system.

        Parameters
        ----------
        filepath: str
            The name of the file to be created.
        content: str
            The markdown content to be written
        """
        logging.info(f"writing markdown report file to {filepath}")
        with open(filepath, mode="w", encoding="utf-8") as report:
            report.write(content)
