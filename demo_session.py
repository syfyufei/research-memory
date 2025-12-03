#!/usr/bin/env python3
"""
Demo script to demonstrate research-memory session logging
"""

import json
import subprocess
import sys

def demo_log_session():
    """Demonstrate logging a research session"""

    # Example session payload
    session_payload = {
        "session_goal": "完成工具变量分析和稳健性检验",
        "changes_summary": "使用父母教育水平作为工具变量，检验了教育内生性问题",
        "experiments": [
            {
                "hypothesis": "教育存在内生性，需要工具变量处理",
                "dataset": "CFPS_final",
                "model": "2SLS工具变量回归",
                "metrics": {
                    "first_stage_f": 28.4,
                    "education_coef_2sls": 0.078,
                    "education_coef_ols": 0.083,
                    "weak_instrument_test": "Passed",
                    "endogeneity_test": "Significant"
                },
                "notes": "工具变量有效，教育系数略降但依然显著"
            }
        ],
        "decisions": [
            {
                "decision": "采用父母教育水平作为工具变量",
                "rationale": "满足相关性和外生性假设，工具变量检验通过",
                "alternatives_considered": [
                    "早期学校质量指标",
                    "教育政策变化",
                    "地区平均教育水平"
                ]
            }
        ],
        "todos": [
            "进行分样本回归分析（城乡差异）",
            "检验工具变量的排他性约束",
            "更新结果表格中的工具变量部分"
        ],
        "phases": {
            "modeling": "执行2SLS回归，处理内生性问题",
            "robustness": "检验工具变量有效性和排他性约束",
            "data_analyse": "比较OLS和2SLS结果差异",
            "notes": "结果显示教育回报率存在轻微向下偏误"
        }
    }

    # Convert payload to JSON
    payload_json = json.dumps(session_payload, ensure_ascii=False, indent=2)

    print("🔬 Research Memory Session Logging Demo")
    print("=" * 50)
    print("\n📝 Session Details:")
    print(f"Goal: {session_payload['session_goal']}")
    print(f"Summary: {session_payload['changes_summary']}")

    print(f"\n🧪 Experiments ({len(session_payload['experiments'])}):")
    for exp in session_payload['experiments']:
        print(f"  - {exp['hypothesis']}")
        print(f"    Model: {exp['model']}")
        print(f"    Key result: F-stat={exp['metrics']['first_stage_f']}")

    print(f"\n🎯 Decisions ({len(session_payload['decisions'])}):")
    for decision in session_payload['decisions']:
        print(f"  - {decision['decision']}")

    print(f"\n✅ TODOs added ({len(session_payload['todos'])}):")
    for todo in session_payload['todos']:
        print(f"  - [ ] {todo}")

    print(f"\n📊 Research Phases:")
    for phase, content in session_payload['phases'].items():
        print(f"  - {phase.upper()}: {content[:50]}...")

    print("\n💾 Logging to research-memory...")

    # Call the handler
    try:
        result = subprocess.run([
            sys.executable, 'handlers.py', 'log-session',
            '--payload-json', payload_json
        ], capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            print("✅ Session logged successfully!")
            print("\n🔍 You can now query this session:")
            print("   python3 handlers.py query --question \"工具变量\"")
            print("   python3 handlers.py query --question \"2SLS\"")
        else:
            print("❌ Error logging session:")
            print(result.stderr)

    except Exception as e:
        print(f"❌ Error: {e}")

def demo_bootstrap():
    """Demonstrate bootstrapping project context"""

    print("\n🔄 Research Memory Bootstrap Demo")
    print("=" * 50)
    print("\n📋 Recovering project context...")

    try:
        result = subprocess.run([
            sys.executable, 'handlers.py', 'bootstrap'
        ], capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            bootstrap_data = json.loads(result.stdout)

            print(f"📅 Last updated: {bootstrap_data['timestamp'][:10]}")

            print(f"\n📈 Recent Progress ({len(bootstrap_data['recent_progress'])} entries):")
            for i, entry in enumerate(bootstrap_data['recent_progress'][-3:], 1):
                lines = entry.split('\n')
                goal_line = next((line for line in lines if 'Session Goal:' in line), '')
                if goal_line:
                    print(f"  {i}. {goal_line.replace('**Session Goal**: ', '').strip()}")

            print(f"\n✅ Current TODOs ({len(bootstrap_data['current_todos'])} total):")
            incomplete = [todo for todo in bootstrap_data['current_todos'] if '[ ]' in todo]
            completed = [todo for todo in bootstrap_data['current_todos'] if '[x]' in todo]
            print(f"  - Pending: {len(incomplete)}")
            print(f"  - Completed: {len(completed)}")

            print(f"\n💡 Work Plan Suggestions:")
            for suggestion in bootstrap_data['work_plan_suggestions']:
                print(f"  - {suggestion}")

        else:
            print("❌ Error bootstrapping context:")
            print(result.stderr)

    except Exception as e:
        print(f"❌ Error: {e}")

def demo_query():
    """Demonstrate querying research history"""

    print("\n🔍 Research Memory Query Demo")
    print("=" * 50)

    queries = [
        "数字化技能",
        "工具变量",
        "教育回报率",
        "稳健性检验"
    ]

    for query in queries:
        print(f"\n🔎 Querying: '{query}'")
        try:
            result = subprocess.run([
                sys.executable, 'handlers.py', 'query',
                '--question', query
            ], capture_output=True, text=True, encoding='utf-8')

            if result.returncode == 0:
                query_data = json.loads(result.stdout)
                print(f"  📊 Results: {query_data['summary']}")

                # Show top 2 matches
                for match in query_data['matches'][:2]:
                    print(f"    - {match['source']}: {match['content'][:80]}...")

            else:
                print(f"  ❌ Error: {result.stderr}")

        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == '__main__':
    print("🧠 Research Memory Skill Demonstration")
    print("=" * 60)

    # Run all demos
    demo_bootstrap()
    demo_log_session()
    demo_query()

    print("\n🎉 Demo completed!")
    print("\n💡 Next steps:")
    print("  1. Use natural language with Claude Code to trigger the skill")
    print("  2. Try: '帮我用 research-memory 恢复项目状态'")
    print("  3. Try: '记录刚才的实验结果'")
    print("  4. Try: '查询之前关于工具变量的讨论'")