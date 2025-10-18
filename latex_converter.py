"""
LaTeX converter for research papers.
"""
import re
from typing import Dict


class LaTeXConverter:
    """Converts research paper content to LaTeX format."""
    
    def __init__(self):
        """Initialize the LaTeX converter."""
        self.document_class = "article"
        self.packages = [
            "\\usepackage[utf8]{inputenc}",
            "\\usepackage[T1]{fontenc}",
            "\\usepackage{amsmath}",
            "\\usepackage{graphicx}",
            "\\usepackage{hyperref}",
            "\\usepackage{cite}",
            "\\usepackage{geometry}",
            "\\geometry{a4paper, margin=1in}",
            "\\usepackage{setspace}",
            "\\setstretch{1.15}",
            "\\usepackage{titlesec}",
            "% Format section titles",
            "\\titleformat{\\section}{\\normalfont\\Large\\bfseries}{\\thesection}{1em}{}",
            "\\titleformat{\\subsection}{\\normalfont\\large\\bfseries}{\\thesubsection}{1em}{}",
            "\\titleformat{\\subsubsection}{\\normalfont\\normalsize\\bfseries}{\\thesubsubsection}{1em}{}"
        ]
    
    def clean_markdown_formatting(self, text: str) -> str:
        """
        Remove markdown formatting from text and convert to LaTeX.
        
        Args:
            text: Text with potential markdown formatting
            
        Returns:
            Clean text with LaTeX formatting
        """
        # Remove markdown bold (**text** or __text__) - convert to plain text for body
        # We don't want bold in the middle of paragraphs
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        
        # Remove markdown italic (*text* or _text_) - convert to plain text
        text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', text)
        text = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)', r'\1', text)
        
        # Convert standalone markdown headers to LaTeX sections (if any leaked through)
        # These will be proper headings
        text = re.sub(r'^###\s+(.+)$', r'\\subsubsection{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^##\s+(.+)$', r'\\subsection{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^#\s+(.+)$', r'\\section{\1}', text, flags=re.MULTILINE)
        
        # Remove markdown bullet points and convert to LaTeX itemize
        lines = text.split('\n')
        in_list = False
        cleaned_lines = []
        
        for line in lines:
            # Check if line is a bullet point
            if re.match(r'^\s*[\*\-\+]\s+', line):
                if not in_list:
                    cleaned_lines.append('\\begin{itemize}')
                    in_list = True
                # Remove bullet and add \item
                cleaned_line = re.sub(r'^\s*[\*\-\+]\s+', r'\\item ', line)
                cleaned_lines.append(cleaned_line)
            else:
                if in_list and line.strip():
                    cleaned_lines.append('\\end{itemize}')
                    in_list = False
                cleaned_lines.append(line)
        
        if in_list:
            cleaned_lines.append('\\end{itemize}')
        
        text = '\n'.join(cleaned_lines)
        
        # Remove extra blank lines (more than 2 consecutive)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove extra spaces (multiple spaces to single space)
        text = re.sub(r' {2,}', ' ', text)
        
        return text.strip()
    
    def escape_latex_special_chars(self, text: str) -> str:
        """
        Escape special LaTeX characters in text.
        
        Args:
            text: Raw text content
            
        Returns:
            Text with escaped LaTeX special characters
        """
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
            '\\': r'\textbackslash{}'
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        return text
    
    def format_section(self, section_name: str, content: str) -> str:
        """
        Format a section in LaTeX.
        
        Args:
            section_name: Name of the section
            content: Section content
            
        Returns:
            LaTeX-formatted section
        """
        # Clean markdown formatting first
        content = self.clean_markdown_formatting(content)
        
        # Remove any subsection commands that duplicate the main section name
        # This handles cases like having both \section{Conclusion} and \subsection{Conclusion}
        section_pattern = re.escape(section_name)
        content = re.sub(rf'\\subsection\{{{section_pattern}\}}\s*\n*', '', content, flags=re.IGNORECASE)
        content = re.sub(rf'\\subsubsection\{{{section_pattern}\}}\s*\n*', '', content, flags=re.IGNORECASE)
        
        # Ensure consistent paragraph spacing
        # Replace single newlines with space, keep double newlines as paragraph breaks
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []

        for para in paragraphs:
            # Skip empty paragraphs
            if not para.strip():
                continue

            # Skip if paragraph is just a section title (plain text)
            para_stripped = para.strip()
            if para_stripped.lower() == section_name.lower():
                continue

            # Keep LaTeX command lines as-is (section, subsection, etc)
            if re.match(r'^\\(sub)*section', para_stripped):
                formatted_paragraphs.append(para_stripped)
                continue

            # Remove single line breaks within paragraphs (but not in itemize)
            if '\\begin{itemize}' not in para and '\\end{itemize}' not in para and '\\item' not in para:
                para = para.replace('\n', ' ')

            # Normalize spaces
            para = re.sub(r' +', ' ', para)
            para = '\n'.join(line.strip() for line in para.split('\n'))
            para = para.strip()

            if para:
                formatted_paragraphs.append(para)

        # Join paragraphs with blank line and add \noindent to prevent indentation
        # Add vertical space between paragraphs for better readability
        # First paragraph of section should have normal indent, rest should have \noindent
        formatted_content = []
        for i, para in enumerate(formatted_paragraphs):
            if para and not para.startswith('\\'):
                if i == 0:  # First paragraph - let LaTeX indent it naturally
                    formatted_content.append(para)
                else:  # Subsequent paragraphs - add space and \noindent
                    formatted_content.append(f"\\vspace{{0.5em}}\n\\noindent {para}")
            else:
                formatted_content.append(para)
        
        content = '\n\n'.join(formatted_content)

        # Final cleanup: collapse excessive spaces
        content = re.sub(r' +', ' ', content)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Determine section level
        if section_name.lower() == "abstract":
            # Don't include section title in abstract
            return f"\\begin{{abstract}}\n{content}\n\\end{{abstract}}\n"
        else:
            # Ensure a single line break before the section for consistency
            return f"\\section{{{section_name}}}\n{content}\n"
    
    def generate_latex(
        self, 
        title: str, 
        sections_content: Dict[str, str],
        author: str = "Author Name",
        date: str = "\\today"
    ) -> str:
        """
        Generate complete LaTeX document.
        
        Args:
            title: Paper title
            sections_content: Dictionary mapping section names to content
            author: Paper author(s)
            date: Publication date
            
        Returns:
            Complete LaTeX document as string
        """
        # Start document
        latex_content = [
            f"\\documentclass{{{self.document_class}}}",
            "",
            "% Packages"
        ]
        latex_content.extend(self.packages)
        latex_content.extend([
            "",
            "% Document metadata",
            f"\\title{{{title}}}",
            f"\\author{{{author}}}",
            f"\\date{{{date}}}",
            "",
            "\\begin{document}",
            "",
            "\\maketitle",
            ""
        ])
        
        # Add sections
        for section_name, content in sections_content.items():
            # Note: Not escaping here as scientific content may contain LaTeX
            # Users can enable escaping if needed
            formatted_section = self.format_section(section_name, content)
            # Append section without adding extra blank lines to avoid extra vertical spacing
            latex_content.append(formatted_section)
        
        # End document
        latex_content.extend([
            "\\end{document}"
        ])
        
        return "\n".join(latex_content)
    
    def save_latex(
        self, 
        latex_content: str, 
        filename: str = "paper.tex"
    ) -> None:
        """
        Save LaTeX content to file.
        
        Args:
            latex_content: LaTeX document content
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        print(f"LaTeX document saved to: {filename}")
