from config import GROK_API_KEY

import json
import os
import shutil
import time
import uuid
from io import BytesIO
from threading import Timer

import gradio as gr
from dotenv import load_dotenv
from e2b_desktop import Sandbox
from gradio_modal import Modal
from huggingface_hub import login, upload_folder
from PIL import Image
from smolagents import CodeAgent
from smolagents.gradio_ui import GradioUI, stream_to_gradio

from e2bqwen import E2BVisionAgent, QwenVLAPIModel, get_agent_summary_erase_images

load_dotenv(override=True)


E2B_API_KEY = os.getenv("E2B_API_KEY")
SANDBOXES = {}
SANDBOX_METADATA = {}
SANDBOX_TIMEOUT = 600
WIDTH = 1024
HEIGHT = 768
TMP_DIR = "./tmp/"
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_API_KEY")
login(token=hf_token)

custom_css = """
.modal-container {
    margin: var(--size-16) auto!important;
}

.sandbox-container {
    position: relative;
    width: 910px;
    overflow: hidden;
    margin: auto;
}
.sandbox-container {
    height: 800px;
}
.sandbox-frame {
    display: none;
    position: absolute;
    top: 0;
    left: 0;
    width: 910px;
    height: 800px;
    pointer-events:none;
}

.sandbox-iframe, .bsod-image {
    position: absolute;
    width: <<WIDTH>>px;
    height: <<HEIGHT>>px;
    border: 4px solid #444444;
    transform-origin: 0 0;
}

/* Colored label for task textbox */
.primary-color-label label span {
    font-weight: bold;
    color: var(--color-accent);
}

/* Status indicator light */
.status-bar {
    display: flex;
    flex-direction: row;
    align-items: center;
    flex-align:center;
    z-index: 100;
}

.status-indicator {
    width: 15px;
    height: 15px;
    border-radius: 50%;
}

.status-text {
    font-size: 16px;
    font-weight: bold;
    padding-left: 8px;
    text-shadow: none;
}

.status-interactive {
    background-color: #2ecc71;
    animation: blink 2s infinite;  
}

.status-view-only {
    background-color: #e74c3c;
}

.status-error {
    background-color: #e74c3c;
    animation: blink-error 1s infinite;
}

@keyframes blink-error {
    0% { background-color: rgba(231, 76, 60, 1); }
    50% { background-color: rgba(231, 76, 60, 0.4); }
    100% { background-color: rgba(231, 76, 60, 1); }
}

@keyframes blink {
    0% { background-color: rgba(46, 204, 113, 1); }  /* Green at full opacity */
    50% { background-color: rgba(46, 204, 113, 0.4); }  /* Green at 40% opacity */
    100% { background-color: rgba(46, 204, 113, 1); }  /* Green at full opacity */
}

#chatbot {
    height:1000px!important;
}
#chatbot .role {
    max-width:95%
}

#chatbot .bubble-wrap {
    overflow-y: visible;
}

.logo-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
    box-sizing: border-box;
    gap: 5px;

.logo-item {
    display: flex;
    align-items: center;
    padding: 0 30px;
    gap: 10px;
    text-decoration: none!important;
    color: #f59e0b;
    font-size:17px;
}
.logo-item:hover {
    color: #935f06!important;
}
""".replace("<<WIDTH>>", str(WIDTH + 15)).replace("<<HEIGHT>>", str(HEIGHT + 10))

footer_html = """
<h3 style="text-align: center; margin-top:50px;"><i>Powered by open source:</i></h2>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<div class="logo-container">
    <a class="logo-item" href="https://github.com/huggingface/smolagents"><i class="fa fa-github"></i>smolagents</a>
    <a class="logo-item" href="https://huggingface.co/Qwen/Qwen2-VL-72B-Instruct"><i class="fa fa-github"></i>Qwen2-VL-72B</a>
    <a class="logo-item" href="https://github.com/e2b-dev/desktop"><i class="fa fa-github"></i>E2B Desktop</a>
</div>
"""
sandbox_html_template = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Oxanium:wght@200..800&display=swap');
</style>
    <h1 style="color:var(--color-accent);margin:0;">Open Computer Agent - <i>Powered by <a href="https://github.com/huggingface/smolagents">smolagents</a></i><h1>
