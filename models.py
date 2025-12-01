"""
Model initialization and management for generator and evaluator.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import (
    GENERATOR_MODEL,
    EVALUATOR_MODEL,
    GOOGLE_API_KEY
)


class ModelManager:
    """Manages the generator and evaluator models."""
    
    def __init__(self):
        """Initialize the generator and evaluator models."""
        self.generator = self._init_generator()
        self.evaluator = self._init_evaluator()
    
    def _init_generator(self):
        """Initialize the generator model (Gemini 2.5 Flash)."""
        return ChatGoogleGenerativeAI(
            model=GENERATOR_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.7,
            max_output_tokens=8000,
            top_p=0.9,
            convert_system_message_to_human=True
        )
    
    def _init_evaluator(self):
        """Initialize the evaluator model (Gemini 2.5 Flash-Lite)."""
        return ChatGoogleGenerativeAI(
            model=EVALUATOR_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.3,
            max_output_tokens=4000,
            top_p=0.95,
            convert_system_message_to_human=True
        )
    
    def create_generator_chain(self):
        """Create a LangChain chain for content generation."""
        prompt = PromptTemplate(
            input_variables=["title", "section", "feedback"],
            template="""You are an expert academic writer. Write high-quality research paper content in plain text.

Paper Title: {title}
Section: {section}

{feedback}

CRITICAL FORMATTING REQUIREMENTS:
- Write in plain text WITHOUT any markdown formatting
- Do NOT use **bold**, *italic*, __underline__, or any markdown syntax
- Do NOT use bullet points with *, -, or + symbols
- Do NOT use # headers or other markdown elements
- Write in complete, flowing paragraphs
- Use proper academic prose with clear topic sentences
- Separate paragraphs with a single blank line
- Use transitions like "Furthermore," "However," "Moreover," etc.

SPECIAL REQUIREMENTS FOR REFERENCES SECTION:
If the section is "References" or "Bibliography":
- Format each reference as a numbered citation: [1], [2], [3], etc.
- Each reference must start on a new line with the number in square brackets
- Follow this exact format for each entry:
  [1] Author(s). Title. Publication. Year.
  [2] Author(s). Title. Publication. Year.
- Include 10-15 relevant academic references
- Use proper citation format (author, title, journal/conference, pages, year)
- Do NOT write references as paragraphs or prose
- Example format:
  [1] P. Smith, J. Doe. A Study on Topic. Journal of Science, vol. 10, pages 1-20. 2020.
  [2] M. Johnson. Another Important Work. Conference Proceedings, pages 45-60. ACM, 2019.

Write a comprehensive, well-researched section that is:
- Academically rigorous and properly structured
- Clear and coherent with smooth transitions
- Factually accurate with logical arguments  
- Professional and readable
- Written entirely in plain text format

Section Content:"""
        )
        
        return LLMChain(llm=self.generator, prompt=prompt)
    
    def create_evaluator_chain(self):
        """Create a LangChain chain for content evaluation."""
        prompt = PromptTemplate(
            input_variables=["title", "section", "content"],
            template="""You are an expert academic reviewer. Evaluate the following research paper section.

Paper Title: {title}
Section: {section}

Content:
{content}

Evaluate the content based on these criteria (score 0-10 for each):

1. RELEVANCE: How relevant is the content to the section topic?
2. COHERENCE: How well-structured and logically flowing is the content?
3. FACTUALITY: How accurate and well-supported are the claims?
4. READABILITY: How clear and accessible is the writing?

Provide your evaluation in this EXACT format:
RELEVANCE: [score]
COHERENCE: [score]
FACTUALITY: [score]
READABILITY: [score]
TOTAL: [sum of all scores]
FEEDBACK: [Detailed feedback on what needs improvement. Be specific about weaknesses and how to address them.]"""
        )
        
        return LLMChain(llm=self.evaluator, prompt=prompt)
