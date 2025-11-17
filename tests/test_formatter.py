"""Tests for CJK-ASCII formatter."""

import pytest

from cjk_ascii_formatter.formatter import (
    format_text,
    is_ascii_alnum,
    is_cjk_char,
    is_url_or_email_context,
)


class TestCJKDetection:
    """Test CJK character detection."""

    def test_chinese_characters(self) -> None:
        """Test Chinese character detection."""
        assert is_cjk_char("中")
        assert is_cjk_char("文")
        assert is_cjk_char("國")

    def test_japanese_hiragana(self) -> None:
        """Test Japanese Hiragana detection."""
        assert is_cjk_char("あ")
        assert is_cjk_char("の")
        assert is_cjk_char("ん")

    def test_japanese_katakana(self) -> None:
        """Test Japanese Katakana detection."""
        assert is_cjk_char("ア")
        assert is_cjk_char("カ")
        assert is_cjk_char("ン")

    def test_korean_hangul(self) -> None:
        """Test Korean Hangul detection."""
        assert is_cjk_char("한")
        assert is_cjk_char("글")
        assert is_cjk_char("가")

    def test_ascii_not_cjk(self) -> None:
        """Test ASCII characters are not CJK."""
        assert not is_cjk_char("A")
        assert not is_cjk_char("z")
        assert not is_cjk_char("1")
        assert not is_cjk_char("!")


class TestASCIIAlnumDetection:
    """Test ASCII alphanumeric detection."""

    def test_letters(self) -> None:
        """Test ASCII letters."""
        assert is_ascii_alnum("A")
        assert is_ascii_alnum("z")
        assert is_ascii_alnum("M")

    def test_numbers(self) -> None:
        """Test ASCII numbers."""
        assert is_ascii_alnum("0")
        assert is_ascii_alnum("5")
        assert is_ascii_alnum("9")

    def test_non_alnum(self) -> None:
        """Test non-alphanumeric ASCII."""
        assert not is_ascii_alnum(" ")
        assert not is_ascii_alnum("!")
        assert not is_ascii_alnum("@")

    def test_cjk_not_alnum(self) -> None:
        """Test CJK characters are not ASCII alnum."""
        assert not is_ascii_alnum("中")
        assert not is_ascii_alnum("あ")


class TestURLEmailContext:
    """Test URL and email context detection."""

    def test_http_url(self) -> None:
        """Test HTTP URL detection."""
        text = "Visit https://example.com for more"
        assert is_url_or_email_context(text, 10)

    def test_email(self) -> None:
        """Test email detection."""
        text = "Contact user@example.com for help"
        assert is_url_or_email_context(text, 12)

    def test_normal_text(self) -> None:
        """Test normal text is not URL/email context."""
        text = "This is normal text"
        assert not is_url_or_email_context(text, 5)


class TestFormatText:
    """Test the main format_text function."""

    def test_japanese_with_numbers(self) -> None:
        """Test Japanese with numbers - example from requirements."""
        assert format_text("日本語123ABC") == "日本語 123ABC"

    def test_ascii_before_japanese(self) -> None:
        """Test ASCII before Japanese - example from requirements."""
        assert format_text("X日本") == "X 日本"

    def test_chinese_with_english(self) -> None:
        """Test Chinese with English."""
        assert format_text("中文English") == "中文 English"

    def test_korean_with_numbers(self) -> None:
        """Test Korean with numbers."""
        assert format_text("한글123") == "한글 123"

    def test_multiple_transitions(self) -> None:
        """Test multiple CJK-ASCII transitions."""
        assert format_text("中文ABC日本DEF") == "中文 ABC 日本 DEF"

    def test_already_spaced(self) -> None:
        """Test text that already has proper spacing."""
        assert format_text("中文 English") == "中文 English"
        assert format_text("日本語 123") == "日本語 123"

    def test_empty_string(self) -> None:
        """Test empty string."""
        assert format_text("") == ""

    def test_only_cjk(self) -> None:
        """Test text with only CJK characters."""
        assert format_text("中文日本語한글") == "中文日本語한글"

    def test_only_ascii(self) -> None:
        """Test text with only ASCII."""
        assert format_text("Hello World 123") == "Hello World 123"

    def test_cjk_with_punctuation(self) -> None:
        """Test CJK with punctuation."""
        # Rule v0.1: Only ASCII letters/numbers trigger spacing, not punctuation
        assert format_text("中文,English") == "中文,English"
        assert format_text("中文.") == "中文."
        # But a letter after punctuation should still get spacing
        assert format_text("Chinese中文") == "Chinese 中文"

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("日本語123ABC", "日本語 123ABC"),
            ("X日本", "X 日本"),
            ("中文English", "中文 English"),
            ("한글ABC", "한글 ABC"),
            ("テスト123", "テスト 123"),
            ("ひらがなTest", "ひらがな Test"),
        ],
    )
    def test_parametrized_cases(self, input_text: str, expected: str) -> None:
        """Test multiple cases with parametrize."""
        assert format_text(input_text) == expected


class TestEdgeCases:
    """Test edge cases including URLs and emails."""

    def test_url_unchanged(self) -> None:
        """Test URLs are not affected by formatting."""
        url_text = "Visit https://example.com/日本語"
        # URL should remain unchanged
        assert format_text(url_text) == url_text

    def test_email_unchanged(self) -> None:
        """Test emails are not affected by formatting."""
        email_text = "Contact test@example.com"
        # Email should remain unchanged
        assert format_text(email_text) == email_text

    def test_url_in_sentence(self) -> None:
        """Test URL within a sentence."""
        text = "See https://example.com for details"
        # The word "for" should still work normally
        result = format_text(text)
        assert "https://example.com" in result

    def test_mixed_with_newlines(self) -> None:
        """Test formatting preserves newlines."""
        text = "中文ABC\n日本語123"
        expected = "中文 ABC\n日本語 123"
        assert format_text(text) == expected

    def test_consecutive_ascii_and_cjk(self) -> None:
        """Test consecutive transitions."""
        assert format_text("A中B文C") == "A 中 B 文 C"

    def test_tab_and_special_chars(self) -> None:
        """Test with tabs and special characters."""
        # Rule v0.1: Tabs are not ASCII alnum, so they don't trigger spacing
        text = "中文\tEnglish"
        expected = "中文\tEnglish"
        assert format_text(text) == expected
        # But letters next to CJK should still get spacing
        text2 = "中文English"
        expected2 = "中文 English"
        assert format_text(text2) == expected2
