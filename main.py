# # main.py
# import sys
# import asyncio
# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse
# from pydantic import BaseModel
# import asyncio
# from automation import submit_student_feedback
# app = FastAPI()

# class Credentials(BaseModel):
#     reg_no: str
#     password: str

# # In-memory session tracking for WebSocket connections
# active_connections: dict[str, WebSocket] = {}

# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: str):
#     await websocket.accept()
#     active_connections[client_id] = websocket
#     try:
#         while True:
#             await websocket.receive_text()
#     except WebSocketDisconnect:
#         del active_connections[client_id]

# @app.post("/api/submit-feedback")
# async def start_feedback(credentials: Credentials, client_id: str):
#     async def progress_callback(message: str):
#         if client_id in active_connections:
#             await active_connections[client_id].send_json({"message": message})

#     # Run the Playwright task asynchronously in the background
#     asyncio.create_task(
#         submit_student_feedback(credentials.reg_no, credentials.password, progress_callback)
#     )

#     return {"status": "started", "message": "Feedback automation process initiated."}

# @app.get("/")
# async def serve_index():
#     return HTMLResponse(content=INDEX_HTML)

# INDEX_HTML = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Auto Feedback Submitter</title>
#     <style>
#         body { font-family: sans-serif; max-width: 500px; margin: 40px auto; padding: 20px; }
#         .form-group { margin-bottom: 15px; }
#         label { display: block; margin-bottom: 5px; }
#         input { width: 100%; padding: 8px; box-sizing: border-box; }
#         button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }
#         #logs { margin-top: 20px; background: #f4f4f4; padding: 10px; height: 200px; overflow-y: scroll; font-family: monospace; }
#     </style>
# </head>
# <body>
#     <h2>Student Feedback Automation</h2>
#     <div class="form-group">
#         <label>Registration No.</label>
#         <input type="text" id="regNo">
#     </div>
#     <div class="form-group">
#         <label>Password</label>
#         <input type="password" id="password">
#     </div>
#     <button onclick="startAutomation()">Submit Feedback</button>

#     <h3>Status Log:</h3>
#     <div id="logs"></div>

#     <script>
#         const clientId = Math.random().toString(36).substring(7);
#         const ws = new WebSocket(`ws://${location.host}/ws/${clientId}`);

#         ws.onmessage = (event) => {
#             const data = JSON.parse(event.data);
#             const logsDiv = document.getElementById("logs");
#             logsDiv.innerHTML += `<div>> ${data.message}</div>`;
#             logsDiv.scrollTop = logsDiv.scrollHeight;
#         };

#         async function startAutomation() {
#             const reg_no = document.getElementById("regNo").value;
#             const password = document.getElementById("password").value;

#             document.getElementById("logs").innerHTML = "<div>> Task queued...</div>";

#             await fetch(`/api/submit-feedback?client_id=${clientId}`, {
#                 method: "POST",
#                 headers: { "Content-Type": "application/json" },
#                 body: JSON.stringify({ reg_no, password })
#             });
#         }
#     </script>
# </body>
# </html>
# """



# import sys
# import asyncio
# import threading

# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(
#         asyncio.WindowsProactorEventLoopPolicy()
#     )

# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse
# from pydantic import BaseModel

# from automation import submit_student_feedback


# app = FastAPI()


# class Credentials(BaseModel):
#     reg_no: str
#     password: str


# # Active WebSocket connections
# active_connections: dict[str, WebSocket] = {}


# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: str):

#     await websocket.accept()

#     active_connections[client_id] = websocket

#     try:
#         while True:
#             await websocket.receive_text()

#     except WebSocketDisconnect:
#         active_connections.pop(client_id, None)

#     except Exception:
#         active_connections.pop(client_id, None)


# async def send_progress(client_id: str, message: str):

#     websocket = active_connections.get(client_id)

#     if websocket:

#         try:
#             await websocket.send_json({
#                 "message": message
#             })

#         except Exception:
#             active_connections.pop(client_id, None)


# def run_playwright_task(
#     reg_no: str,
#     password: str,
#     client_id: str
# ):

