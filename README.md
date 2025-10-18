# AI Research Paper Generator - API Server# Research Paper Generator with Iterative Improvement



Minimal FastAPI server for AI-powered research paper generation.An AI-powered research paper generation system that uses iterative evaluation and refinement to produce high-quality academic content.



## 🚀 Quick Start## Overview



```powershellThis system implements a sophisticated workflow that:

# Start the server

python start_server.py1. **Generates** research paper content using Google Gemini 2.5 Flash

```2. **Evaluates** the content using Google Gemini 2.5 Flash-Lite with multiple quality criteria

3. **Refines** the content iteratively based on evaluation feedback

Server runs at: **http://localhost:8000**4. **Converts** the final paper to professional LaTeX format



## 📡 API Endpoints## Features



### 1. Generate Paper- 🤖 **Dual-Model Architecture**: Separate generator and evaluator models for quality

**POST** `/generate`- 🔄 **Iterative Improvement**: Automatic revision based on evaluation feedback

- 📊 **Multi-Criteria Evaluation**: Scores for relevance, coherence, factuality, and readability

```json- 📝 **LaTeX Output**: Professional research paper formatting

{- ⚙️ **Configurable Thresholds**: Adjustable quality standards

  "title": "Paper Title",- 🔌 **LangChain Integration**: Modular and extensible architecture

  "sections": ["Abstract", "Introduction", "Conclusion"]

}## Installation

```

1. Clone the repository:

Returns `job_id` for tracking.```bash

git clone <repository-url>

### 2. Check Statuscd Report-ai

**GET** `/status/{job_id}````



Returns current generation status.2. Install dependencies:

```bash

### 3. Get Resultspip install -r requirements.txt

**GET** `/paper/{job_id}/json` - JSON format  ```

**GET** `/paper/{job_id}/latex` - LaTeX format

3. Set up your API keys:

## 🔧 Setup   - Copy `.env.example` to `.env`

   - Get your Google AI Studio API key from https://aistudio.google.com/app/apikey

```powershell   ```bash

pip install -r requirements.txt   cp .env.example .env

```   ```

   - Edit `.env` and add your API key:

Create `.env` file with:   ```

```   GOOGLE_API_KEY="your-api-key-here"

GOOGLE_API_KEY=your-key-here   ```

```

## Usage

## 📦 Core Files

### Basic Usage

- `api.py` - FastAPI server with job management

- `workflow.py` - Paper generation orchestrationRun with the example input:

- `generator.py` - AI content generation```bash

- `evaluator.py` - Quality evaluationpython main.py

- `latex_converter.py` - LaTeX formatting```

- `models.py` - LLM configuration

- `config.py` - Settings### Custom Input



That's it! Simple and clean.Create a JSON input file with your paper structure:


```json
{
  "title": "Your Research Paper Title",
  "sections": [
    "Abstract",
    "Introduction",
    "Methodology",
    "Results",
    "Conclusion"
  ],
  "feedback": ""
}
```

Run with your input file:
```bash
python main.py input.json
```

### Output Files

The system generates three output files:

1. **`output_paper.tex`** - LaTeX formatted research paper
2. **`output_paper.json`** - Complete paper data with evaluations
3. **`input_example.json`** - Example input format (auto-generated)

## Architecture

### Components

1. **`config.py`** - Configuration and constants
2. **`models.py`** - Model initialization and LangChain setup
3. **`generator.py`** - Content generation logic
4. **`evaluator.py`** - Content evaluation and scoring
5. **`latex_converter.py`** - LaTeX formatting and conversion
6. **`workflow.py`** - Main orchestration logic
7. **`main.py`** - Entry point and CLI

### Workflow

```
┌─────────────────────────────────────────────────────┐
│ 1. Load Input JSON                                  │
│    (title, sections)                                │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 2. Generate Content                                 │
│    Model: Mistral-7B-Instruct                       │
│    → Write content for each section                 │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 3. Evaluate Content                                 │
│    Model: Llama-3-8B-Instruct                       │
│    → Score: Relevance, Coherence,                   │
│              Factuality, Readability (0-10 each)    │
│    → Provide detailed feedback                      │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 4. Check Score vs Threshold                         │
└─────────────┬───────────────┬───────────────────────┘
              │               │
      Score < Threshold   Score ≥ Threshold
              │               │
              ▼               ▼
┌─────────────────────┐  ┌──────────────────────┐
│ 5a. Revise Content  │  │ 5b. Convert to LaTeX │
│     (use feedback)  │  │     → Final output   │
│     → Loop to step 2│  └──────────────────────┘
└─────────────────────┘
     (max 5 iterations)
```

## Configuration

Edit `config.py` to customize:

- **Models**: Change generator/evaluator models
- **Thresholds**: Adjust quality score threshold (default: 32/40)
- **Iterations**: Set maximum revision attempts (default: 5)
- **API Settings**: Configure API endpoints and keys

## Evaluation Criteria

Each section is scored on four criteria (0-10 points each):

1. **Relevance** - Content relevance to section topic
2. **Coherence** - Structure and logical flow
3. **Factuality** - Accuracy and support for claims
4. **Readability** - Clarity and accessibility

**Total possible score per section**: 40 points

## Requirements

- Python 3.8+
- LangChain
- Google AI Studio API key (free tier available)
- Internet connection for API calls

## Example Output

The system produces a complete LaTeX document with:

- Proper document structure
- Title and metadata
- All sections with generated content
- Professional formatting
- Ready to compile with `pdflatex`

To compile the LaTeX output:
```bash
pdflatex output_paper.tex
```

## Troubleshooting

### API Key Issues
- Ensure your Google API key is properly set in `.env`
- Get a free API key at https://aistudio.google.com/app/apikey
- Note: Free tier has generous limits (60 requests/minute for Gemini Pro)

### Low Scores
- Adjust `SCORE_THRESHOLD` in `config.py`
- Increase `MAX_ITERATIONS` for more revision attempts
- Try more specific section names in your input

### Model Errors
- Check that model names are correct in `config.py`
- Verify your API provider supports the models
- Check API rate limits and quotas

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Models via [Google AI Studio](https://aistudio.google.com/)
- Generator: Gemini 2.5 Flash
- Evaluator: Gemini 2.5 Flash-Lite
