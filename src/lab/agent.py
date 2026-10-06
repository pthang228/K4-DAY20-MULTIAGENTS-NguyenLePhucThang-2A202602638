"""GUIDE Phần 1 - Dựng tác tử (agent) bằng Deep Agents.   >>> SINH VIÊN CÀI ĐẶT make_backend VÀ build_agent <<<

Pseudo-code: guides/pseudocode/01_agent.md
Kiểm tra:    pytest tests/test_02_agent.py
"""
import os
import sys
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

from .model import make_model
from .subagents import get_subagents

# ---- CÓ SẴN, KHÔNG SỬA: system prompt dùng chung cho mọi sinh viên (để đường cơ sở so sánh được) ----
PATHS_NOTE = (
    "PATHS: every path is relative to the sandbox root and never starts with '/'. "
    "The task files are in the folder workspace/ (for example workspace/app.log). "
    "Use exactly this relative form both in the file tools and in the shell (execute); "
    "the shell starts in the sandbox root. "
)
BASE_PROMPT = (
    "You are an engineering assistant working in a sandbox. "
    + PATHS_NOTE
    + "Use the shell to run Python and tests. "
    "When you are done, reply with a short summary that mentions only files you really created or changed."
)
SKILLS_NOTE = (
    " Skills are in the folder skills/ (one sub-folder per skill with a SKILL.md). "
    "As your FIRST action, read the SKILL.md of every skill whose description could apply to the task, "
    "then follow them. Never modify skills/."
)
SUBAGENTS_NOTE = (
    " You have specialised subagents (see the description of the task tool). "
    "For anything beyond a trivial step, delegate to a suitable subagent and put ALL the task rules and file paths "
    "in the delegation message, because a subagent sees only what you send. "
    "Check what a subagent returns before you rely on it."
)
# --------------------------------------------------------------------------------------------------


def make_backend(sandbox: Path):
    """Tạo backend (môi trường thực thi) cho tác tử.

    Yêu cầu:
      - Thư mục gốc (root_dir) là `sandbox`; đường dẫn tương đối `workspace/...` và `skills/...`
        phải dùng được ở CẢ công cụ tệp lẫn shell (shell chạy với thư mục làm việc = `sandbox`).
      - Tác tử chạy được lệnh shell và gọi được `python` (cần đặt PATH).
      - KHÔNG chuyển biến môi trường của bạn vào shell của tác tử (khóa API không được lộ).
    """
    sandbox = Path(sandbox).resolve()

    # Start from a deliberately small environment.  In particular, do not copy
    # os.environ: it commonly contains provider API keys.  The Python directory
    # is included explicitly so the agent can run the same interpreter as the
    # harness.  The remaining entries are conventional system-tool locations.
    path_entries = [str(Path(sys.executable).resolve().parent)]
    if os.name == "nt":
        # Git for Windows supplies the Unix-like commands used by the lab tasks.
        # These paths are harmless when Git is not installed.
        path_entries.extend([
            str(Path(sys.executable).resolve().parents[1] / "native" / "git" / "usr" / "bin"),
            r"C:\Program Files\Git\usr\bin",
            r"C:\Windows\System32",
            r"C:\Windows",
        ])
    else:
        path_entries.extend(["/usr/local/bin", "/usr/bin", "/bin"])

    env = {
        "PATH": os.pathsep.join(path_entries),
        "HOME": str(sandbox),
        "PYTHONDONTWRITEBYTECODE": "1",
        # The lab workspaces do not rely on third-party pytest plugins.  Turning
        # off global auto-loading keeps their tests isolated from packages in
        # the harness environment.
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
    }
    if os.name == "nt":
        # CPython's socket/asyncio modules need the Windows system directory to
        # initialise Winsock.  Copy only this small allow-list of non-secret OS
        # settings; provider credentials and the rest of the parent environment
        # remain unavailable to the agent shell.
        env.update({
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", r"C:\Windows"),
            "WINDIR": os.environ.get("WINDIR", r"C:\Windows"),
            "COMSPEC": os.environ.get("COMSPEC", r"C:\Windows\System32\cmd.exe"),
            "TEMP": str(sandbox),
            "TMP": str(sandbox),
            "PATHEXT": ".COM;.EXE;.BAT;.CMD",
        })
    return LocalShellBackend(
        root_dir=sandbox,
        virtual_mode=True,
        inherit_env=False,
        env=env,
        timeout=120,
    )


def build_agent(sandbox: Path, mode: str = "single", use_skills: bool = False, model=None):
    """Tạo tác tử Deep Agents.

    Tham số:
      sandbox:    thư mục chứa `workspace/` (và `skills/` nếu có).
      mode:       "single"    -> tác tử mặc định (có subagent `general-purpose` sẵn của Deep Agents)
                  "subagents" -> thêm các subagent từ `get_subagents()` (nối PATHS_NOTE vào `system_prompt` của MỖI subagent,
                                 vì subagent không nhận BASE_PROMPT) và thêm SUBAGENTS_NOTE vào prompt chính
      use_skills: True -> nạp thư mục "/skills/" qua tham số `skills=` của create_deep_agent
                  và thêm SKILLS_NOTE vào prompt.
      model:      mô hình ngôn ngữ; None -> dùng `make_model()`.
    mode không hợp lệ -> ném ValueError.
    Trả về: đồ thị (graph) đã biên dịch, gọi bằng `.invoke({"messages": [...]})`.
    """
    if mode not in {"single", "subagents"}:
        raise ValueError(f"unknown agent mode: {mode}")

    prompt = BASE_PROMPT
    kwargs = {}

    if mode == "subagents":
        kwargs["subagents"] = [
            {**subagent, "system_prompt": f"{subagent['system_prompt']} {PATHS_NOTE}"}
            for subagent in get_subagents()
        ]
        prompt += SUBAGENTS_NOTE

    if use_skills:
        kwargs["skills"] = ["/skills/"]
        prompt += SKILLS_NOTE

    return create_deep_agent(
        model=model or make_model(),
        system_prompt=prompt,
        backend=make_backend(sandbox),
        **kwargs,
    )