#     """
#     Runs Playwright inside its own thread/event loop.

#     This avoids Windows asyncio subprocess issues
#     when Playwright is launched from FastAPI's event loop.
#     """

#     async def runner():

#         async def progress_callback(message: str):

#             await send_progress(
#                 client_id,
#                 message
#             )

#         try:

#             result = await submit_student_feedback(
#                 reg_no,
#                 password,
#                 progress_callback
#             )

#             if result:

#                 await send_progress(
#                     client_id,
#                     "TASK_SUCCESS"
#                 )

#             else:

#                 await send_progress(
#                     client_id,
#                     "TASK_FAILED"
#                 )

#         except Exception as e:

#             await send_progress(
#                 client_id,
#                 f"TASK_ERROR: {str(e)}"
#             )

#     # Windows: use ProactorEventLoop
#     if sys.platform == "win32":

#         loop = asyncio.ProactorEventLoop()

#         asyncio.set_event_loop(loop)

#     else:

#         loop = asyncio.new_event_loop()

#         asyncio.set_event_loop(loop)

#     try:

#         loop.run_until_complete(runner())

#     finally:

#         loop.close()


# @app.post("/api/submit-feedback")
# async def start_feedback(
#     credentials: Credentials,
#     client_id: str
# ):

#     # Start Playwright in separate thread
#     thread = threading.Thread(
#         target=run_playwright_task,
#         args=(
#             credentials.reg_no,
#             credentials.password,
#             client_id
#         ),
#         daemon=True
#     )

#     thread.start()

#     return {
#         "status": "started",
#         "message": "Feedback automation process initiated."
#     }


# @app.get("/")
# async def serve_index():

#     return HTMLResponse(
#         content=INDEX_HTML
#     )


# INDEX_HTML = """
# <!DOCTYPE html>

# <html lang="en">

# <head>

#     <meta charset="UTF-8">

#     <title>Auto Feedback Submitter</title>

#     <style>

#         body {
#             font-family: sans-serif;
#             max-width: 500px;
#             margin: 40px auto;
#             padding: 20px;
#         }

#         .form-group {
#             margin-bottom: 15px;
#         }

#         label {
#             display: block;
#             margin-bottom: 5px;
#         }

#         input {
#             width: 100%;
#             padding: 8px;
#             box-sizing: border-box;
#         }

#         button {
#             width: 100%;
#             padding: 10px;
#             background: #007bff;
#             color: white;
#             border: none;
#             cursor: pointer;
#         }

#         #logs {
#             margin-top: 20px;
#             background: #f4f4f4;
#             padding: 10px;
#             height: 200px;
#             overflow-y: scroll;
#             font-family: monospace;
#         }

#     </style>

# </head>


# <body>

#     <h2>Student Feedback Automation</h2>


#     <div class="form-group">

#         <label>
#             Registration No.
#         </label>

#         <input
#             type="text"
#             id="regNo"
#         >

#     </div>


#     <div class="form-group">

#         <label>
#             Password
#         </label>

#         <input
#             type="password"
#             id="password"
#         >

#     </div>


#     <button onclick="startAutomation()">
#         Submit Feedback
#     </button>


#     <h3>Status Log:</h3>

#     <div id="logs"></div>


# <script>

# const clientId =
#     Math.random()
#         .toString(36)
#         .substring(7);


# const ws =
#     new WebSocket(
#         `ws://${location.host}/ws/${clientId}`
#     );


# ws.onopen = () => {

#     addLog("WebSocket connected.");

# };


# ws.onmessage = (event) => {

#     const data =
#         JSON.parse(event.data);

#     addLog(data.message);

# };


# ws.onerror = () => {

#     addLog("WebSocket connection error.");

# };


# ws.onclose = () => {

#     addLog("WebSocket disconnected.");

# };


# function addLog(message) {

#     const logsDiv =
#         document.getElementById("logs");

#     const div =
#         document.createElement("div");

#     div.textContent =
#         "> " + message;

#     logsDiv.appendChild(div);

