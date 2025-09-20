import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any
import os


class DocumentProcessor:
    """AI agent to read documents, identify instructions, and execute them."""
    
    def __init__(self):
        self.execution_log = []
        self.supported_processes = {
            'file_operations': ['create', 'delete', 'move', 'copy', 'read', 'write'],
            'data_processing': ['analyze', 'transform', 'filter', 'sort', 'group'],
            'web_operations': ['fetch', 'scrape', 'download', 'upload'],
            'system_operations': ['run', 'execute', 'start', 'stop', 'restart'],
            'notification': ['alert', 'notify', 'send', 'email', 'message']
        }
        
    def parse_document(self, text: str) -> Dict[str, List[Dict]]:
        """
        Parse document to identify instruction patterns and categorize them by process type.
        
        Args:
            text: Document text to parse
            
        Returns:
            Dictionary with process types as keys and list of instructions as values
        """
        instructions_by_process = {}
        
        # Common instruction patterns
        patterns = {
            'imperative': r'\b(create|delete|move|copy|read|write|analyze|transform|filter|sort|group|fetch|scrape|download|upload|run|execute|start|stop|restart|alert|notify|send|email|message)\s+[\w\s,.-]+',
            'conditional': r'if\s+.+\s+then\s+.+',
            'sequential': r'(first|then|next|finally|after|before)\s+.+',
            'numbered': r'\d+\.\s+.+',
            'bullet': r'[•\-\*]\s+.+'
        }
        
        # Find all instruction-like sentences
        for pattern_type, pattern in patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                instruction_text = match.group().strip()
                process_type = self._identify_process_type(instruction_text)
                
                if process_type not in instructions_by_process:
                    instructions_by_process[process_type] = []
                
                instructions_by_process[process_type].append({
                    'text': instruction_text,
                    'pattern_type': pattern_type,
                    'position': match.start(),
                    'identified_at': datetime.now().isoformat()
                })
        
        return instructions_by_process
    
    def _identify_process_type(self, instruction: str) -> str:
        """Identify which process type an instruction belongs to."""
        instruction_lower = instruction.lower()
        
        for process_type, keywords in self.supported_processes.items():
            for keyword in keywords:
                if keyword in instruction_lower:
                    return process_type
        
        return 'general'
    
    def execute_instructions(self, instructions_by_process: Dict[str, List[Dict]]) -> List[Dict]:
        """
        Execute identified instructions and return status for each.
        
        Args:
            instructions_by_process: Dictionary of instructions categorized by process type
            
        Returns:
            List of execution results with status
        """
        execution_results = []
        
        for process_type, instructions in instructions_by_process.items():
            for instruction in instructions:
                result = self._execute_single_instruction(instruction, process_type)
                execution_results.append(result)
                self.execution_log.append(result)
                
        return execution_results
    
    def _execute_single_instruction(self, instruction: Dict, process_type: str) -> Dict:
        """Execute a single instruction based on its process type."""
        execution_start = datetime.now()
        
        try:
            # Simulate execution based on process type
            status = self._simulate_execution(instruction['text'], process_type)
            
            result = {
                'instruction': instruction['text'],
                'process_type': process_type,
                'pattern_type': instruction['pattern_type'],
                'execution_time': execution_start.isoformat(),
                'status': status,
                'success': status != 'failed',
                'duration_ms': int((datetime.now() - execution_start).total_seconds() * 1000)
            }
            
        except Exception as e:
            result = {
                'instruction': instruction['text'],
                'process_type': process_type,
                'pattern_type': instruction['pattern_type'],
                'execution_time': execution_start.isoformat(),
                'status': 'failed',
                'success': False,
                'error': str(e),
                'duration_ms': int((datetime.now() - execution_start).total_seconds() * 1000)
            }
            
        return result
    
    def _simulate_execution(self, instruction: str, process_type: str) -> str:
        """Simulate execution of instruction based on process type."""
        instruction_lower = instruction.lower()
        
        # File operations simulation
        if process_type == 'file_operations':
            if 'create' in instruction_lower:
                return 'file_created'
            elif 'delete' in instruction_lower:
                return 'file_deleted'
            elif 'read' in instruction_lower:
                return 'file_read'
            elif 'write' in instruction_lower:
                return 'file_written'
            else:
                return 'file_operation_completed'
        
        # Data processing simulation
        elif process_type == 'data_processing':
            if 'analyze' in instruction_lower:
                return 'analysis_completed'
            elif 'transform' in instruction_lower:
                return 'transformation_completed'
            elif 'filter' in instruction_lower:
                return 'filtering_completed'
            else:
                return 'data_processing_completed'
        
        # Web operations simulation
        elif process_type == 'web_operations':
            if 'fetch' in instruction_lower or 'download' in instruction_lower:
                return 'download_completed'
            elif 'upload' in instruction_lower:
                return 'upload_completed'
            else:
                return 'web_operation_completed'
        
        # System operations simulation
        elif process_type == 'system_operations':
            if 'start' in instruction_lower:
                return 'service_started'
            elif 'stop' in instruction_lower:
                return 'service_stopped'
            elif 'run' in instruction_lower or 'execute' in instruction_lower:
                return 'command_executed'
            else:
                return 'system_operation_completed'
        
        # Notification simulation
        elif process_type == 'notification':
            if 'email' in instruction_lower:
                return 'email_sent'
            elif 'alert' in instruction_lower:
                return 'alert_triggered'
            else:
                return 'notification_sent'
        
        # General instructions
        else:
            return 'instruction_processed'
    
    def get_execution_summary(self) -> Dict:
        """Get summary of all executions."""
        if not self.execution_log:
            return {'total': 0, 'successful': 0, 'failed': 0, 'processes': {}}
        
        total = len(self.execution_log)
        successful = sum(1 for result in self.execution_log if result['success'])
        failed = total - successful
        
        processes = {}
        for result in self.execution_log:
            process_type = result['process_type']
            if process_type not in processes:
                processes[process_type] = {'total': 0, 'successful': 0, 'failed': 0}
            
            processes[process_type]['total'] += 1
            if result['success']:
                processes[process_type]['successful'] += 1
            else:
                processes[process_type]['failed'] += 1
        
        return {
            'total': total,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total) * 100 if total > 0 else 0,
            'processes': processes,
            'last_execution': self.execution_log[-1]['execution_time'] if self.execution_log else None
        }
    
    def process_document(self, text: str) -> Dict:
        """
        Main method to process a document end-to-end.
        
        Args:
            text: Document text to process
            
        Returns:
            Complete processing results including instructions found and execution status
        """
        # Parse document for instructions
        instructions_by_process = self.parse_document(text)
        
        # Execute identified instructions
        execution_results = self.execute_instructions(instructions_by_process)
        
        # Generate summary
        summary = self.get_execution_summary()
        
        return {
            'document_length': len(text),
            'instructions_found': sum(len(instructions) for instructions in instructions_by_process.values()),
            'instructions_by_process': instructions_by_process,
            'execution_results': execution_results,
            'execution_summary': summary,
            'processed_at': datetime.now().isoformat()
        }


