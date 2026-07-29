from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# Reconfigure stdout for Windows console unicode printing
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import streamlit as st

from chat import run_model_tool_loop, trim_history
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import build_artifact_version

# Initialize environment
ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
DATA_DIR = ROOT / "data"
load_lab_env(ROOT)

# Page configuration
st.set_page_config(
    page_title="Research Agent Lab — AI Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_all_eval_cases() -> list[dict[str, Any]]:
    cases = []
    for file_name in ["eval_group.json", "eval_base.json"]:
        file_path = DATA_DIR / file_name
        if file_path.exists():
            try:
                data = json.loads(file_path.read_text(encoding="utf-8"))
                for c in data.get("cases", []):
                    c["source_suite"] = data.get("dataset_role", file_name)
                    cases.append(c)
            except Exception:
                pass
    return cases


all_eval_cases = load_all_eval_cases()


def init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "history" not in st.session_state:
        st.session_state.history = []
    if "turn_records" not in st.session_state:
        st.session_state.turn_records = []
    if "preset_prompt" not in st.session_state:
        st.session_state.preset_prompt = ""


init_session_state()

# Sidebar Setup
st.sidebar.title("🔬 Research Agent Dashboard")
st.sidebar.markdown("---")

# 🎨 Custom Theme: Only Chat Background Color Picker
st.sidebar.subheader("🎨 Custom Theme")
bg_color = st.sidebar.color_picker(
    "Màu nền Chat (Background Color)",
    value="#0E1117",
    help="Chọn màu nền cho giao diện chat",
)

st.sidebar.markdown("---")

# Inject Dynamic CSS for Chat Background Color
st.markdown(
    f"""
    <style>
    /* Custom Styling */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }}
    .stApp {{
        background-color: {bg_color} !important;
        color: #e0e6ed;
    }}
    section[data-testid="stSidebar"] {{
        background-color: #161b22;
    }}
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {{
        background-color: #1e3a8a;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
    }}
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {{
        background-color: #1f2937;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
    }}
    .version-card {{
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 15px;
    }}
    .version-badge {{
        background-color: #2563eb;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.85rem;
    }}
    .case-card {{
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 12px;
        margin-top: 8px;
        margin-bottom: 12px;
    }}
    .hash-text {{
        font-family: monospace;
        font-size: 0.78rem;
        color: #9ca3af;
        word-break: break-all;
    }}
    .trace-card {{
        background-color: #1a202c;
        border-left: 4px solid #3b82f6;
        border-radius: 6px;
        padding: 10px 14px;
        margin-top: 8px;
        margin-bottom: 8px;
    }}
    .trace-status-success {{
        color: #10b981;
        font-weight: bold;
    }}
    .trace-status-error {{
        color: #ef4444;
        font-weight: bold;
    }}
    .trace-status-waiting {{
        color: #f59e0b;
        font-weight: bold;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Version Selector (v0 - v3)
st.sidebar.subheader("📌 Version Selection")
selected_version = st.sidebar.selectbox(
    "Choose Version",
    options=["v3", "v2", "v1", "v0"],
    index=0,
    help="Select artifact version to inspect system prompt & tool configuration.",
)

# Map version selector to actual versioned files
if selected_version == "v0":
    system_prompt_file = ARTIFACTS_DIR / "system_prompt_v0.md"
    tools_file = ARTIFACTS_DIR / "tools_v0.yaml"
elif selected_version == "v1":
    system_prompt_file = ARTIFACTS_DIR / "system_prompt_v1.md"
    tools_file = ARTIFACTS_DIR / "tools_v0.yaml"
elif selected_version == "v2":
    system_prompt_file = ARTIFACTS_DIR / "system_prompt_v2.md"
    tools_file = ARTIFACTS_DIR / "tools_v0.yaml"
else:
    system_prompt_file = ARTIFACTS_DIR / "system_prompt.md"
    tools_file = ARTIFACTS_DIR / "tools.yaml"

system_prompt_text = system_prompt_file.read_text(encoding="utf-8") if system_prompt_file.exists() else ""
tool_declarations = load_tool_declarations(tools_file) if tools_file.exists() else []

art_ver = build_artifact_version(selected_version, system_prompt_file, tools_file)

# Display Version Info Box
st.sidebar.markdown(
    f"""
    <div class="version-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span class="version-badge">{art_ver.version}</span>
            <span style="font-size: 0.8rem; color: #10b981;">Active</span>
        </div>
        <div style="font-size: 0.85rem; margin-bottom: 4px;"><b>Artifact Version:</b></div>
        <div class="hash-text">{art_ver.artifact_version}</div>
        <div style="font-size: 0.85rem; margin-top: 8px; margin-bottom: 2px;"><b>Prompt Hash:</b></div>
        <div class="hash-text">{art_ver.prompt_hash[:16]}...</div>
        <div style="font-size: 0.85rem; margin-top: 6px; margin-bottom: 2px;"><b>Tools Hash:</b></div>
        <div class="hash-text">{art_ver.tools_hash[:16]}...</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 🧪 Test Case Selector & Inspector
st.sidebar.subheader("🧪 Test Case Inspector")
case_options = ["-- Chọn Test Case ID --"] + [f"{c['id']} [{c['source_suite'].upper()}]" for c in all_eval_cases]
selected_case_option = st.sidebar.selectbox("Test Case ID", options=case_options, index=0)

if selected_case_option != "-- Chọn Test Case ID --":
    selected_id = selected_case_option.split(" [")[0]
    matched_case = next((c for c in all_eval_cases if c["id"] == selected_id), None)

    if matched_case:
        prompt_text = matched_case.get("query")
        if not prompt_text and matched_case.get("turns"):
            prompt_text = matched_case["turns"][0].get("user", "")

        expect_calls = matched_case.get("expect", {}).get("tool_calls", [])
        no_tool = matched_case.get("expect", {}).get("no_tool", False)
        failure_type = matched_case.get("failure_type", "N/A")
        what_it_tests = matched_case.get("metadata", {}).get("what_it_tests", "")

        expected_summary = "no_tool (Không gọi tool)" if no_tool else json.dumps(expect_calls, ensure_ascii=False)

        st.sidebar.markdown(
            f"""
            <div class="case-card">
                <div style="font-size:0.85rem; color:#60a5fa; font-weight:bold;">📋 Case ID: {matched_case['id']}</div>
                <div style="font-size:0.8rem; margin-top:4px;"><b>Failure Type:</b> <code style="color:#f87171;">{failure_type}</code></div>
                <div style="font-size:0.8rem; margin-top:4px;"><b>Prompt:</b> <br><i>"{prompt_text}"</i></div>
                <div style="font-size:0.8rem; margin-top:4px;"><b>Expected Tool:</b> <br><code style="color:#34d399;">{expected_summary}</code></div>
                {f'<div style="font-size:0.75rem; color:#94a3b8; margin-top:4px;"><b>Mô tả:</b> {what_it_tests}</div>' if what_it_tests else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.sidebar.button("🚀 Nạp Prompt vào Chat Input", use_container_width=True):
            st.session_state.preset_prompt = prompt_text
            st.rerun()

st.sidebar.markdown("---")

# Provider & Model Settings
st.sidebar.subheader("⚙️ Model Settings")
provider_name = st.sidebar.selectbox(
    "Provider",
    options=["openrouter", "openai", "anthropic", "gemini"],
    index=0,
)

model_override = st.sidebar.text_input(
    "Model Override (Optional)",
    placeholder="e.g. openai/gpt-4o-mini",
    value="",
)

history_window = st.sidebar.slider("History Window", min_value=1, max_value=10, value=5)
max_tool_rounds = st.sidebar.slider("Max Tool Rounds", min_value=1, max_value=8, value=4)

if st.sidebar.button("🧹 Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.session_state.history = []
    st.session_state.turn_records = []
    st.session_state.preset_prompt = ""
    st.rerun()

# Main Title Header
st.title("🤖 Research Agent Interactive Chat")
st.caption(f"Running Version: **{selected_version}** | Provider: **{provider_name}** | Tools Loaded: **{len(tool_declarations)}**")

# Render Chat History
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display Tool Execution Trace for Assistant messages
        if message["role"] == "assistant" and "turn_record" in message:
            turn_rec = message["turn_record"]
            rounds = turn_rec.get("rounds", [])
            tool_events = turn_rec.get("tool_events", [])

            if rounds or tool_events:
                with st.expander(f"🛠️ Tool Execution Trace ({len(rounds)} Rounds, {len(tool_events)} Tools Called)", expanded=False):
                    for round_item in rounds:
                        st.markdown(f"#### 🔄 Round {round_item.get('round')}")
                        if round_item.get("assistant_text"):
                            st.caption(f"Assistant thoughts/text: {round_item['assistant_text']}")

                        calls = round_item.get("tool_calls", [])
                        results = round_item.get("tool_results", [])

                        for call_idx, call in enumerate(calls):
                            tool_name = call.get("name", "unknown")
                            tool_args = call.get("args", {})
                            res_event = results[call_idx] if call_idx < len(results) else {}
                            res_payload = res_event.get("result", {})

                            # Determine status
                            if isinstance(res_payload, dict) and "error" in res_payload:
                                status_html = '<span class="trace-status-error">❌ ERROR</span>'
                            elif isinstance(res_payload, dict) and res_payload.get("awaiting_user"):
                                status_html = '<span class="trace-status-waiting">⏸️ WAITING FOR USER</span>'
                            else:
                                status_html = '<span class="trace-status-success">✅ SUCCESS</span>'

                            st.markdown(
                                f"""
                                <div class="trace-card">
                                    <div style="display:flex; justify-content:space-between;">
                                        <span>🔧 <b>Tool:</b> <code>{tool_name}</code></span>
                                        <span>{status_html}</span>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            st.json({"arguments": tool_args, "result": res_payload})

# Chat Input with Preset Prompt Support
default_input = st.session_state.preset_prompt
st.session_state.preset_prompt = ""  # Consume preset

if prompt := st.chat_input("Enter your request or question here...", key="chat_input"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Execute Agent Loop
    with st.chat_message("assistant"):
        with st.spinner("Agent is reasoning and executing tools..."):
            try:
                provider = make_provider(provider_name)
                openai_tools = to_openai_tools(tool_declarations)

                messages = [
                    {"role": "system", "content": system_prompt_text},
                    *trim_history(st.session_state.history, history_window),
                    {"role": "user", "content": prompt},
                ]

                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=openai_tools,
                    model=model_override if model_override.strip() else None,
                    max_tool_rounds=max_tool_rounds,
                )

                assistant_text = result.get("assistant_text") or "Completed."
                st.markdown(assistant_text)

                # Update history
                st.session_state.history.append({"role": "user", "content": prompt})
                st.session_state.history.append({"role": "assistant", "content": assistant_text})

                # Record message with turn record for trace rendering
                message_record = {
                    "role": "assistant",
                    "content": assistant_text,
                    "turn_record": result,
                }
                st.session_state.messages.append(message_record)

                # Render Tool Execution Trace immediately
                rounds = result.get("rounds", [])
                tool_events = result.get("tool_events", [])
                if rounds or tool_events:
                    with st.expander(f"🛠️ Tool Execution Trace ({len(rounds)} Rounds, {len(tool_events)} Tools Called)", expanded=True):
                        for round_item in rounds:
                            st.markdown(f"#### 🔄 Round {round_item.get('round')}")
                            if round_item.get("assistant_text"):
                                st.caption(f"Assistant thoughts/text: {round_item['assistant_text']}")

                            calls = round_item.get("tool_calls", [])
                            results = round_item.get("tool_results", [])

                            for call_idx, call in enumerate(calls):
                                tool_name = call.get("name", "unknown")
                                tool_args = call.get("args", {})
                                res_event = results[call_idx] if call_idx < len(results) else {}
                                res_payload = res_event.get("result", {})

                                if isinstance(res_payload, dict) and "error" in res_payload:
                                    status_html = '<span class="trace-status-error">❌ ERROR</span>'
                                elif isinstance(res_payload, dict) and res_payload.get("awaiting_user"):
                                    status_html = '<span class="trace-status-waiting">⏸️ WAITING FOR USER</span>'
                                else:
                                    status_html = '<span class="trace-status-success">✅ SUCCESS</span>'

                                st.markdown(
                                    f"""
                                    <div class="trace-card">
                                        <div style="display:flex; justify-content:space-between;">
                                            <span>🔧 <b>Tool:</b> <code>{tool_name}</code></span>
                                            <span>{status_html}</span>
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                                st.json({"arguments": tool_args, "result": res_payload})

            except Exception as exc:
                error_msg = f"❌ Error running agent: {type(exc).__name__}: {str(exc)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
