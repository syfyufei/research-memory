#!/usr/bin/env python3
"""
Research Memory Skill Handlers

Core implementation for academic research project memory management.
Provides tools for context bootstrap, session logging, and historical querying.

Author: Yufei Sun (Adrian) <syfyufei@gmail.com>
Version: 0.1.0
"""

import os
import json
import csv
import re
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import argparse
import sys
import uuid

# Research phases supported by the skill
RESEARCH_PHASES = [
    "DGP", "data_preprocess", "data_analyse", "modeling",
    "robustness", "writing", "infra", "notes"
]

# Default configuration
DEFAULT_CONFIG = {
    "memory_directory": "memory",
    "timestamp_format": "ISO8601",
    "csv_delimiter": ",",
    "encoding": "utf-8",
    "bootstrap": {
        "recent_entries_count": 5,
        "include_todos": True,
        "suggest_work_plan": True
    },
    "logging": {
        "auto_timestamp": True,
        "phase_sections": RESEARCH_PHASES,
        "experiment_schema": ["hypothesis", "dataset", "model", "metrics", "notes"]
    },
    "search": {
        "max_results": 10,
        "include_context": True,
        "context_lines": 3
    }
}


class MemoryBackend:
    """
    Abstract memory backend interface for future extensibility.
    v0 implementation uses local files, but this allows easy migration to v1.
    """

    def __init__(self, memory_dir: Optional[str] = None):
        self.config = self._load_config()

        # Use configured memory directory or parameter
        if memory_dir is None:
            memory_dir = self.config.get("memory_directory", "memory")

        self.memory_dir = Path(memory_dir)

        # Store configuration options for easy access
        self.encoding = self.config.get("encoding", "utf-8")
        self.csv_delimiter = self.config.get("csv_delimiter", ",")
        self.timestamp_format = self.config.get("timestamp_format", "ISO8601")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json or use defaults."""
        config_path = Path("config/config.json")
        config = DEFAULT_CONFIG.copy()

        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)

                # Deep merge user config with defaults
                self._deep_merge(config, user_config)
                return config

            except Exception as e:
                print(f"Warning: Could not load config from {config_path}, using defaults. Error: {e}")

        return config

    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """Deep merge update dict into base dict."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def ensure_memory_directory(self):
        """Create memory directory and files if they don't exist."""
        self.memory_dir.mkdir(exist_ok=True)

        # Create default files if they don't exist
        default_files = {
            "project-overview.md": self._get_default_project_overview(),
            "devlog.md": "# Development Log\n\n",
            "decisions.md": "# Key Decisions\n\n",
            "todos.md": "# TODO Items and Open Questions\n\n",
            "experiments.csv": self._get_default_experiments_csv()
        }

        for filename, content in default_files.items():
            file_path = self.memory_dir / filename
            if not file_path.exists():
                with open(file_path, 'w', encoding=self.encoding) as f:
                    f.write(content)

    def _get_default_project_overview(self) -> str:
        """Generate default project overview content."""
        return """# Project Overview

## Research Questions

## Hypotheses

## Datasets

## Methodology

## Key Variables

## Code Structure

## Project Status
*Initial setup - ready for research documentation*

---

*Last updated: {timestamp}*
""".format(timestamp=datetime.now(timezone.utc).isoformat())

    def _get_default_experiments_csv(self) -> str:
        """Generate default experiments CSV with headers."""
        headers = [
            "timestamp", "experiment_id", "hypothesis", "dataset",
            "model", "spec", "metrics", "notes", "research_phase"
        ]
        return ",".join(headers) + "\n"

    def _get_timestamp(self) -> str:
        """Get current timestamp based on configured format."""
        now = datetime.now(timezone.utc)

        if self.timestamp_format == "ISO8601":
            return now.isoformat()
        elif self.timestamp_format == "YYYY-MM-DD_HH-MM-SS":
            return now.strftime("%Y-%m-%d_%H-%M-%S")
        elif self.timestamp_format == "timestamp":
            return str(int(now.timestamp()))
        else:
            # Default to ISO8601 for unknown formats
            return now.isoformat()

    def _process_todos(self, todos_payload: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Process unified TODO payload with status tracking.

        Args:
            todos_payload: List of TODO items with status information

        Returns:
            Tuple of (new_todos, completed_todos)
        """
        new_todos = []
        completed_todos = []

        for todo in todos_payload:
            todo_status = todo.get('status', 'pending').lower()

            if todo_status == 'completed':
                completed_todos.append(todo)
            elif todo_status in ['pending', 'cancelled']:
                new_todos.append(todo)

        return new_todos, completed_todos

    def _update_todos_file(self, new_todos: List[Dict[str, Any]], completed_todos: List[Dict[str, Any]], timestamp: str) -> None:
        """
        Update todos.md with new and completed items.

        Args:
            new_todos: List of new TODO items to add
            completed_todos: List of TODO items to mark as completed
            timestamp: Current timestamp for marking completion time
        """
        todos_path = self.memory_dir / "todos.md"

        # Read existing todos if file exists
        existing_content = ""
        if todos_path.exists():
            with open(todos_path, 'r', encoding=self.encoding) as f:
                existing_content = f.read()

        # Process completed todos - find and mark them as complete
        if completed_todos:
            lines = existing_content.split('\n')
            updated_lines = []

            for line in lines:
                line_stripped = line.strip()
                is_todo_item = re.match(r'^-\s*\[\s*\]', line_stripped)

                if is_todo_item:
                    # Extract TODO text
                    todo_text = re.sub(r'^-\s*\[\s*\]\s*', '', line_stripped)

                    # Check if this TODO should be marked as completed
                    for completed_todo in completed_todos:
                        completed_text = completed_todo.get('text', '').strip()
                        completion_note = completed_todo.get('completion_note', '')

                        if todo_text == completed_text:
                            # Mark as completed with timestamp
                            timestamp_short = timestamp[:10]
                            completion_entry = f"- [x] {todo_text} (completed: {timestamp_short}"
                            if completion_note:
                                completion_entry += f" - {completion_note}"
                            completion_entry += ")"
                            updated_lines.append(completion_entry)
                            break
                    else:
                        # No match found, keep original line
                        updated_lines.append(line)
                else:
                    # Not a TODO item, keep as is
                    updated_lines.append(line)

            existing_content = '\n'.join(updated_lines)

        # Add new todos
        if new_todos:
            # Prepare new todos section
            new_todos_section = f"\n### {timestamp[:10]} {timestamp[11:16]}\n\n"

            for todo in new_todos:
                todo_text = todo.get('text', '')
                priority = todo.get('priority', 'medium')
                category = todo.get('category', '')

                # Format with priority and category if specified
                todo_entry = "- [ ]"
                if priority != 'medium':
                    todo_entry += f" [{priority.upper()}]"
                if category:
                    todo_entry += f" [{category}]"
                todo_entry += f" {todo_text}"

                new_todos_section += todo_entry + "\n"

            new_todos_section += "\n"

            # Append to existing content
            existing_content += new_todos_section

        # Write updated content back to file
        with open(todos_path, 'w', encoding=self.encoding) as f:
            f.write(existing_content)

    def _generate_experiment_id(self) -> str:
        """
        Generate collision-resistant experiment ID using timestamp + UUID.

        Returns:
            Unique experiment ID in format: exp_YYYYMMDD_HHMMSS_UUID
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')
        unique_suffix = uuid.uuid4().hex[:8]  # Use 8 characters for better uniqueness
        return f"exp_{timestamp}_{unique_suffix}"


def bootstrap_context(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Bootstrap project context from memory files.

    Args:
        config: Optional configuration dictionary

    Returns:
        Dictionary containing project context, recent progress, and suggestions
    """
    backend = MemoryBackend()
    backend.ensure_memory_directory()

    recent_entries_count = backend.config["bootstrap"]["recent_entries_count"]
    include_todos = backend.config["bootstrap"]["include_todos"]
    suggest_work_plan = backend.config["bootstrap"]["suggest_work_plan"]

    result = {
        "project_context": "",
        "recent_progress": [],
        "current_todos": [],
        "work_plan_suggestions": [],
        "timestamp": backend._get_timestamp()
    }

    # Read project overview
    overview_path = backend.memory_dir / "project-overview.md"
    if overview_path.exists():
        with open(overview_path, 'r', encoding=backend.encoding) as f:
            result["project_context"] = f.read()

    # Read recent devlog entries
    devlog_path = backend.memory_dir / "devlog.md"
    if devlog_path.exists():
        with open(devlog_path, 'r', encoding=backend.encoding) as f:
            content = f.read()

        # Extract recent entries (simplified - looks for date headers)
        entries = re.findall(r'^## \d{4}-\d{2}-\d{2}.*?(?=^## |\Z)', content, re.MULTILINE | re.DOTALL)
        result["recent_progress"] = entries[-recent_entries_count:] if entries else []

    # Read current todos
    if include_todos:
        todos_path = backend.memory_dir / "todos.md"
        if todos_path.exists():
            with open(todos_path, 'r', encoding=backend.encoding) as f:
                content = f.read()

            # Extract TODO items (lines with - [ ] or - [x])
            todo_lines = []
            for line in content.split('\n'):
                if re.match(r'^\s*-\s*\[[ x]\]', line):
                    todo_lines.append(line.strip())
            result["current_todos"] = todo_lines

    # Generate work plan suggestions (basic implementation)
    if suggest_work_plan:
        suggestions = []

        # Analyze recent progress for patterns
        if result["recent_progress"]:
            suggestions.append("Review and analyze recent experimental results")

        # Check for open todos
        incomplete_todos = [todo for todo in result["current_todos"] if "[ ]" in todo]
        if incomplete_todos:
            suggestions.append(f"Address {len(incomplete_todos)} open TODO items")

        if not suggestions:
            suggestions.append("Continue with planned research activities")

        result["work_plan_suggestions"] = suggestions

    return result


def log_session(payload: Dict[str, Any]) -> None:
    """
    Log a research session to memory files.

    Args:
        payload: Dictionary containing session information including:
            - session_goal: Main objective
            - changes_summary: Summary of changes
            - experiments: List of experiment records
            - decisions: List of decisions with rationale
            - todos: List of TODO items
            - phases: Dict mapping research phases to descriptions
    """
    backend = MemoryBackend()
    backend.ensure_memory_directory()

    timestamp = backend._get_timestamp()
    date_header = f"## {timestamp[:10]} {timestamp[11:16]}"

    # Update devlog.md
    devlog_path = backend.memory_dir / "devlog.md"

    # Ensure devlog.md exists and has proper format
    if not devlog_path.exists():
        with open(devlog_path, 'w', encoding=backend.encoding) as f:
            f.write("# Development Log\n\n")

    # Read existing content to check ending
    with open(devlog_path, 'r', encoding=backend.encoding) as f:
        existing_content = f.read()

    # Create session entry with proper separation
    session_entry = f"{date_header}\n\n"
    session_entry += f"**Session Goal**: {payload.get('session_goal', 'Not specified')}\n\n"
    session_entry += f"**Changes Summary**: {payload.get('changes_summary', 'No changes recorded')}\n\n"

    # Add research phase sections
    phases = payload.get('phases', {})
    for phase in backend.config["logging"]["phase_sections"]:
        if phase in phases and phases[phase]:
            session_entry += f"### {phase.upper()}\n{phases[phase]}\n\n"

    session_entry += "---\n\n"

    # Ensure proper separation from existing content
    if existing_content and not existing_content.endswith('\n\n'):
        # Add separation if needed
        with open(devlog_path, 'a', encoding=backend.encoding) as f:
            f.write('\n' + session_entry)
    else:
        # Append normally
        with open(devlog_path, 'a', encoding=backend.encoding) as f:
            f.write(session_entry)

    # Update experiments.csv
    experiments = payload.get('experiments', [])
    if experiments:
        experiments_path = backend.memory_dir / "experiments.csv"

        with open(experiments_path, 'a', newline='', encoding=backend.encoding) as csvfile:
            writer = csv.writer(csvfile, delimiter=backend.csv_delimiter)

            for exp in experiments:
                row = [
                    timestamp,
                    backend._generate_experiment_id(),
                    exp.get('hypothesis', ''),
                    exp.get('dataset', ''),
                    exp.get('model', ''),
                    exp.get('spec', ''),
                    json.dumps(exp.get('metrics', {})),
                    exp.get('notes', ''),
                    ','.join(phases.keys()) if phases else ''
                ]
                writer.writerow(row)

    # Update decisions.md
    decisions = payload.get('decisions', [])
    if decisions:
        decisions_path = backend.memory_dir / "decisions.md"

        with open(decisions_path, 'a', encoding=backend.encoding) as f:
            for decision in decisions:
                decision_entry = f"""## {timestamp}

**Decision**: {decision.get('decision', '')}

**Rationale**: {decision.get('rationale', '')}

**Alternatives Considered**: {', '.join(decision.get('alternatives_considered', []))}

---

"""
                f.write(decision_entry)

    # Update todos.md with unified TODO management
    todos = payload.get('todos', [])
    if todos:
        # Handle both old format (list of strings) and new format (list of dicts)
        if todos and isinstance(todos[0], str):
            # Convert old format to new unified format
            unified_todos = [{"text": todo, "status": "pending"} for todo in todos]
        else:
            # Already in new format
            unified_todos = todos

        # Process todos and update file
        new_todos, completed_todos = backend._process_todos(unified_todos)
        backend._update_todos_file(new_todos, completed_todos, timestamp)


def query_history(query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Query research history for relevant information.

    Args:
        query: Search query string
        filters: Optional filters (date_range, phase, content_type, limit)

    Returns:
        Dictionary containing search results and summaries
    """
    backend = MemoryBackend()
    backend.ensure_memory_directory()

    # Apply filters or use defaults
    if filters is None:
        filters = {}

    max_results = filters.get('limit', backend.config["search"]["max_results"])
    include_context = backend.config["search"]["include_context"]
    context_lines = backend.config["search"]["context_lines"]

    # Parse date filters
    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    phase_filter = filters.get('phase')
    type_filter = filters.get('type')

    # Simple keyword-based search (v0 implementation)
    keywords = re.findall(r'\w+', query.lower())

    results = {
        "query": query,
        "matches": [],
        "summary": "",
        "timestamp": backend._get_timestamp()
    }

    # Search based on type filter
    if not type_filter or type_filter == "devlog":
        devlog_path = backend.memory_dir / "devlog.md"
        if devlog_path.exists():
            matches = _search_in_file(devlog_path, keywords, "devlog", include_context, context_lines, backend.encoding)
            # Apply date and phase filters to devlog results
            filtered_matches = _apply_filters_to_matches(matches, from_date, to_date, phase_filter)
            results["matches"].extend(filtered_matches)

    if not type_filter or type_filter == "decisions":
        decisions_path = backend.memory_dir / "decisions.md"
        if decisions_path.exists():
            matches = _search_in_file(decisions_path, keywords, "decisions", include_context, context_lines, backend.encoding)
            filtered_matches = _apply_filters_to_matches(matches, from_date, to_date, phase_filter)
            results["matches"].extend(filtered_matches)

    if not type_filter or type_filter == "experiments":
        experiments_path = backend.memory_dir / "experiments.csv"
        if experiments_path.exists():
            matches = _search_in_csv(experiments_path, keywords, "experiments", backend.encoding, backend.csv_delimiter)
            filtered_matches = _apply_filters_to_matches(matches, from_date, to_date, phase_filter)
            results["matches"].extend(filtered_matches)

    # Sort by relevance (simplified - count keyword matches)
    results["matches"].sort(key=lambda x: x.get("relevance", 0), reverse=True)
    results["matches"] = results["matches"][:max_results]

    # Generate summary
    if results["matches"]:
        results["summary"] = f"Found {len(results['matches'])} relevant entries for '{query}'"
    else:
        results["summary"] = f"No entries found matching '{query}'"

    return results


def _search_in_file(file_path: Path, keywords: List[str], source_type: str,
                   include_context: bool, context_lines: int, encoding: str = 'utf-8') -> List[Dict[str, Any]]:
    """Search for keywords in a text file."""
    matches = []

    try:
        with open(file_path, 'r', encoding=encoding) as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            line_lower = line.lower()
            keyword_matches = sum(1 for kw in keywords if kw in line_lower)

            if keyword_matches > 0:
                match = {
                    "source": source_type,
                    "line_number": i + 1,
                    "relevance": keyword_matches,
                    "content": line.strip()
                }

                if include_context:
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    context = ''.join(lines[start:end]).strip()
                    match["context"] = context

                matches.append(match)

    except Exception as e:
        print(f"Warning: Could not search {file_path}: {e}")

    return matches


def _search_in_csv(file_path: Path, keywords: List[str], source_type: str,
                   encoding: str = 'utf-8', csv_delimiter: str = ',') -> List[Dict[str, Any]]:
    """Search for keywords in a CSV file."""
    matches = []

    try:
        with open(file_path, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f, delimiter=csv_delimiter)

            for i, row in enumerate(reader):
                # Search all fields for keywords
                row_text = ' '.join(str(value) for value in row.values()).lower()
                keyword_matches = sum(1 for kw in keywords if kw in row_text)

                if keyword_matches > 0:
                    match = {
                        "source": source_type,
                        "row_number": i + 2,  # +2 because CSV reader is 0-indexed and header is row 1
                        "relevance": keyword_matches,
                        "content": f"Experiment: {row.get('experiment_id', 'N/A')} - {row.get('hypothesis', 'N/A')}"
                    }

                    # Add relevant fields as context
                    relevant_fields = ['timestamp', 'hypothesis', 'dataset', 'model', 'metrics', 'notes']
                    context = {field: row.get(field, '') for field in relevant_fields if row.get(field)}
                    match["context"] = context

                    matches.append(match)

    except Exception as e:
        print(f"Warning: Could not search {file_path}: {e}")

    return matches


# CLI interface
def main():
    """Command-line interface for the research memory skill."""
    parser = argparse.ArgumentParser(description='Research Memory Skill CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Bootstrap command
    subparsers.add_parser('bootstrap', help='Bootstrap project context')

    # Log session command
    log_parser = subparsers.add_parser('log-session', help='Log a research session')
    log_parser.add_argument('--payload-json', required=True, help='JSON payload for session logging')

    # Query command
    query_parser = subparsers.add_parser('query', help='Query research history')
    query_parser.add_argument('--question', required=True, help='Search query')
    query_parser.add_argument('--from-date', help='Filter from date (YYYY-MM-DD)')
    query_parser.add_argument('--to-date', help='Filter to date (YYYY-MM-DD)')
    query_parser.add_argument('--phase', choices=RESEARCH_PHASES, help='Filter by research phase')
    query_parser.add_argument('--type', choices=['devlog', 'decisions', 'experiments'], help='Filter by content type')
    query_parser.add_argument('--limit', type=int, help='Maximum number of results')

    args = parser.parse_args()

    if args.command == 'bootstrap':
        result = bootstrap_context()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == 'log-session':
        try:
            payload = json.loads(args.payload_json)
            log_session(payload)
            print("Session logged successfully")
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON payload - {e}")
            sys.exit(1)

    elif args.command == 'query':
        # Build filters from arguments
        filters = {}
        if hasattr(args, 'from_date') and args.from_date:
            filters['from_date'] = args.from_date
        if hasattr(args, 'to_date') and args.to_date:
            filters['to_date'] = args.to_date
        if hasattr(args, 'phase') and args.phase:
            filters['phase'] = args.phase
        if hasattr(args, 'type') and args.type:
            filters['type'] = args.type
        if hasattr(args, 'limit') and args.limit:
            filters['limit'] = args.limit

        result = query_history(args.question, filters)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        parser.print_help()
        sys.exit(1)


def _apply_filters_to_matches(matches: List[Dict[str, Any]], from_date: Optional[str],
                             to_date: Optional[str], phase_filter: Optional[str]) -> List[Dict[str, Any]]:
    """
    Apply date and phase filters to search matches.

    Args:
        matches: List of search matches
        from_date: Filter start date (YYYY-MM-DD format)
        to_date: Filter end date (YYYY-MM-DD format)
        phase_filter: Filter by research phase

    Returns:
        Filtered list of matches
    """
    filtered_matches = []

    for match in matches:
        # Extract date from match
        match_date = None

        if 'timestamp' in match:
            # For experiments.csv matches
            match_date = match['timestamp'][:10]
        elif 'context' in match:
            # For devlog/decisions matches, try to extract date from context
            context = match['context'] if isinstance(match['context'], str) else str(match['context'])
            # Look for date patterns like "## 2025-11-27" or "2025-11-27T"
            date_match = re.search(r'##\s*(\d{4}-\d{2}-\d{2})|(\d{4}-\d{2}-\d{2})T', context)
            if date_match:
                match_date = date_match.group(1) or date_match.group(2)

        # Apply date filter
        if from_date and match_date:
            if match_date < from_date:
                continue

        if to_date and match_date:
            if match_date > to_date:
                continue

        # Apply phase filter
        if phase_filter:
            content = match.get('content', '')
            context = match.get('context', '')
            if not isinstance(context, str):
                context = str(context)
            content += context
            if phase_filter.lower() not in content.lower():
                continue

        filtered_matches.append(match)

    return filtered_matches


if __name__ == '__main__':
    main()