def create_sample_documents():
    """Create sample documents with various types of instructions for testing."""
    
    sample_docs = {
        'project_setup.txt': """
Project Setup Instructions

1. Create a new project directory called "my_project"
2. Download the requirements file from the server
3. Install all dependencies using pip
4. Start the development server on port 8000
5. Send notification email to team@company.com when setup is complete

Additional tasks:
• Analyze the log files for any errors
• Filter out warnings from the error logs
• Generate a summary report of the installation process
        """,
        
        'data_pipeline.txt': """
Data Processing Pipeline

First, fetch the daily sales data from the API endpoint
Then, transform the data by removing duplicates and null values
Next, analyze customer behavior patterns
After analysis, create visualizations for key metrics
Finally, upload the processed results to the cloud storage

If errors occur, then alert the operations team immediately
        """,
        
        'maintenance_procedure.txt': """
System Maintenance Procedure

- Stop all running services gracefully
- Create backup of the database
- Run system diagnostics
- Update all software packages
- Restart services in the correct order
- Verify all systems are operational
- Email status report to administrators
        """
    }
    
    # Create sample documents directory
    sample_dir = '/tmp/sample_documents'
    os.makedirs(sample_dir, exist_ok=True)
    
    for filename, content in sample_docs.items():
        with open(os.path.join(sample_dir, filename), 'w') as f:
            f.write(content.strip())
    
    return sample_dir


# Example usage and testing function
if __name__ == "__main__":
    # Create AI agent
    agent = DocumentProcessor()
    
    # Create sample documents
    sample_dir = create_sample_documents()
    print(f"Sample documents created in: {sample_dir}")
    
    # Process a sample document
    sample_text = """
    Data Processing Instructions:
    
    1. Fetch user data from the database
    2. Filter active users only
    3. Analyze user engagement metrics
    4. Create visualization charts
    5. Send report to management team
    
    If processing fails, then alert the technical team
    """
    
    print("\nProcessing sample document...")
    results = agent.process_document(sample_text)
    
    print(f"\nDocument Analysis Results:")
    print(f"Instructions found: {results['instructions_found']}")
    print(f"Processes identified: {list(results['instructions_by_process'].keys())}")
    
    print(f"\nExecution Summary:")
    summary = results['execution_summary']
    print(f"Total executions: {summary['total']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success rate: {summary['success_rate']:.1f}%")
    
    print(f"\nDetailed Execution Results:")
    for result in results['execution_results']:
        status_icon = "✅" if result['success'] else "❌"
        print(f"{status_icon} [{result['process_type']}] {result['instruction']} -> {result['status']}")