<div class="sandbox-container" style="margin:0;">
    <div class="status-bar">
        <div class="status-indicator {status_class}"></div>
        <div class="status-text">{status_text}</div>
    </div>
    <iframe id="sandbox-iframe"
        src="{stream_url}" 
        class="sandbox-iframe"
        style="display: block;"
        allowfullscreen>
    </iframe>
    <img src="https://huggingface.co/datasets/mfarre/servedfiles/resolve/main/blue_screen_of_death.gif" class="bsod-image" style="display: none;"/>
    <img src="https://huggingface.co/datasets/m-ric/images/resolve/main/HUD_thom.png" class="sandbox-frame" />
</div>
""".replace("<<WIDTH>>", str(WIDTH + 15)).replace("<<HEIGHT>>", str(HEIGHT + 10))

custom_js = """function() {
    document.body.classList.add('dark');

    // Function to check if sandbox is timing out
    const checkSandboxTimeout = function() {
        const timeElement = document.getElementById('sandbox-creation-time');
        
        if (timeElement) {
            const creationTime = parseFloat(timeElement.getAttribute('data-time'));
            const timeoutValue = parseFloat(timeElement.getAttribute('data-timeout'));
            const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
            
            const elapsedTime = currentTime - creationTime;
            console.log("Sandbox running for: " + elapsedTime + " seconds of " + timeoutValue + " seconds");
            
            // If we've exceeded the timeout, show BSOD
            if (elapsedTime >= timeoutValue) {
                console.log("Sandbox timeout! Showing BSOD");
                showBSOD('Error');
                // Don't set another timeout, we're done checking
                return;
            }
        }
        
        // Continue checking every 5 seconds
        setTimeout(checkSandboxTimeout, 5000);
    };
    
    const showBSOD = function(statusText = 'Error') {
        console.log("Showing BSOD with status: " + statusText);
        const iframe = document.getElementById('sandbox-iframe');
        const bsod = document.getElementById('bsod-image');
        
        if (iframe && bsod) {
            iframe.style.display = 'none';
            bsod.style.display = 'block';

            // Update status indicator
            const statusIndicator = document.querySelector('.status-indicator');
            const statusTextElem = document.querySelector('.status-text');

            if (statusIndicator) {
                statusIndicator.className = 'status-indicator status-error';
            }
            
            if (statusTextElem) {
                statusTextElem.innerText = statusText;
            }
        }
    };

    const resetBSOD = function() {
        console.log("Resetting BSOD display");
        const iframe = document.getElementById('sandbox-iframe');
        const bsod = document.getElementById('bsod-image');
        
        if (iframe && bsod) {
            if (bsod.style.display === 'block') {
                // BSOD is currently showing, reset it
                iframe.style.display = 'block';
                bsod.style.display = 'none';
                console.log("BSOD reset complete");
                return true; // Indicates reset was performed
            }
        }
        return false; // No reset needed
    };
    
    // Function to monitor for error messages
    const monitorForErrors = function() {
        console.log("Error monitor started");
        const resultsInterval = setInterval(function() {
            const resultsElements = document.querySelectorAll('textarea, .output-text');
            for (let elem of resultsElements) {
                const content = elem.value || elem.innerText || '';
                if (content.includes('Error running agent')) {
                    console.log("Error detected!");
                    showBSOD('Error');
                    clearInterval(resultsInterval);
                    break;
                }
            }
        }, 1000);
    };
    
    
    // Start monitoring for timeouts immediately
    checkSandboxTimeout();
    
    // Start monitoring for errors
    setTimeout(monitorForErrors, 3000);
    
    // Also monitor for errors after button clicks
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'BUTTON') {
            if (e.target.innerText === "Let's go!") {
                resetBSOD();
            }
            setTimeout(monitorForErrors, 3000);
        }
    });

    // Set up an interval to click the refresh button every 5 seconds
    setInterval(function() {
        const btn = document.getElementById('refresh-log-btn');
        if (btn) btn.click();
    }, 5000);

    // Force dark mode
    const params = new URLSearchParams(window.location.search);
    if (!params.has('__theme')) {
        params.set('__theme', 'dark');
        window.location.search = params.toString();
    }
}
"""


def upload_to_hf_and_remove(folder_path):
    repo_id = "smolagents/computer-agent-logs"
    try:
        folder_name = os.path.basename(os.path.normpath(folder_path))

        # Upload the folder to Huggingface
        print(f"Uploading {folder_path} to {repo_id}/{folder_name}...")
        url = upload_folder(
            folder_path=folder_path,
            repo_id=repo_id,
            repo_type="dataset",
            path_in_repo=folder_name,
            ignore_patterns=[".git/*", ".gitignore"],
        )

        # Remove the local folder after successful upload
        print(f"Upload complete. Removing local folder {folder_path}...")
        shutil.rmtree(folder_path)
        print("Local folder removed successfully.")

        return url

    except Exception as e:
        print(f"Error during upload or cleanup: {str(e)}")
        raise


def cleanup_sandboxes():
    """Remove sandboxes that haven't been accessed for longer than SANDBOX_TIMEOUT"""
    current_time = time.time()
    sandboxes_to_remove = []

    for session_id, metadata in SANDBOX_METADATA.items():
        if current_time - metadata["last_accessed"] > SANDBOX_TIMEOUT:
            sandboxes_to_remove.append(session_id)

    for session_id in sandboxes_to_remove:
        if session_id in SANDBOXES:
            try:
                # Upload data before removing if needed
                data_dir = os.path.join(TMP_DIR, session_id)
                if os.path.exists(data_dir):
                    upload_to_hf_and_remove(data_dir)

                # Close the sandbox
                SANDBOXES[session_id].kill()
                del SANDBOXES[session_id]
                del SANDBOX_METADATA[session_id]
                print(f"Cleaned up sandbox for session {session_id}")
            except Exception as e:
                print(f"Error cleaning up sandbox {session_id}: {str(e)}")


