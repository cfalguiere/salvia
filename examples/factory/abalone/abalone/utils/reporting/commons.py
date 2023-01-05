"""This module contains helper functions to create reports."""
import json
import logging
from typing import Any, Dict, NewType

ReportContent = NewType("ReportContent", Dict[str, Any])
MarkDownContent = NewType("MarkDownContent", str)


class BaseReport:
    """This class is an abstract class used as a base class for other reports."""

    def __init__(self) -> None:
        """Initialize a report instance."""
        pass

    def write_json_report(self, filepath: str, json_report: ReportContent) -> None:
        """Write down the dict onto the local file system.

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
        """Load the JSON report into a dict.

        Parameters
        ----------
        filepath: str
            The name of the file to be loaded.

        Raises
        ------
        ValueError
            if could not load the file.

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
            raise ValueError(f"Could not load data from file {filepath} - reason: {exc}") from exc

    def write_markdown_report(self, filepath: str, content: MarkDownContent) -> None:
        """Write down the Markdown content onto the local file system.

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
