"""Core formatting logic for CJK-ASCII spacing."""

import re


def is_cjk_char(char: str) -> bool:
    """Check if a character is a CJK character.

    Args:
        char: Single character to check.

    Returns:
        True if character is CJK (Chinese, Japanese, Korean).

    Examples:
        >>> is_cjk_char("中")
        True
        >>> is_cjk_char("A")
        False
    """
    if not char:
        return False
    code_point = ord(char)
    return (
        0x4E00 <= code_point <= 0x9FFF  # CJK Unified Ideographs
        or 0x3040 <= code_point <= 0x309F  # Hiragana
        or 0x30A0 <= code_point <= 0x30FF  # Katakana
        or 0xAC00 <= code_point <= 0xD7AF  # Hangul
    )


def is_ascii_alnum(char: str) -> bool:
    """Check if a character is an ASCII letter or digit.

    Args:
        char: Single character to check.

    Returns:
        True if character is ASCII alphanumeric.

    Examples:
        >>> is_ascii_alnum("A")
        True
        >>> is_ascii_alnum("1")
        True
        >>> is_ascii_alnum("中")
        False
    """
    return bool(char and char.isascii() and char.isalnum())


def is_url_or_email_context(text: str, pos: int) -> bool:
    """Check if position is within a URL or email address.

    Args:
        text: Full text string.
        pos: Position to check.

    Returns:
        True if position is within a URL or email.

    Examples:
        >>> is_url_or_email_context("Visit https://example.com", 10)
        True
        >>> is_url_or_email_context("Regular text", 5)
        False
    """
    # Simple heuristic: check for protocol or @ nearby
    # Look backward and forward for URL/email indicators
    window_size = 50
    start = max(0, pos - window_size)
    end = min(len(text), pos + window_size)
    context = text[start:end]

    # Check for URL protocols
    url_patterns = [
        r"https?://",
        r"ftp://",
        r"www\.",
    ]
    for pattern in url_patterns:
        if re.search(pattern, context, re.IGNORECASE):
            return True

    # Check for email pattern
    return "@" in context and bool(re.search(r"[\w.-]+@[\w.-]+", context))


def format_text(text: str) -> str:
    """Format CJK-ASCII spacing according to Dualbind rules v0.1.

    Rule v0.1: Insert a half-width space between any CJK character and
    an adjacent ASCII letter/number on either side.

    Args:
        text: Input text with mixed CJK and ASCII characters.

    Returns:
        Formatted text with proper spacing.

    Examples:
        >>> format_text("日本語123ABC")
        '日本語 123ABC'
        >>> format_text("X日本")
        'X 日本'
        >>> format_text("中文English")
        '中文 English'
    """
    if not text:
        return text

    result: list[str] = []
    i = 0

    while i < len(text):
        char = text[i]
        result.append(char)

        # Check if we need to insert a space after this character
        if i < len(text) - 1:
            next_char = text[i + 1]

            # Skip if already followed by space
            if next_char == " ":
                i += 1
                continue

            # Rule: CJK ↔ ASCII letter/number spacing
            if (
                (is_cjk_char(char) and is_ascii_alnum(next_char))
                or (is_ascii_alnum(char) and is_cjk_char(next_char))
            ) and not is_url_or_email_context(text, i):
                result.append(" ")

        i += 1

    return "".join(result)