def get_or_create_sandbox(session_uuid):
    current_time = time.time()

    if (
        session_uuid in SANDBOXES
        and session_uuid in SANDBOX_METADATA
        and current_time - SANDBOX_METADATA[session_uuid]["created_at"]
        < SANDBOX_TIMEOUT
    ):
        print(f"Reusing Sandbox for  {session_uuid}")
        SANDBOX_METADATA[session_uuid]["last_accessed"] = current_time
        return SANDBOXES[session_uuid]
    else:
        print("No sandbox found, creating a new one")

    if session_uuid in SANDBOXES:
        try:
            print(f"Closing expired sandbox for session {session_uuid}")
            SANDBOXES[session_uuid].kill()
        except Exception as e:
            print(f"Error closing expired sandbox: {str(e)}")

    print(f"Creating new sandbox for session {session_uuid}")
    desktop = Sandbox(
        api_key=E2B_API_KEY,
        resolution=(WIDTH, HEIGHT),
        dpi=96,
        timeout=SANDBOX_TIMEOUT,
        template="k0wmnzir0zuzye6dndlw",
    )
    desktop.stream.start(require_auth=True)
    setup_cmd = """sudo mkdir -p /usr/lib/firefox-esr/distribution && echo '{"policies":{"OverrideFirstRunPage":"","OverridePostUpdatePage":"","DisableProfileImport":true,"DontCheckDefaultBrowser":true}}' | sudo tee /usr/lib/firefox-esr/distribution/policies.json > /dev/null"""
    desktop.commands.run(setup_cmd)

    print(f"Sandbox ID for session {session_uuid} is {desktop.sandbox_id}.")

    SANDBOXES[session_uuid] = desktop
    SANDBOX_METADATA[session_uuid] = {
        "created_at": current_time,
        "last_accessed": current_time,
    }
    return desktop