#     logsDiv.scrollTop =
#         logsDiv.scrollHeight;
# }


# async function startAutomation() {

#     const reg_no =
#         document
#             .getElementById("regNo")
#             .value;

#     const password =
#         document
#             .getElementById("password")
#             .value;


#     if (!reg_no || !password) {

#         addLog(
#             "Please enter registration number and password."
#         );

#         return;
#     }


#     document
#         .getElementById("logs")
#         .innerHTML =
#         "<div>> Task queued...</div>";


#     try {

#         const response =
#             await fetch(
#                 `/api/submit-feedback?client_id=${clientId}`,
#                 {
#                     method: "POST",

#                     headers: {
#                         "Content-Type":
#                             "application/json"
#                     },

#                     body: JSON.stringify({
#                         reg_no: reg_no,
#                         password: password
#                     })
#                 }
#             );


#         const data =
#             await response.json();


#         addLog(data.message);


#     } catch (error) {

#         addLog(
#             "Failed to start automation: " +
#             error
#         );

#     }

# }

# </script>

# </body>

# </html>
# """



import sys
import asyncio
import threading
from typing import List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from automation import submit_student_feedback, DEFAULT_SUBJECTS

app = FastAPI(title="Auto Feedback Portal")

class FeedbackRequest(BaseModel):
    reg_no: str
    password: str
    subjects: Optional[List[str]] = None

