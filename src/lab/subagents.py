"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use when the task requires inspecting documentation, source files, data, or logs "
                "before deciding what to change; ask it to report evidence and likely edge cases."
            ),
            "system_prompt": (
                "You are a read-first investigator. Inspect the requested files and run only "
                "non-destructive diagnostic commands. Do not modify files. Return a concise, "
                "evidence-based report with exact paths, relevant conventions, and uncertainties."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use when a well-scoped code, data-cleaning, or log-processing change must be "
                "implemented and verified in the workspace."
            ),
            "system_prompt": (
                "You are an implementation specialist. Read the supplied requirements and relevant "
                "files, make only the requested workspace changes, and run focused tests or validation. "
                "Preserve unrelated behavior. Report changed paths, commands run, and remaining risks."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use after changes are made, or when an independent check of requirements, edge cases, "
                "and output formats is needed before declaring the task complete."
            ),
            "system_prompt": (
                "You are an independent reviewer. Do not edit files. Compare the current workspace "
                "against every supplied requirement, inspect diffs or outputs, and run relevant checks. "
                "Report concrete failures first, then passed checks and any residual uncertainty."
            ),
        },
    ]