def update_html(interactive_mode: bool, session_uuid):
    desktop = get_or_create_sandbox(session_uuid)
    auth_key = desktop.stream.get_auth_key()
    base_url = desktop.stream.get_url(auth_key=auth_key)
    stream_url = base_url if interactive_mode else f"{base_url}&view_only=true"

    status_class = "status-interactive" if interactive_mode else "status-view-only"
    status_text = "Interactive" if interactive_mode else "Agent running..."
    creation_time = (
        SANDBOX_METADATA[session_uuid]["created_at"]
        if session_uuid in SANDBOX_METADATA
        else time.time()
    )

    sandbox_html_content = sandbox_html_template.format(
        stream_url=stream_url,
        status_class=status_class,
        status_text=status_text,
    )
    sandbox_html_content += f'<div id="sandbox-creation-time" style="display:none;" data-time="{creation_time}" data-timeout="{SANDBOX_TIMEOUT}"></div>'
    return sandbox_html_content


def generate_interaction_id(session_uuid):
    return f"{session_uuid}_{int(time.time())}"


def save_final_status(folder, status: str, summary, error_message=None) -> None:
    with open(os.path.join(folder, "metadata.json"), "w") as output_file:
        output_file.write(
            json.dumps(
                {"status": status, "summary": summary, "error_message": error_message},
            )
        )


def extract_browser_uuid(js_uuid):
    print(f"[BROWSER] Got browser UUID from JS: {js_uuid}")
    return js_uuid


def initialize_session(interactive_mode, browser_uuid):
    if not browser_uuid:
        new_uuid = str(uuid.uuid4())
        print(f"[LOAD] No UUID from browser, generating: {new_uuid}")
        return update_html(interactive_mode, new_uuid), new_uuid
    else:
        print(f"[LOAD] Got UUID from browser: {browser_uuid}")
        return update_html(interactive_mode, browser_uuid), browser_uuid


def create_agent(data_dir, desktop):
    model = QwenVLAPIModel(
        model_id="Qwen/Qwen2.5-VL-72B-Instruct",
        hf_token=hf_token,
    )

    # model = OpenAIServerModel(
    #     "gpt-4o",api_key=GROK_API_KEY
    # )
    return E2BVisionAgent(
        model=model,
        data_dir=data_dir,
        desktop=desktop,
        max_steps=200,
        verbosity_level=2,
        # planning_interval=10,
        use_v1_prompt=True,
    )


