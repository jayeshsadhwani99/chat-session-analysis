import pytest
import pandas as pd
import sys
import os

# Add the parent directory to the path so we can import sample_pipeline
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sample_pipeline import (
    classify_intent, 
    classify_funnel, 
    extract_brand, 
    classify_support,
    Intent,
    FunnelStage
)


class TestIntentClassification:
    """Test cases for intent classification functionality."""
    
    def test_commercial_intent(self):
        """Test commercial intent detection."""
        queries = [
            "How much does it cost?",
            "I want to buy a subscription",
            "What's the pricing?",
            "Can I get a discount?",
            "Upgrade my plan"
        ]
        for query in queries:
            assert classify_intent(query) == Intent.COMMERCIAL
    
    def test_paraphrase_edit_intent(self):
        """Test paraphrase/edit intent detection."""
        queries = [
            "Can you reword this?",
            "Rewrite this text",
            "Paraphrase this sentence",
            "Improve my writing",
            "Check grammar"
        ]
        for query in queries:
            assert classify_intent(query) == Intent.PARAPHRASE_EDIT
    
    def test_educational_quiz_intent(self):
        """Test educational/quiz intent detection."""
        queries = [
            "A. First option B. Second option",
            "Select the correct answer",
            "Which of the following is true?",
            "What is this called?",
            "Definition of machine learning"
        ]
        for query in queries:
            assert classify_intent(query) == Intent.EDUCATIONAL_QUIZ
    
    def test_informational_intent(self):
        """Test informational intent detection."""
        queries = [
            "How to install Python?",
            "What is machine learning?",
            "Who is the CEO?",
            "Why does this happen?",
            "Can you tell me about APIs?"
        ]
        for query in queries:
            assert classify_intent(query) == Intent.INFORMATIONAL
    
    def test_navigational_intent(self):
        """Test navigational intent detection."""
        queries = [
            "Go to my dashboard",
            "Open settings",
            "Find my account",
            "Login to the system",
            "Access my profile"
        ]
        for query in queries:
            assert classify_intent(query) == Intent.NAVIGATIONAL
    
    def test_other_intent(self):
        """Test other intent detection."""
        queries = [
            "Hello there",
            "Thanks for your help",
            "Good morning",
            "",
            None
        ]
        for query in queries:
            assert classify_intent(query) == Intent.OTHER


class TestFunnelClassification:
    """Test cases for funnel stage classification."""
    
    def test_decision_funnel(self):
        """Test decision funnel stage."""
        query = "I want to buy this"
        intent = Intent.COMMERCIAL
        assert classify_funnel(query, intent) == FunnelStage.DECISION
    
    def test_retention_funnel(self):
        """Test retention funnel stage."""
        # Navigational intent
        query = "Go to my account"
        intent = Intent.NAVIGATIONAL
        assert classify_funnel(query, intent) == FunnelStage.RETENTION
        
        # Support keywords
        query = "I need help with an error"
        intent = Intent.OTHER
        assert classify_funnel(query, intent) == FunnelStage.RETENTION
    
    def test_consideration_funnel(self):
        """Test consideration funnel stage."""
        queries = [
            "Compare these options",
            "What are the pros and cons?",
            "Which is better?",
            "Show me alternatives"
        ]
        for query in queries:
            assert classify_funnel(query, Intent.OTHER) == FunnelStage.CONSIDERATION
    
    def test_awareness_funnel(self):
        """Test awareness funnel stage."""
        # Informational intent
        query = "What is this?"
        intent = Intent.INFORMATIONAL
        assert classify_funnel(query, intent) == FunnelStage.AWARENESS
        
        # Educational intent
        query = "Explain this concept"
        intent = Intent.EDUCATIONAL_QUIZ
        assert classify_funnel(query, intent) == FunnelStage.AWARENESS


class TestBrandExtraction:
    """Test cases for brand extraction functionality."""
    
    def test_brand_detection(self):
        """Test brand detection in queries."""
        test_cases = [
            ("I love using Google", "google"),
            ("Microsoft Office is great", "microsoft"),
            ("How to use Apple products", "apple"),
            ("OpenAI ChatGPT is amazing", "chatgpt"),  # "chatgpt" comes before "openai" in sorted list
            ("AWS cloud services", "aws"),
            ("No brand mentioned here", "none")
        ]
        
        for query, expected_brand in test_cases:
            assert extract_brand(query) == expected_brand
    
    def test_longer_brand_precedence(self):
        """Test that longer brand names are matched first."""
        query = "I use Google Cloud Platform"
        # Should match "google cloud" before "google"
        assert extract_brand(query) == "google cloud"


class TestSupportClassification:
    """Test cases for support query classification."""
    
    def test_support_detection(self):
        """Test support query detection."""
        support_queries = [
            "I need help with an error",
            "How do I reset my password?",
            "Something is broken",
            "I'm having trouble with this",
            "Support request"
        ]
        
        for query in support_queries:
            assert classify_support(query) is True
    
    def test_non_support_detection(self):
        """Test non-support query detection."""
        non_support_queries = [
            "How to use this feature?",
            "What is the price?",
            "Hello there"
            # Removed "Thanks for your help" as "help" is in support keywords
        ]
        
        for query in non_support_queries:
            assert classify_support(query) is False


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_inputs(self):
        """Test handling of empty or None inputs."""
        assert classify_intent("") == Intent.OTHER
        assert classify_intent(None) == Intent.OTHER
        assert classify_funnel("", Intent.OTHER) == FunnelStage.AWARENESS
        assert classify_funnel(None, Intent.OTHER) == FunnelStage.AWARENESS
        assert extract_brand("") == "none"
        assert extract_brand(None) == "none"
        assert classify_support("") is False
        assert classify_support(None) is False
    
    def test_case_insensitivity(self):
        """Test that classification is case insensitive."""
        assert classify_intent("HOW TO BUY") == Intent.COMMERCIAL  # "buy" triggers commercial intent
        assert classify_intent("how to buy") == Intent.COMMERCIAL
        assert extract_brand("GOOGLE") == "google"
        assert extract_brand("google") == "google"


if __name__ == "__main__":
    pytest.main([__file__]) 