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

# Research phases supported by the skill
RESEARCH_PHASES = [
    "DGP", "data_preprocess", "data_analyse", "modeling",
    "robustness", "writing", "infra", "notes"
]

# Default configuration
DEFAULT_CONFIG = {
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

    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = Path(memory_dir)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json or use defaults."""
        config_path = Path("config/config.json")
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                # Merge with defaults
                config = DEFAULT_CONFIG.copy()
                for section, values in user_config.items():
                    if section in config:
                        config[section].update(values)
                    else:
                        config[section] = values
                return config
            except Exception as e:
                print(f"Warning: Could not load config, using defaults. Error: {e}")

        return DEFAULT_CONFIG

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
                with open(file_path, 'w', encoding='utf-8') as f:
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

    def _get_iso_timestamp(self) -> str:
        """Get current ISO 8601 timestamp."""
        return datetime.now(timezone.utc).isoformat()


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
        "timestamp": backend._get_iso_timestamp()
    }

    # Read project overview
    overview_path = backend.memory_dir / "project-overview.md"
    if overview_path.exists():
        with open(overview_path, 'r', encoding='utf-8') as f:
            result["project_context"] = f.read()

    # Read recent devlog entries
    devlog_path = backend.memory_dir / "devlog.md"
    if devlog_path.exists():
        with open(devlog_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract recent entries (simplified - looks for date headers)
        entries = re.findall(r'^## \d{4}-\d{2}-\d{2}.*?(?=^## |\Z)', content, re.MULTILINE | re.DOTALL)
        result["recent_progress"] = entries[-recent_entries_count:] if entries else []

    # Read current todos
    if include_todos:
        todos_path = backend.memory_dir / "todos.md"
        if todos_path.exists():
            with open(todos_path, 'r', encoding='utf-8') as f:
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

    timestamp = backend._get_iso_timestamp()
    date_header = f"## {timestamp[:10]} {timestamp[11:16]}"

    # Update devlog.md
    devlog_path = backend.memory_dir / "devlog.md"

    # Create session entry
    session_entry = f"""{date_header}

**Session Goal**: {payload.get('session_goal', 'Not specified')}

**Changes Summary**: {payload.get('changes_summary', 'No changes recorded')}

"""

    # Add research phase sections
    phases = payload.get('phases', {})
    for phase in backend.config["logging"]["phase_sections"]:
        if phase in phases and phases[phase]:
            session_entry += f"### {phase.upper()}\n{phases[phase]}\n\n"

    # Append to devlog
    with open(devlog_path, 'a', encoding='utf-8') as f:
        f.write(session_entry + "---\n\n")

    # Update experiments.csv
    experiments = payload.get('experiments', [])
    if experiments:
        experiments_path = backend.memory_dir / "experiments.csv"

        with open(experiments_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            for exp in experiments:
                row = [
                    timestamp,
                    f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
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

        with open(decisions_path, 'a', encoding='utf-8') as f:
            for decision in decisions:
                decision_entry = f"""## {timestamp}

**Decision**: {decision.get('decision', '')}

**Rationale**: {decision.get('rationale', '')}

**Alternatives Considered**: {', '.join(decision.get('alternatives_considered', []))}

---

"""
                f.write(decision_entry)

    # Update todos.md
    todos = payload.get('todos', [])
    if todos:
        todos_path = backend.memory_dir / "todos.md"

        with open(todos_path, 'a', encoding='utf-8') as f:
            f.write(f"\n### {timestamp[:10]} {timestamp[11:16]}\n\n")
            for todo in todos:
                f.write(f"- [ ] {todo}\n")
            f.write("\n")


def query_history(query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Query research history for relevant information.

    Args:
        query: Search query string
        filters: Optional filters (date_range, phase, content_type)

    Returns:
        Dictionary containing search results and summaries
    """
    backend = MemoryBackend()
    backend.ensure_memory_directory()

    max_results = backend.config["search"]["max_results"]
    include_context = backend.config["search"]["include_context"]
    context_lines = backend.config["search"]["context_lines"]

    # Simple keyword-based search (v0 implementation)
    keywords = re.findall(r'\w+', query.lower())

    results = {
        "query": query,
        "matches": [],
        "summary": "",
        "timestamp": backend._get_iso_timestamp()
    }

    # Search devlog.md
    devlog_path = backend.memory_dir / "devlog.md"
    if devlog_path.exists():
        matches = _search_in_file(devlog_path, keywords, "devlog", include_context, context_lines)
        results["matches"].extend(matches)

    # Search decisions.md
    decisions_path = backend.memory_dir / "decisions.md"
    if decisions_path.exists():
        matches = _search_in_file(decisions_path, keywords, "decisions", include_context, context_lines)
        results["matches"].extend(matches)

    # Search experiments.csv
    experiments_path = backend.memory_dir / "experiments.csv"
    if experiments_path.exists():
        matches = _search_in_csv(experiments_path, keywords, "experiments")
        results["matches"].extend(matches)

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
                   include_context: bool, context_lines: int) -> List[Dict[str, Any]]:
    """Search for keywords in a text file."""
    matches = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
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


def _search_in_csv(file_path: Path, keywords: List[str], source_type: str) -> List[Dict[str, Any]]:
    """Search for keywords in a CSV file."""
    matches = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

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
        result = query_history(args.question)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()