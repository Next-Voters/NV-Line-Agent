"""UI Utility Module.

This module provides a dedicated UI class for handling consistent and beautiful 
terminal formatting using the `rich` library.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import print as rprint

console = Console()

class UI:
    """Utility class for terminal formatting."""
    
    @staticmethod
    def print_section_header(title: str):
        """Print a visually prominent section header."""
        console.print(Panel(Text(title, style="bold magenta"), border_style="magenta"))

    @staticmethod
    def print_status(message: str):
        """Print a status update message."""
        console.print(f"[cyan]➤[/cyan] [italic white]{message}[/italic white]")

    @staticmethod
    def print_research_brief(brief: str):
        """Print the research brief in a nice panel."""
        console.print(Panel(
            Text(brief, style="white"),
            title="[bold green]💼 Research Brief[/bold green]",
            border_style="green"
        ))

    @staticmethod
    def print_ai_question(question: str):
        """Print a question from the AI to the user."""
        console.print(f"[bold yellow]Agent:[/bold yellow] {question}")

    @staticmethod
    def print_research_topics(topics: list[str]):
        """Print research topics created by the supervisor."""
        console.print("\n[bold blue]Lead Researchers (Supervisors) has created the following research topics:[/bold blue]")
        table = Table(show_header=False, box=None, padding=(0, 1))
        for i, topic in enumerate(topics, 1):
            table.add_row(f"[bold blue]{i}.[/bold blue]", f"[white]{topic}[/white]")
        console.print(table)
        console.print("") # Add a newline for spacing

    @staticmethod
    def print_final_report(report: str):
        """Print the final research report."""
        console.print(Panel(
            Text(report, style="white"),
            title="[bold cyan]📊 Final Research Report[/bold cyan]",
            border_style="cyan"
        ))

    @staticmethod
    def print_error(message: str):
        """Print an error message."""
        console.print(f"[bold red]ERROR:[/bold red] {message}")