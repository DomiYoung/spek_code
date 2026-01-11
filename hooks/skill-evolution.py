#!/usr/bin/env python3
"""
Skill 进化检测 Hook（Stop 事件）
Session 结束时检测 Skill 激活情况，建议更新 description
"""

import json
import sys
import os
from datetime import datetime

def main():
    """
    Stop 事件触发时执行
    分析本次 Session 的 Skill 使用情况，建议进化
    """
    session_data = {}
    try:
        if not sys.stdin.isatty():
            data = sys.stdin.read()
            if data:
                try:
                    session_data = json.loads(data)
                except json.JSONDecodeError:
                    pass
    except Exception:
        pass
    
    # 提取 Session 信息
    transcript_path = session_data.get('transcript_path', '')
    
    # 输出进化提醒
    output = {
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": f"""
📚 **Skill 进化检查**

Session 结束前，请回答以下问题：

1. **本次是否有 Skill 应该激活但未激活？**
   - 如果有，考虑更新该 Skill 的 description，添加触发词
   
2. **本次是否手动调用了某个 Skill？**
   - 如果是，说明 description 不够清晰，需要改进
   
3. **本次是否学到了新的踩坑经验？**
   - 知识四问：可复用？费力？有帮助？未文档化？
   - 2+ YES → 写入对应 SKILL.md + Evolution Marker

**Evolution Marker 格式**:
```
<!-- Evolution: {datetime.now().strftime('%Y-%m-%d')} | source: {{project}} | trigger: description-improvement | author: @user -->
```
"""
        }
    }
    print(json.dumps(output))

if __name__ == "__main__":
    main()
