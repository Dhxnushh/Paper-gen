import sys
from pathlib import Path

# Make sure project root is on sys.path so imports work when running from tools/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from latex_converter import LaTeXConverter

converter = LaTeXConverter()

sections = {
    'Abstract': r'This is a short abstract about enzymatic polymerization of \\epsilon-caprolactone using Candida antarctica lipase B. The study shows efficient polymerization under mild conditions.',
    'Introduction': 'Introduction content. This should start on a new page. It describes background and motivation for using CALB for polycaprolactone synthesis.',
    'Methods': 'Materials and methods go here.',
    'References': '''[1] P. Bellot, T. Chappell, A. Doucet, S. Geva, S. Gurajada, J. Kamps, G. Kazai, M. Koolen, M. Landoni, M. Marx, et al. Report on INEX 2012. In ACM SIGIR Forum, volume 46, pages 50–59. ACM, 2012.
[2] C. Bravo-Lillo, L. F. Cranor, J. Downs, S. Komanduri, and M. Sleeper. Improving computer security dialogs. In Human-Computer Interaction–INTERACT 2011, pages 18–35. Springer, 2011.
[3] D. P. Coppola. Introduction to international disaster management. Butterworth-Heinemann, 2006.
[4] E. Dale and J. S. Chall. A formula for predicting readability. Educational research bulletin, pages 11–28, 1948.
[5] O. De Clercq, V. Hoste, B. Desmet, P. Van Oosten, M. De Cock, and L. Macken. Using the crowd for readability prediction. Natural Language Engineering, pages 1–33, 2013.'''
}

latex = converter.generate_latex(
    title=r'Enzymatic Synthesis of Polycaprolactone using Candida antarctica Lipase B and \\epsilon-Caprolactone',
    sections_content=sections,
    author='Researcher Name',
    date='October 19, 2025'
)

# Save to a test file
with open('test_output.tex', 'w', encoding='utf-8') as f:
    f.write(latex)

print('Wrote test_output.tex')
print('\n--- Preview (first 1200 characters) ---\n')
print(latex[:1200])
