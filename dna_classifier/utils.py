"""
DNA Sequence Utilities - Validation, Cleaning, and Processing.
"""
import re
import logging

logger = logging.getLogger(__name__)

VALID_DNA_CHARS = set('ATGC')
MIN_LENGTH = 10
MAX_LENGTH = 5000


def clean_sequence(sequence: str) -> str:
    """
    Clean a DNA sequence: strip whitespace, convert to uppercase,
    remove spaces and newlines.
    """
    cleaned = re.sub(r'\s+', '', sequence.strip().upper())
    return cleaned


def validate_sequence(sequence: str) -> tuple[bool, str]:
    """
    Validate a DNA sequence.

    Returns:
        (is_valid: bool, error_message: str)
    """
    if not sequence:
        return False, "DNA sequence cannot be empty."

    if len(sequence) < MIN_LENGTH:
        return False, f"Sequence too short. Minimum length is {MIN_LENGTH} characters."

    if len(sequence) > MAX_LENGTH:
        return False, f"Sequence too long. Maximum length is {MAX_LENGTH} characters."

    invalid_chars = set(sequence) - VALID_DNA_CHARS
    if invalid_chars:
        return False, (
            f"Invalid characters found: {', '.join(sorted(invalid_chars))}. "
            f"Only A, T, G, C are allowed."
        )

    return True, ""


def get_sequence_stats(sequence: str) -> dict:
    """
    Compute base composition statistics for a DNA sequence.
    """
    length = len(sequence)
    if length == 0:
        return {}

    counts = {base: sequence.count(base) for base in 'ATGC'}
    percentages = {base: round(count / length * 100, 2) for base, count in counts.items()}
    gc_content = round((counts['G'] + counts['C']) / length * 100, 2)

    return {
        'length': length,
        'counts': counts,
        'percentages': percentages,
        'gc_content': gc_content,
        'at_content': round(100 - gc_content, 2),
    }


def colorize_sequence_html(sequence: str) -> str:
    """
    Return HTML with each base colored differently.
    A=green, T=red, G=blue, C=yellow
    """
    color_map = {
        'A': '#22c55e',  # green
        'T': '#ef4444',  # red
        'G': '#3b82f6',  # blue
        'C': '#f59e0b',  # amber
    }
    html_parts = []
    for base in sequence:
        color = color_map.get(base, '#ffffff')
        html_parts.append(f'<span style="color:{color}" class="dna-base">{base}</span>')
    return ''.join(html_parts)