class EnrichedGradioUI(GradioUI):
    def log_user_message(self, text_input):
        import gradio as gr

        return (
            text_input,
            gr.Button(interactive=False),
        )

    def interact_with_agent(
        self,
        task_input,
        stored_messages,
        session_state,
        session_uuid,
        consent_storage,
        request: gr.Request,
    ):
        interaction_id = generate_interaction_id(session_uuid)
        desktop = get_or_create_sandbox(session_uuid)

        data_dir = os.path.join(TMP_DIR, interaction_id)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Always re-create an agent from scratch, else Qwen-VL gets confused with past history
        session_state["agent"] = create_agent(data_dir=data_dir, desktop=desktop)

        try:
            stored_messages.append(gr.ChatMessage(role="user", content=task_input))
            yield stored_messages

            screenshot_bytes = session_state["agent"].desktop.screenshot(format="bytes")
            initial_screenshot = Image.open(BytesIO(screenshot_bytes))

            for msg in stream_to_gradio(
                session_state["agent"],
                task=task_input,
                task_images=[initial_screenshot],
                reset_agent_memory=False,
            ):
                if (
                    hasattr(session_state["agent"], "last_marked_screenshot")
                    and msg.content == "-----"
                ):  # Append the last screenshot before the end of step
                    stored_messages.append(
                        gr.ChatMessage(
                            role="assistant",
                            content={
                                "path": session_state[
                                    "agent"
                                ].last_marked_screenshot.to_string(),
                                "mime_type": "image/png",
                            },
                        )
                    )
                stored_messages.append(msg)
                yield stored_messages

            # THIS ERASES IMAGES FROM AGENT MEMORY, USE WITH CAUTION
            if consent_storage:
                summary = get_agent_summary_erase_images(session_state["agent"])
                save_final_status(data_dir, "completed", summary=summary)
            yield stored_messages

        except Exception as e:
            error_message = f"Error in interaction: {str(e)}"
            raise e
            print(error_message)
            stored_messages.append(
                gr.ChatMessage(
                    role="assistant", content="Run failed:\n" + error_message
                )
            )
            if consent_storage:
                summary = get_agent_summary_erase_images(session_state["agent"])
                save_final_status(
                    data_dir, "failed", summary=summary, error_message=error_message
                )
            yield stored_messages
        finally:
            if consent_storage:
                upload_to_hf_and_remove(data_dir)


theme = gr.themes.Default(
    font=["Oxanium", "sans-serif"], primary_hue="amber", secondary_hue="blue"
)

