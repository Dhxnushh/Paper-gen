"""
Main workflow orchestrator for iterative paper generation and evaluation.
"""
import json
from typing import Dict, List
from generator import PaperGenerator
from evaluator import PaperEvaluator
from latex_converter import LaTeXConverter
from config import SCORE_THRESHOLD, MAX_ITERATIONS


class PaperWorkflow:
    """Orchestrates the iterative paper generation and evaluation workflow."""
    
    def __init__(self):
        """Initialize the workflow with generator, evaluator, and converter."""
        self.generator = PaperGenerator()
        self.evaluator = PaperEvaluator()
        self.latex_converter = LaTeXConverter()
    
    def load_input(self, json_input: str) -> Dict:
        """
        Load and parse input JSON.
        
        Args:
            json_input: JSON string or file path
            
        Returns:
            Parsed input dictionary
        """
        try:
            # Try to load as file first
            with open(json_input, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Try to parse as JSON string
            return json.loads(json_input)
    
    def run_workflow(
        self, 
        input_data: Dict,
        output_latex: str = "paper.tex",
        output_json: str = "paper_final.json"
    ) -> Dict:
        """
        Run the complete iterative workflow.
        
        Args:
            input_data: Input dictionary with title and sections
            output_latex: Output LaTeX filename
            output_json: Output JSON filename
            
        Returns:
            Final paper data with content and evaluation
        """
        title = input_data.get("title", "Untitled Paper")
        sections = input_data.get("sections", [])
        
        if not sections:
            raise ValueError("No sections provided in input data")
        
        print("="*80)
        print(f"Starting Paper Generation Workflow")
        print(f"Title: {title}")
        print(f"Sections: {', '.join(sections)}")
        print(f"Threshold: {SCORE_THRESHOLD} / {len(sections) * 40}")
        print("="*80)
        
        sections_content = {}
        feedback_dict = {}
        iteration = 0
        total_score = 0
        evaluations = {}
        
        # Iterative improvement loop
        while iteration < MAX_ITERATIONS:
            iteration += 1
            print(f"\n{'='*80}")
            print(f"ITERATION {iteration}")
            print(f"{'='*80}\n")
            
            # Step 1: Generate content
            print("Step 1: Generating paper content...")
            sections_content = self.generator.generate_all_sections(
                title, 
                sections, 
                feedback_dict
            )
            
            # Step 2: Evaluate content
            print("\nStep 2: Evaluating paper content...")
            evaluations, total_score = self.evaluator.evaluate_paper(
                title, 
                sections_content
            )
            
            # Calculate per-section average
            avg_score = total_score / len(sections) if sections else 0
            max_possible = len(sections) * 40
            
            print(f"\n{'='*80}")
            print(f"EVALUATION RESULTS - Iteration {iteration}")
            print(f"{'='*80}")
            for section, eval_data in evaluations.items():
                print(f"\n{section}:")
                print(f"  Relevance:   {eval_data['relevance']}/10")
                print(f"  Coherence:   {eval_data['coherence']}/10")
                print(f"  Factuality:  {eval_data['factuality']}/10")
                print(f"  Readability: {eval_data['readability']}/10")
                print(f"  Total:       {eval_data['total']}/40")
                print(f"  Feedback: {eval_data['feedback'][:100]}...")
            
            print(f"\n{'='*80}")
            print(f"OVERALL SCORE: {total_score}/{max_possible}")
            print(f"AVERAGE PER SECTION: {avg_score:.2f}/40")
            print(f"THRESHOLD: {SCORE_THRESHOLD}")
            print(f"{'='*80}\n")
            
            # Step 3: Check if threshold is met
            if total_score >= SCORE_THRESHOLD:
                print(f"✓ Score meets threshold! Proceeding to LaTeX conversion.")
                break
            
            if iteration >= MAX_ITERATIONS:
                print(f"✗ Maximum iterations reached. Proceeding with current version.")
                break
            
            # Prepare feedback for next iteration
            print(f"\n✗ Score below threshold. Preparing for revision...")
            feedback_dict = {
                section: eval_data["feedback"]
                for section, eval_data in evaluations.items()
            }
        
        # Step 4: Convert to LaTeX
        print(f"\nStep 4: Converting to LaTeX format...")
        latex_content = self.latex_converter.generate_latex(
            title, 
            sections_content
        )
        self.latex_converter.save_latex(latex_content, output_latex)
        
        # Save final JSON output
        final_output = {
            "title": title,
            "sections": sections_content,
            "evaluations": evaluations,
            "total_score": total_score,
            "iterations": iteration,
            "threshold_met": total_score >= SCORE_THRESHOLD
        }
        
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(final_output, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*80}")
        print(f"WORKFLOW COMPLETE")
        print(f"{'='*80}")
        print(f"Final Score: {total_score}/{max_possible}")
        print(f"Iterations: {iteration}")
        print(f"LaTeX Output: {output_latex}")
        print(f"JSON Output: {output_json}")
        print(f"{'='*80}\n")
        
        return final_output
