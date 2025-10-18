"""
Content evaluator for research paper quality assessment.
"""
import re
from typing import Dict, Tuple
from models import ModelManager
from config import EVALUATION_CRITERIA


class PaperEvaluator:
    """Evaluates research paper content quality."""
    
    def __init__(self):
        """Initialize the paper evaluator with model manager."""
        self.model_manager = ModelManager()
        self.evaluator_chain = self.model_manager.create_evaluator_chain()
    
    def parse_evaluation(self, evaluation_text: str) -> Dict[str, any]:
        """
        Parse the evaluation text to extract scores and feedback.
        
        Args:
            evaluation_text: Raw evaluation text from the model
            
        Returns:
            Dictionary containing scores and feedback
        """
        result = {
            "relevance": 0,
            "coherence": 0,
            "factuality": 0,
            "readability": 0,
            "total": 0,
            "feedback": ""
        }
        
        try:
            # Extract scores using regex
            relevance_match = re.search(r'RELEVANCE:\s*(\d+)', evaluation_text, re.IGNORECASE)
            coherence_match = re.search(r'COHERENCE:\s*(\d+)', evaluation_text, re.IGNORECASE)
            factuality_match = re.search(r'FACTUALITY:\s*(\d+)', evaluation_text, re.IGNORECASE)
            readability_match = re.search(r'READABILITY:\s*(\d+)', evaluation_text, re.IGNORECASE)
            total_match = re.search(r'TOTAL:\s*(\d+)', evaluation_text, re.IGNORECASE)
            feedback_match = re.search(r'FEEDBACK:\s*(.+)', evaluation_text, re.IGNORECASE | re.DOTALL)
            
            if relevance_match:
                result["relevance"] = int(relevance_match.group(1))
            if coherence_match:
                result["coherence"] = int(coherence_match.group(1))
            if factuality_match:
                result["factuality"] = int(factuality_match.group(1))
            if readability_match:
                result["readability"] = int(readability_match.group(1))
            if total_match:
                result["total"] = int(total_match.group(1))
            else:
                # Calculate total if not provided
                result["total"] = (
                    result["relevance"] + 
                    result["coherence"] + 
                    result["factuality"] + 
                    result["readability"]
                )
            if feedback_match:
                result["feedback"] = feedback_match.group(1).strip()
            
        except Exception as e:
            print(f"Error parsing evaluation: {str(e)}")
            result["feedback"] = evaluation_text
        
        return result
    
    def evaluate_section(
        self, 
        title: str, 
        section: str, 
        content: str
    ) -> Dict[str, any]:
        """
        Evaluate a single section of the paper.
        
        Args:
            title: The paper title
            section: The section name
            content: The section content
            
        Returns:
            Dictionary containing evaluation scores and feedback
        """
        try:
            evaluation_text = self.evaluator_chain.run(
                title=title,
                section=section,
                content=content
            )
            return self.parse_evaluation(evaluation_text)
        except Exception as e:
            print(f"Error evaluating section '{section}': {str(e)}")
            return {
                "relevance": 0,
                "coherence": 0,
                "factuality": 0,
                "readability": 0,
                "total": 0,
                "feedback": f"Evaluation error: {str(e)}"
            }
    
    def evaluate_paper(
        self, 
        title: str, 
        sections_content: Dict[str, str]
    ) -> Tuple[Dict[str, Dict], int]:
        """
        Evaluate all sections of the paper.
        
        Args:
            title: The paper title
            sections_content: Dictionary mapping section names to content
            
        Returns:
            Tuple of (evaluations dict, total score)
        """
        evaluations = {}
        total_score = 0
        
        for section, content in sections_content.items():
            print(f"Evaluating section: {section}...")
            evaluation = self.evaluate_section(title, section, content)
            evaluations[section] = evaluation
            total_score += evaluation["total"]
        
        return evaluations, total_score