# Create a Gradio app with Blocks
with gr.Blocks(theme=theme, css=custom_css, js=custom_js) as demo:
    # Storing session hash in a state variable
    session_uuid_state = gr.State(None)
    print("Starting the app!")
    with gr.Row():
        sandbox_html = gr.HTML(
            value=sandbox_html_template.format(
                stream_url="",
                status_class="status-interactive",
                status_text="Interactive",
            ),
            label="Output",
        )
        with gr.Sidebar(position="left"):
            with Modal(visible=True) as modal:
                gr.Markdown("""### Welcome to smolagent's Computer agent demo 🖥️
In this app, you'll be able to interact with an agent powered by [smolagents](https://github.com/huggingface/smolagents) and [Qwen-VL](https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct).

👉 Type a task in the left sidebar, click the button, and watch the agent solving your task. ✨

_Please note that we store the task logs by default so **do not write any personal information**; you can uncheck the logs storing on the task bar._
""")
            task_input = gr.Textbox(
                value="Find me pictures of cute puppies",
                label="Enter your task below:",
                elem_classes="primary-color-label",
            )

            run_btn = gr.Button("Let's go!", variant="primary")

            gr.Examples(
                examples=[
                    "Use Google Maps to find the Hugging Face HQ in Paris",
                    "Go to Wikipedia and find what happened on April 4th",
                    "Find out the travel time by train from Bern to Basel on Google Maps",
                    "Go to Hugging Face Spaces and then find the Space flux.1 schnell. Use the space to generate an image with the prompt 'a field of gpus'",
                ],
                inputs=task_input,
                label="Example Tasks",
                examples_per_page=4,
            )

            session_state = gr.State({})
            stored_messages = gr.State([])

            minimalist_toggle = gr.Checkbox(label="Innie/Outie", value=False)

            consent_storage = gr.Checkbox(
                label="Store task and agent trace?", value=True
            )

            gr.Markdown(
                """
- **Data**: To opt-out of storing your trace, uncheck the box above.
- **Be patient**: The agent's first step can take a few seconds.
- **Captcha**: Sometimes the VMs get flagged for weird behaviour and are blocked with a captcha. Best is then to interrupt the agent and solve the captcha manually.
- **Restart**: If your agent seems stuck, the simplest way to restart is to refresh the page.
                """.strip()
            )

            def apply_theme(minimalist_mode: bool):
                if not minimalist_mode:
                    return """
                        <style>
                        .sandbox-frame {
                            display: block!important;
                        }

                        .sandbox-iframe, .bsod-image {
                            /* top: 73px; */
                            top: 99px;
                            /* left: 74px; */
                            left: 110px;
                        }
                        .sandbox-iframe {
                            transform: scale(0.667);
                            /* transform: scale(0.59); */
                        }

                        .status-bar {
                            position: absolute;
                            bottom: 88px;
                            left: 355px;
                        }
                        .status-text {
                            color: #fed244;
                        }
                        </style>
                    """
                else:
                    return """
                        <style>
                        .sandbox-container {
                            height: 700px!important;
                        }
                        .sandbox-iframe {
                            transform: scale(0.65);
                        }
                        </style>
                    """

            # Hidden HTML element to inject CSS dynamically
            theme_styles = gr.HTML(apply_theme(False), visible=False)
            minimalist_toggle.change(
                fn=apply_theme, inputs=[minimalist_toggle], outputs=[theme_styles]
            )

            footer = gr.HTML(value=footer_html, label="Header")

    chatbot_display = gr.Chatbot(
        elem_id="chatbot",
        label="Agent's execution logs",
        type="messages",
        avatar_images=(
            None,
            "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/smolagents/mascot_smol.png",
        ),
        resizable=True,
    )

    agent_ui = EnrichedGradioUI(
        CodeAgent(tools=[], model=None, name="ok", description="ok")
    )

    stop_btn = gr.Button("Stop the agent!", variant="huggingface")

    def read_log_content(log_file, tail=4):
        """Read the contents of a log file for a specific session"""
        if not log_file:
            return "Waiting for session..."

        if not os.path.exists(log_file):
            return "Waiting for machine from the future to boot..."

        try:
            with open(log_file, "r") as f:
                lines = f.readlines()
                return "".join(lines[-tail:] if len(lines) > tail else lines)
        except Exception as e:
            return f"Guru meditation: {str(e)}"

    # Function to set view-only mode
    def clear_and_set_view_only(task_input, session_uuid):
        return update_html(False, session_uuid)

    def set_interactive(session_uuid):
        return update_html(True, session_uuid)

    def reactivate_stop_btn():
        return gr.Button("Stop the agent!", variant="huggingface")

    is_interactive = gr.Checkbox(value=True, visible=False)

    # Chain the events
    run_event = (
        run_btn.click(
            fn=clear_and_set_view_only,
            inputs=[task_input, session_uuid_state],
            outputs=[sandbox_html],
        )
        .then(
            agent_ui.interact_with_agent,
            inputs=[
                task_input,
                stored_messages,
                session_state,
                session_uuid_state,
                consent_storage,
            ],
            outputs=[chatbot_display],
        )
        .then(fn=set_interactive, inputs=[session_uuid_state], outputs=[sandbox_html])
        .then(fn=reactivate_stop_btn, outputs=[stop_btn])
    )

    def interrupt_agent(session_state):
        if not session_state["agent"].interrupt_switch:
            session_state["agent"].interrupt()
            return gr.Button("Stopping agent... (could take time)", variant="secondary")
        else:
            return gr.Button("Stop the agent!", variant="huggingface")

    stop_btn.click(fn=interrupt_agent, inputs=[session_state], outputs=[stop_btn])

    def set_logs_source(session_state):
        session_state["replay_log"] = "udupp2fyavq_1743170323"

    demo.load(
        fn=lambda: True,  # dummy to trigger the load
        outputs=[is_interactive],
    ).then(
        fn=initialize_session,
        js="() => localStorage.getItem('gradio-session-uuid') || (() => { const id = self.crypto.randomUUID(); localStorage.setItem('gradio-session-uuid', id); return id })()",
        inputs=[is_interactive],
        outputs=[sandbox_html, session_uuid_state],
    )

# Launch the app
if __name__ == "__main__":
    Timer(60, cleanup_sandboxes).start()  # Run every minute
    demo.launch()
