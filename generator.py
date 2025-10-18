"""
Content generator for research paper sections.
"""
from typing import Dict, List
from models import ModelManager


class PaperGenerator:
    """Generates content for research paper sections."""
    
    def __init__(self):
        """Initialize the paper generator with model manager."""
        self.model_manager = ModelManager()
        self.generator_chain = self.model_manager.create_generator_chain()
    
    def generate_section(
        self, 
        title: str, 
        section: str, 
        feedback: str = ""
    ) -> str:
        """
        Generate content for a specific section.
        
        Args:
            title: The paper title
            section: The section name (e.g., "Abstract", "Introduction")
            feedback: Optional feedback from evaluator for revision
            
        Returns:
            Generated content for the section
        """
        feedback_prompt = ""
        if feedback:
            feedback_prompt = f"Previous Feedback (use this to improve):\n{feedback}\n\nIMPORTANT: Continue to write in plain text without markdown formatting.\n"
        
        try:
            result = self.generator_chain.run(
                title=title,
                section=section,
                feedback=feedback_prompt
            )
            return result.strip()
        except Exception as e:
            print(f"Error generating section '{section}': {str(e)}")
            return f"[Error generating content: {str(e)}]"
    
    def generate_all_sections(
        self, 
        title: str, 
        sections: List[str],
        feedback_dict: Dict[str, str] = None
    ) -> Dict[str, str]:
        """
        Generate content for all sections of the paper.
        
        Args:
            title: The paper title
            sections: List of section names
            feedback_dict: Dictionary mapping sections to feedback
            
        Returns:
            Dictionary mapping section names to generated content
        """
        if feedback_dict is None:
            feedback_dict = {}
        
        content = {}
        for section in sections:
            print(f"Generating section: {section}...")
            feedback = feedback_dict.get(section, "")
            content[section] = self.generate_section(title, section, feedback)
        
        return content
