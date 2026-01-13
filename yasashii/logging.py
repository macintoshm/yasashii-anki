"""Colorful logging module with Rich library support and emojis"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

class ColorfulLogger:
    """Custom logger with rich colors and emojis"""
    
    def __init__(self):
        self.console = Console()
    
    def info(self, message, emoji="ℹ️"):
        self.console.print(f"{emoji} [orchid2]{message}[/orchid2]")
    
    def success(self, message, emoji="✅"):
        self.console.print(f"{emoji} [green]{message}[/green]")
    
    def warning(self, message, emoji="⚠️"):
        self.console.print(f"{emoji} [yellow]{message}[/yellow]")
    
    def error(self, message, emoji="❌"):
        self.console.print(f"{emoji} [red]{message}[/red]")
    
    def header(self, title, emoji="🌸"):
        panel = Panel(
            Text(title, style="bold magenta"), 
            border_style="magenta",
            title=f"{emoji} Yasashii Anki {emoji}"
        )
        self.console.print(panel)
    
    def word_result(self, word_data, emoji="📚"):
        """Display a single word result beautifully"""
        if not word_data:
            return
            
        self.console.print(f"{emoji} [bold yellow]{word_data.get('word', 'Word')}[/bold yellow]")
        self.console.print(f"[bold cyan]Word:\t\t[/bold cyan][bold yellow]{word_data.get('word', 'N/A')}[/bold yellow]")
        self.console.print(f"[bold cyan]Reading:\t[/bold cyan][green]{', '.join(word_data.get('readings', []))}[/green]")
        self.console.print(f"[bold cyan]Meaning:\t[/bold cyan]")
        
        # Format the dictionary structure for display
        meanings_dict = word_data.get('meanings', {})
        if meanings_dict:
            sense_number = 1
            for sense_key, glosses in meanings_dict.items():
                glosses_str = ', '.join(glosses)
                # Extract part of speech from sense key (format: "sense1 v5k-s, vi")
                pos = sense_key.split(' ', 1)[1] if ' ' in sense_key else sense_key
                self.console.print(f"[pale_violet_red1]\t{sense_number}. [italic light_pink1]({pos})[/italic light_pink1] {glosses_str}[/pale_violet_red1]")
                sense_number += 1
        else:
            self.console.print(f"[blue]No meanings found[/blue]")
        
        if word_data.get('examples'):
            example = word_data['examples'][0]
            self.console.print(f"[bold cyan]Example:\t[/bold cyan][dim white]{example['sentences']['japanese']}[/dim white]")
            self.console.print(f"[bold cyan]Translation:\t[/bold cyan][dim cyan]{example['sentences']['english']}[/dim cyan]")
        
        self.console.print()


# Create global logger instance
logger = ColorfulLogger()
