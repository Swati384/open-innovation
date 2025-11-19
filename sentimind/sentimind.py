#!/usr/bin/env python3
"""
SentiMind - AI-powered Sentiment Analyzer CLI Tool
Analyze the sentiment of text with beautiful, color-coded output.
"""

import click
from textblob import TextBlob
from colorama import Fore, Style, init
import os

# Initialize colorama for cross-platform color support
init(autoreset=True)

class SentimentAnalyzer:
    """Analyze sentiment of text using TextBlob."""
    
    def __init__(self):
        self.polarity_thresholds = {
            'very_positive': (0.5, 1.0),
            'positive': (0.1, 0.5),
            'neutral': (-0.1, 0.1),
            'negative': (-0.5, -0.1),
            'very_negative': (-1.0, -0.5)
        }
    
    def analyze(self, text):
        """Analyze sentiment of given text."""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        return {
            'text': text,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'sentiment': self._classify_sentiment(polarity)
        }
    
    def _classify_sentiment(self, polarity):
        """Classify sentiment based on polarity score."""
        for sentiment, (min_val, max_val) in self.polarity_thresholds.items():
            if min_val <= polarity <= max_val:
                return sentiment
        return 'neutral'
    
    def get_color(self, sentiment):
        """Return color for sentiment."""
        colors = {
            'very_positive': Fore.GREEN,
            'positive': Fore.LIGHTGREEN_EX,
            'neutral': Fore.YELLOW,
            'negative': Fore.LIGHTRED_EX,
            'very_negative': Fore.RED
        }
        return colors.get(sentiment, Fore.WHITE)

def format_result(analyzer, result):
    """Format and display analysis result with colors."""
    sentiment = result['sentiment']
    color = analyzer.get_color(sentiment)
    polarity = result['polarity']
    subjectivity = result['subjectivity']
    
    output = f"\n{Style.BRIGHT}Text:{Style.RESET_ALL} {result['text']}\n"
    output += f"Sentiment: {color}{sentiment.replace('_', ' ').upper()}{Style.RESET_ALL}\n"
    output += f"Polarity Score: {polarity:.2f} (range: -1.0 to 1.0)\n"
    output += f"Subjectivity Score: {subjectivity:.2f} (range: 0.0 to 1.0)\n"
    
    return output

@click.group()
def cli():
    """SentiMind - Sentiment Analysis CLI Tool"""
    pass

@cli.command()
@click.argument('text', required=False)
def analyze(text):
    """Analyze sentiment of provided text."""
    analyzer = SentimentAnalyzer()
    
    if not text:
        click.echo(f"{Fore.CYAN}Enter text to analyze (press Enter twice to finish):{Style.RESET_ALL}")
        lines = []
        while True:
            try:
                line = input()
                if line:
                    lines.append(line)
                else:
                    if lines:
                        break
                    else:
                        continue
            except EOFError:
                break
        
        if not lines:
            click.echo(f"{Fore.RED}No text provided!{Style.RESET_ALL}")
            return
        
        text = ' '.join(lines)
    
    result = analyzer.analyze(text)
    click.echo(format_result(analyzer, result))

@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
def analyze_file(filepath):
    """Analyze sentiment from a text file (one line per analysis)."""
    analyzer = SentimentAnalyzer()
    
    if not os.path.isfile(filepath):
        click.echo(f"{Fore.RED}File not found: {filepath}{Style.RESET_ALL}")
        return
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            click.echo(f"{Fore.RED}File is empty!{Style.RESET_ALL}")
            return
        
        click.echo(f"\n{Fore.CYAN}Analyzing {len(lines)} lines from {filepath}...{Style.RESET_ALL}\n")
        
        for i, line in enumerate(lines, 1):
            text = line.strip()
            if text:
                result = analyzer.analyze(text)
                click.echo(f"{Style.BRIGHT}[Line {i}]{Style.RESET_ALL}")
                click.echo(format_result(analyzer, result))
        
        click.echo(f"{Fore.GREEN}Analysis complete!{Style.RESET_ALL}\n")
    
    except Exception as e:
        click.echo(f"{Fore.RED}Error reading file: {e}{Style.RESET_ALL}")

@cli.command()
def interactive():
    """Launch interactive sentiment analyzer."""
    analyzer = SentimentAnalyzer()
    click.echo(f"\n{Fore.CYAN}{Style.BRIGHT}Welcome to SentiMind Interactive Mode!{Style.RESET_ALL}")
    click.echo(f"Type 'quit' or 'exit' to quit.\n")
    
    while True:
        try:
            text = click.prompt(f"{Fore.CYAN}Enter text{Style.RESET_ALL}")
            
            if text.lower() in ['quit', 'exit']:
                click.echo(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}\n")
                break
            
            if not text.strip():
                click.echo(f"{Fore.RED}Please enter some text.{Style.RESET_ALL}")
                continue
            
            result = analyzer.analyze(text)
            click.echo(format_result(analyzer, result))
        
        except KeyboardInterrupt:
            click.echo(f"\n{Fore.YELLOW}Exiting...{Style.RESET_ALL}\n")
            break

@cli.command()
def version():
    """Show version information."""
    click.echo(f"{Fore.CYAN}SentiMind v1.0.0{Style.RESET_ALL}")
    click.echo("AI-powered Sentiment Analysis CLI Tool")

if __name__ == '__main__':
    cli()
