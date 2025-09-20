# AI Document Processing Agent

## Overview

This AI agent reads documents, identifies instructions for different processes, executes them, and provides status reporting after each execution.

## Features

### 🔍 Document Analysis
- **Instruction Detection**: Uses regex patterns to identify imperative commands, conditional statements, numbered lists, and bullet points
- **Process Categorization**: Automatically categorizes instructions into process types:
  - **File Operations**: create, delete, move, copy, read, write
  - **Data Processing**: analyze, transform, filter, sort, group
  - **Web Operations**: fetch, scrape, download, upload  
  - **System Operations**: run, execute, start, stop, restart
  - **Notification**: alert, notify, send, email, message
  - **General**: other instructions

### ⚡ Execution Simulation
- Simulates execution of identified instructions based on process type
- Provides realistic status responses for each instruction type
- Tracks execution timing and success/failure rates

### 📊 Status Reporting
- Real-time status updates for each instruction execution
- Summary statistics including success rates by process type
- Visual charts showing execution results
- Detailed execution logs with timestamps

## Usage

### Web Interface
1. Start the dashboard: `python document_dashboard.py`
2. Open http://127.0.0.1:8050/ in your browser
3. Enter document text or use sample documents
4. Click "Process Document" to see results

### Command Line
```python
from ai_agent import DocumentProcessor

agent = DocumentProcessor()
results = agent.process_document("Your document text here")
print(f"Found {results['instructions_found']} instructions")
```

## Sample Documents

The system includes three sample documents demonstrating different instruction patterns:

### Project Setup Instructions
```
1. Create a new project directory called "my_project"
2. Download the requirements file from the server
3. Install all dependencies using pip
4. Start the development server on port 8000
5. Send notification email to team@company.com
```

### Data Processing Pipeline
```
First, fetch the daily sales data from the API endpoint
Then, transform the data by removing duplicates
Next, analyze customer behavior patterns
Finally, upload the processed results to cloud storage
```

### System Maintenance
```
- Stop all running services gracefully
- Create backup of the database
- Run system diagnostics
- Update all software packages
- Restart services in correct order
```

## Technical Implementation

### Core Components

1. **DocumentProcessor Class**: Main AI agent class
   - `parse_document()`: Identifies instruction patterns
   - `execute_instructions()`: Simulates instruction execution
   - `get_execution_summary()`: Generates statistics

2. **Pattern Recognition**: Uses regex to identify:
   - Imperative commands (action verbs)
   - Conditional statements (if/then)
   - Sequential instructions (first/then/next)
   - Numbered and bulleted lists

3. **Process Classification**: Categorizes instructions using keyword matching
   - Maps action verbs to process types
   - Handles overlapping categories gracefully

4. **Execution Simulation**: Provides realistic status responses
   - File operations → file_created, file_deleted, etc.
   - Data processing → analysis_completed, filtering_completed
   - Web operations → download_completed, upload_completed
   - System operations → service_started, command_executed
   - Notifications → email_sent, alert_triggered

### Status Tracking

Each instruction execution includes:
- **Instruction text**: Original instruction content
- **Process type**: Categorized process category
- **Pattern type**: How the instruction was identified
- **Execution time**: ISO timestamp of execution
- **Status**: Specific status message
- **Success**: Boolean success/failure
- **Duration**: Execution time in milliseconds
- **Error**: Error details if execution failed

## Example Output

```json
{
  "document_length": 440,
  "instructions_found": 12,
  "execution_summary": {
    "total": 12,
    "successful": 12,
    "failed": 0,
    "success_rate": 100.0,
    "processes": {
      "file_operations": {"total": 3, "successful": 3, "failed": 0},
      "web_operations": {"total": 2, "successful": 2, "failed": 0},
      "data_processing": {"total": 4, "successful": 4, "failed": 0}
    }
  }
}
```

## Testing

Run the test suite to verify functionality:
```bash
python test_ai_agent.py
```

Tests cover:
- Basic instruction detection and execution
- Process type categorization accuracy  
- Status reporting completeness
- Error handling scenarios

## Future Enhancements

- **Real Execution**: Replace simulation with actual command execution
- **Custom Process Types**: Allow users to define new process categories
- **Workflow Dependencies**: Handle instruction dependencies and ordering
- **Error Recovery**: Implement retry logic and error recovery strategies
- **API Integration**: Connect to external systems for real operations
- **Natural Language Processing**: Use advanced NLP for better instruction understanding