active_connections: dict[str, WebSocket] = {}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    active_connections[client_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except (WebSocketDisconnect, Exception):
        active_connections.pop(client_id, None)

async def send_progress(client_id: str, data: dict):
    websocket = active_connections.get(client_id)
    if websocket:
        try:
            await websocket.send_json(data)
        except Exception:
            active_connections.pop(client_id, None)

def run_playwright_task(reg_no: str, password: str, subjects: Optional[List[str]], client_id: str):
    async def runner():
        async def progress_callback(payload: dict):
            await send_progress(client_id, payload)

        try:
            result = await submit_student_feedback(
                reg_no, password, subjects, progress_callback
            )
            status = "TASK_SUCCESS" if result else "TASK_FAILED"
            await send_progress(client_id, {"message": f"Execution finished: {status}", "type": "status", "status": status})
        except Exception as e:
            await send_progress(client_id, {"message": f"Fatal Task Failure: {str(e)}", "type": "error", "status": "TASK_ERROR"})

    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(runner())
    finally:
        loop.close()

@app.post("/api/submit-feedback")
async def start_feedback(req: FeedbackRequest, client_id: str):
    if not req.reg_no.strip() or not req.password.strip():
        return {"status": "error", "message": "Registration number and password are required."}

    thread = threading.Thread(
        target=run_playwright_task,
        args=(req.reg_no, req.password, req.subjects, client_id),
        daemon=True
    )
    thread.start()
    return {"status": "started", "message": "Automation worker initialized."}

@app.get("/")
async def serve_index():
    return HTMLResponse(content=INDEX_HTML)

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoFeedback Pro - Adamas University</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: { 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca' }
                    }
                }
            }
        }
    </script>
    <style>
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0f172a; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans selection:bg-brand-500 selection:text-white">

    <!-- Header Navigation -->
    <header class="border-b border-slate-800 bg-slate-900/50 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="p-2 bg-brand-600 rounded-lg shadow-lg shadow-brand-500/20">
                    <i data-lucide="zap" class="w-5 h-5 text-white"></i>
                </div>
                <span class="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">AutoFeedback AI</span>
            </div>
            <nav class="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-400">
                <a href="#app" class="hover:text-white transition">App Portal</a>
                <a href="#demo" class="hover:text-white transition">Demo Walkthrough</a>
                <a href="#team" class="hover:text-white transition">Project Team</a>
            </nav>
        </div>
    </header>

    <main class="flex-grow max-w-7xl w-full mx-auto px-6 py-10 space-y-20">

        <!-- App Section -->
        <section id="app" class="grid lg:grid-cols-12 gap-8 items-start">
            
            <!-- Left: Credentials & Subject Config -->
            <div class="lg:col-span-5 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6 backdrop-blur">
                <div>
                    <h2 class="text-xl font-semibold flex items-center gap-2">
                        <i data-lucide="shield-check" class="w-5 h-5 text-brand-500"></i> Portal Login
                    </h2>
                    <p class="text-xs text-slate-400 mt-1">Automate your pending course evaluations safely.</p>
                </div>

                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Registration No.</label>
                        <input type="text" id="regNo" placeholder="e.g., AU/2022/0001" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Password</label>
                        <input type="password" id="password" placeholder="••••••••••••" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition">
                    </div>
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <label class="text-xs font-semibold text-slate-300 uppercase tracking-wider">Custom Subjects (Comma Separated)</label>
                            <button onclick="resetDefaultSubjects()" class="text-[10px] text-brand-500 hover:underline">Reset Defaults</button>
                        </div>
                        <textarea id="subjectsInput" rows="4" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition leading-relaxed"></textarea>
                    </div>

                    <button id="submitBtn" onclick="startAutomation()" class="w-full py-3 bg-brand-600 hover:bg-brand-700 text-white font-medium text-sm rounded-xl shadow-lg shadow-brand-500/20 transition flex items-center justify-center space-x-2">
                        <i data-lucide="play" class="w-4 h-4"></i>
                        <span>Start Automated Submission</span>
                    </button>
                </div>
            </div>

            <!-- Right: Real-time Live Log & Progress Stream -->
            <div class="lg:col-span-7 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col h-[520px] backdrop-blur">
                <div class="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
                    <div class="flex items-center space-x-2">
                        <span id="statusIndicator" class="w-2.5 h-2.5 rounded-full bg-slate-600"></span>
                        <h3 class="font-semibold text-sm">Real-time Execution Stream</h3>
                    </div>
                    <button onclick="clearLogs()" class="text-xs text-slate-400 hover:text-white flex items-center gap-1">
                        <i data-lucide="trash-2" class="w-3.5 h-3.5"></i> Clear Log
                    </button>
                </div>

                <div id="logs" class="flex-grow overflow-y-auto space-y-2 text-xs font-mono pr-2">
                    <div class="text-slate-500 italic">Waiting for process initiation...</div>
                </div>
            </div>
        </section>

        <!-- Demo Video Section -->
        <section id="demo" class="space-y-6">
            <div class="text-center max-w-2xl mx-auto space-y-2">
                <h2 class="text-2xl font-bold tracking-tight">Interactive Demonstration</h2>
                <p class="text-slate-400 text-sm">Watch the Playwright headless agent automatically identify pending course forms and submit evaluation reports.</p>
            </div>
            <div class="max-w-4xl mx-auto bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl aspect-video relative group flex items-center justify-center">
                <!-- Video Embed / Local Player Placeholder -->
                <video controls class="w-full h-full object-cover">
                    <source src="https://drive.google.com/file/d/1n8fJNRiCvpT8705h0K7pxNlHdxs7Ykib/view?usp=sharing" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        </section>

        <!-- Project Team Section -->
        <section id="team" class="space-y-8">
            <div class="text-center max-w-2xl mx-auto space-y-2">
                <h2 class="text-2xl font-bold tracking-tight">Project Team & Mentorship</h2>
                <p class="text-slate-400 text-sm">Developed under academic guidance at Adamas University.</p>
            </div>

            <div class="grid md:grid-cols-2 gap-6 max-w-3xl mx-auto">
                
                <!-- Project Mentor -->
                <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 flex items-start space-x-4">
                    <div class="w-12 h-12 bg-indigo-500/10 border border-indigo-500/30 rounded-xl flex items-center justify-center text-brand-500 flex-shrink-0">
                        <i data-lucide="graduation-cap" class="w-6 h-6"></i>
                    </div>
                    <div class="space-y-1">
                        <span class="text-[10px] font-bold text-brand-500 uppercase tracking-wider">Project Mentor</span>
                        <h3 class="font-semibold text-base">NA</h3>
                        <p class="text-xs text-slate-400">Department of Computer Science & Engineering</p>
                        <p class="text-xs text-slate-500 pt-1">Guided the architecture, security compliance, and automation workflow optimization.</p>
                    </div>
                </div>

                <!-- Lead Developer -->
                <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 flex items-start space-x-4">
                    <div class="w-12 h-12 bg-emerald-500/10 border border-emerald-500/30 rounded-xl flex items-center justify-center text-emerald-400 flex-shrink-0">
                        <i data-lucide="code" class="w-6 h-6"></i>
                    </div>
                    <div class="space-y-1">
                        <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">Lead Developer</span>
                        <h3 class="font-semibold text-base">Priyam</h3>
                        <p class="text-xs text-slate-400">Full-Stack Automation Lead (AUCSE)</p>
                        <p class="text-xs text-slate-500 pt-1">Designed backend Playwright pipelines, FastAPI WebSocket integrations, and frontend UI.</p>
                    </div>
                </div>

            </div>
        </section>

    </main>

    <footer class="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        &copy; Adamas Knowledge City Automated Feedback Agent. Built with FastAPI & Playwright.
    </footer>

    <script>
        lucide.createIcons();

        const defaultSubjectsList = """ + str(DEFAULT_SUBJECTS) + """;
        document.getElementById("subjectsInput").value = defaultSubjectsList.join(", ");

        function resetDefaultSubjects() {
            document.getElementById("subjectsInput").value = defaultSubjectsList.join(", ");
        }

        const clientId = Math.random().toString(36).substring(7);
        const wsProtocol = location.protocol === "https:" ? "wss:" : "ws:";
        const ws = new WebSocket(`${wsProtocol}//${location.host}/ws/${clientId}`);

        const statusIndicator = document.getElementById("statusIndicator");

        ws.onopen = () => {
            statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-emerald-500";
            addLog("Connected to WebSocket server.", "info");
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if(data.type === "status") {
                if(data.status === "TASK_SUCCESS") {
                    statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-emerald-500";
                } else {
                    statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-rose-500";
                }
            }
            addLog(data.message, data.type || "info");
        };

        ws.onclose = () => {
            statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-slate-600";
            addLog("WebSocket disconnected.", "warning");
        };

        function addLog(message, type = "info") {
            const logsDiv = document.getElementById("logs");
            const div = document.createElement("div");
            
            let color = "text-slate-300";
            if (type === "error") color = "text-rose-400 font-semibold";
            if (type === "warning") color = "text-amber-400";
            if (type === "success") color = "text-emerald-400";

            const timestamp = new Date().toLocaleTimeString();
            div.className = `${color} leading-relaxed flex items-start space-x-2`;
            div.innerHTML = `<span class="text-slate-600 flex-shrink-0">[${timestamp}]</span> <span>${message}</span>`;
            
            logsDiv.appendChild(div);
            logsDiv.scrollTop = logsDiv.scrollHeight;
        }

        function clearLogs() {
            document.getElementById("logs").innerHTML = "";
        }

        async function startAutomation() {
            const reg_no = document.getElementById("regNo").value;
            const password = document.getElementById("password").value;
            const rawSubjects = document.getElementById("subjectsInput").value;

            if (!reg_no || !password) {
                addLog("Validation Error: Missing registration number or password.", "error");
                return;
            }

            const subjects = rawSubjects.split(",").map(s => s.trim()).filter(Boolean);

            statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse";
            addLog("Initiating request to background worker...", "info");

            try {
                const response = await fetch(`/api/submit-feedback?client_id=${clientId}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ reg_no, password, subjects })
                });

                const data = await response.json();
                if (data.status === "error") {
                    addLog(data.message, "error");
                    statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-rose-500";
                } else {
                    addLog(data.message, "info");
                }
            } catch (error) {
                addLog("HTTP Request Failed: " + error, "error");
                statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-rose-500";
            }
        }
    </script>
</body>
</html>
"""


# main.py (at the very bottom)
if __name__ == "__main__":
    import uvicorn
    import os

    # Read the PORT environment variable provided by Render (defaults to 8000 for local testing)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)