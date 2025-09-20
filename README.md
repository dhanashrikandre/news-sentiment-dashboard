# news-sentiment-dashboard
A real-time sentiment tracker using global news headlines with AI document processing capabilities.

## Features

### 📰 News Sentiment Analysis
- Pulls top headlines from RSS Feeds for multiple countries
- Analyzes sentiment using VADER
- Displays a world sentiment map and word cloud

### 🤖 AI Document Processing Agent
- **Document Analysis**: Reads documents and identifies instructions for different processes
- **Instruction Categorization**: Automatically categorizes instructions by process type (file operations, data processing, web operations, system operations, notifications)
- **Execution Simulation**: Simulates execution of identified instructions with realistic status responses
- **Status Reporting**: Provides real-time status updates and execution summaries

## Setup

1. Clone the repo
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the news sentiment dashboard:
    ```bash
    python dashboard.py
    ```
   Or run the AI document processing agent:
    ```bash
    python document_dashboard.py
    ```

## AI Document Processing Agent

The AI agent can process documents containing instructions and:
- Identify different types of instructions (imperative, conditional, sequential, numbered, bulleted)
- Categorize instructions by process type
- Execute instructions with status reporting
- Provide execution summaries and visualizations

### Usage Examples

1. **Web Interface**: Open http://127.0.0.1:8050/ after running `document_dashboard.py`
2. **Command Line**:
    ```python
    from ai_agent import DocumentProcessor
    agent = DocumentProcessor()
    results = agent.process_document("Your document text here")
    ```

### Sample Documents Included
- Project setup instructions
- Data processing pipeline workflows  
- System maintenance procedures

See [AI_AGENT_README.md](AI_AGENT_README.md) for detailed documentation.

## Testing

Test the AI agent functionality:
```bash
python test_ai_agent.py
```

## Output

### News Sentiment Dashboard
After running the code, open this link in browser: http://127.0.0.1:8050/ to see the output

![image](https://github.com/user-attachments/assets/09d13f0b-b5b3-443d-97f9-f3edc67e68f1)

### AI Document Processing Agent
The AI agent provides a modern web interface for document processing with real-time instruction analysis and execution status reporting.
