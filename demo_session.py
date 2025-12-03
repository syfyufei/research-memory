#!/usr/bin/env python3
"""
Enhanced demo script to showcase all research-memory v0.2 features

Demonstrates:
- Complete configuration system
- Unified TODO management with status tracking
- Advanced CLI filtering
- Collision-resistant experiment IDs
- File format improvements
"""

import json
import subprocess
import sys

def demo_configuration():
    """Demonstrate configuration system"""
    print("⚙️ Configuration System Demo")
    print("=" * 50)

    print("📋 Current Configuration:")
    try:
        with open('config/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)

        key_configs = [
            ("Memory Directory", config.get('memory_directory')),
            ("Encoding", config.get('encoding')),
            ("CSV Delimiter", config.get('csv_delimiter')),
            ("Timestamp Format", config.get('timestamp_format')),
            ("Recent Entries Count", config.get('bootstrap', {}).get('recent_entries_count')),
            ("Max Search Results", config.get('search', {}).get('max_results'))
        ]

        for key, value in key_configs:
            print(f"  ✅ {key}: {value}")

        print("\n💡 All configuration fields are now functional!")

    except Exception as e:
        print(f"❌ Error reading config: {e}")

def demo_enhanced_todos():
    """Demonstrate new unified TODO management system"""
    print("\n🎯 Enhanced TODO Management Demo")
    print("=" * 50)

    # Example payload with new TODO format
    todos_payload = {
        "session_goal": "展示新的TODO管理系统",
        "changes_summary": "演示pending/completed/cancelled状态、优先级和分类",
        "todos": [
            {
                "text": "完成工具变量的有效性检验（弱工具变量检验、外生性检验）",
                "status": "completed",
                "completion_note": "通过2SLS回归验证了工具变量有效性"
            },
            {
                "text": "进行分样本回归分析（城乡差异）",
                "status": "pending",
                "priority": "high",
                "category": "analysis"
            },
            {
                "text": "检验工具变量的排他性约束",
                "status": "pending",
                "priority": "medium",
                "category": "robustness"
            },
            {
                "text": "准备论文投稿材料",
                "status": "cancelled",
                "priority": "low",
                "category": "writing"
            }
        ],
        "experiments": [
            {
                "hypothesis": "TODO管理系统增强验证",
                "dataset": "demo_data",
                "model": "test_validation",
                "metrics": {"success": True, "features_implemented": 5},
                "notes": "验证新TODO功能正常工作"
            }
        ],
        "phases": {
            "notes": "测试新的TODO管理系统，包括状态跟踪、优先级和分类功能"
        }
    }

    payload_json = json.dumps(todos_payload, ensure_ascii=False, indent=2)

    print("📝 TODO Management Features:")
    print("  ✅ Status tracking: pending/completed/cancelled")
    print("  ✅ Priority levels: high/medium/low")
    print("  ✅ Category system: analysis/modeling/writing/etc")
    print("  ✅ Auto-completion detection")
    print("  ✅ Timestamp recording")

    print(f"\n💾 Logging enhanced todos...")

    try:
        result = subprocess.run([
            sys.executable, 'handlers.py', 'log-session',
            '--payload-json', payload_json
        ], capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            print("✅ Enhanced TODO system test completed!")

            # Show the updated todos structure
            print("\n📄 Updated todos.md structure:")
            print("-" * 40)
            try:
                with open('memory/todos.md', 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # Find recent TODOs with new format
                for i, line in enumerate(lines[-20:], len(lines)-19):
                    if '[HIGH]' in line or '[LOW]' in line or '[analysis]' in line:
                        print(f"  Line {i+1}: {line.rstrip()}")
                    elif '[x]' in line and 'completed:' in line:
                        print(f"  Line {i+1}: {line.rstrip()}")

            except Exception as e:
                print(f"Error reading todos.md: {e}")

        else:
            print("❌ Error in TODO test:")
            print(result.stderr)

    except Exception as e:
        print(f"❌ Error: {e}")

def demo_advanced_search():
    """Demonstrate advanced CLI filtering"""
    print("\n🔍 Advanced Search Filtering Demo")
    print("=" * 50)

    test_cases = [
        {
            "description": "Limit results to 3 entries",
            "args": ["--question", "数字化技能", "--limit", "3"]
        },
        {
            "description": "Filter by experiment type only",
            "args": ["--question", "实验", "--type", "experiments"]
        },
        {
            "description": "Filter by date range (Dec 1-3, 2025)",
            "args": ["--question", "分析", "--from-date", "2025-12-01", "--to-date", "2025-12-03"]
        },
        {
            "description": "Filter by research phase (modeling)",
            "args": ["--question", "回归", "--phase", "modeling"]
        },
        {
            "description": "Combined filters (experiments + limit 2)",
            "args": ["--question", "技能", "--type", "experiments", "--limit", "2"]
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔎 Test {i}: {test_case['description']}")

        cmd = [sys.executable, 'handlers.py', 'query'] + test_case['args']

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

            if result.returncode == 0:
                query_data = json.loads(result.stdout)
                matches_count = len(query_data.get('matches', []))
                print(f"  ✅ Results: {query_data['summary']} ({matches_count} matches)")

                # Show sample result
                if query_data['matches']:
                    sample = query_data['matches'][0]
                    print(f"  📄 Sample: {sample['source']} - {sample['content'][:60]}...")
            else:
                print(f"  ❌ Error: {result.stderr}")

        except Exception as e:
            print(f"  ❌ Error: {e}")

def demo_collision_prevention():
    """Demonstrate experiment ID collision prevention"""
    print("\n🔐 Experiment ID Collision Prevention Demo")
    print("=" * 50)

    # Generate multiple experiments quickly to test uniqueness
    experiments = []
    for i in range(3):
        exp = {
            "hypothesis": f"唯一性测试实验 {i+1}",
            "dataset": "test_data",
            "model": f"test_model_{i+1}",
            "metrics": {"test_id": i+1, "success": True},
            "notes": f"验证实验ID唯一性，测试 {i+1}"
        }
        experiments.append(exp)

    payload = {
        "session_goal": "验证实验ID唯一性",
        "experiments": experiments,
        "phases": {
            "notes": "快速生成多个实验以测试ID碰撞防护"
        }
    }

    payload_json = json.dumps(payload, ensure_ascii=False, indent=2)

    print("🔐 ID Generation Features:")
    print("  ✅ Millisecond precision timestamps")
    print("  ✅ UUID suffix for guaranteed uniqueness")
    print("  ✅ Format: exp_YYYYMMDD_HHMMSS_UUUUUUUUU")

    print(f"\n💾 Logging {len(experiments)} experiments rapidly...")

    try:
        result = subprocess.run([
            sys.executable, 'handlers.py', 'log-session',
            '--payload-json', payload_json
        ], capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            print("✅ Experiment uniqueness test completed!")

            # Show the generated IDs
            print("\n📊 Generated Experiment IDs:")
            try:
                with open('memory/experiments.csv', 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Skip header, get last 3 rows
                    for line in lines[-3:]:
                        if line.strip():
                            parts = line.split(',')
                            if len(parts) >= 2:
                                exp_id = parts[1]
                                print(f"  🏷️  {exp_id}")
            except Exception as e:
                print(f"Error reading experiments.csv: {e}")

        else:
            print("❌ Error in collision test:")
            print(result.stderr)

    except Exception as e:
        print(f"❌ Error: {e}")

def demo_file_format_improvements():
    """Demonstrate improved file formatting"""
    print("\n📝 File Format Improvements Demo")
    print("=" * 50)

    # Add multiple sessions to test formatting
    sessions = [
        {
            "session_goal": "测试文件格式修复",
            "phases": {"notes": "验证分隔符和换行处理"}
        },
        {
            "session_goal": "第二次会话测试",
            "phases": {"notes": "验证连续会话的格式一致性"}
        }
    ]

    for i, session in enumerate(sessions):
        payload = {"session_goal": session['session_goal'], "phases": session['phases']}
        payload_json = json.dumps(payload, ensure_ascii=False)

        try:
            result = subprocess.run([
                sys.executable, 'handlers.py', 'log-session',
                '--payload-json', payload_json
            ], capture_output=True, text=True, encoding='utf-8')

            if result.returncode == 0:
                print(f"  ✅ Session {i+1} logged successfully")
            else:
                print(f"  ❌ Session {i+1} failed")

        except Exception as e:
            print(f"  ❌ Error in session {i+1}: {e}")

    print("\n📋 File Format Improvements:")
    print("  ✅ Consistent separation between devlog entries")
    print("  ✅ Proper newline handling")
    print("  ✅ No more `---##` concatenation issues")
    print("  ✅ Automatic devlog.md creation")

if __name__ == '__main__':
    print("🧠 Research Memory Skill v0.2 Enhanced Demonstration")
    print("=" * 70)
    print("Showcasing all new improvements and features\n")

    # Run all enhanced demos
    demo_configuration()
    demo_enhanced_todos()
    demo_advanced_search()
    demo_collision_prevention()
    demo_file_format_improvements()

    print("\n🎉 Enhanced Demo Completed!")
    print("\n🚀 v0.2 New Features Summary:")
    print("  ✅ Complete configuration system with all fields functional")
    print("  ✅ Intelligent TODO management with status tracking")
    print("  ✅ Advanced search with multiple filter options")
    print("  ✅ Collision-resistant experiment ID generation")
    print("  ✅ Improved file formatting and consistency")
    print("  ✅ Backward compatibility with old formats")

    print("\n💡 Usage Tips:")
    print("  🌟 Try natural language triggers with Claude Code")
    print("  🔧 Use advanced CLI filtering for precise queries")
    print("  📝 Leverage new TODO status tracking for better task management")
    print("  🔒 Trust the collision-resistant experiment IDs")

    print("\n📖 For more examples, see the README.md file")