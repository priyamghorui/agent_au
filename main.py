# import sys
# import asyncio
# import threading
# from typing import List, Optional
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse
# from pydantic import BaseModel

# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# from automation import submit_student_feedback, DEFAULT_SUBJECTS

# app = FastAPI(title="Auto Feedback Portal")

# class FeedbackRequest(BaseModel):
#     reg_no: str
#     password: str
#     subjects: Optional[List[str]] = None

# active_connections: dict[str, WebSocket] = {}

# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: str):
#     await websocket.accept()
#     active_connections[client_id] = websocket
#     try:
#         while True:
#             await websocket.receive_text()
#     except (WebSocketDisconnect, Exception):
#         active_connections.pop(client_id, None)

# async def send_progress(client_id: str, data: dict):
#     websocket = active_connections.get(client_id)
#     if websocket:
#         try:
#             await websocket.send_json(data)
#         except Exception:
#             active_connections.pop(client_id, None)

# def run_playwright_task(reg_no: str, password: str, subjects: Optional[List[str]], client_id: str):
#     async def runner():
#         async def progress_callback(payload: dict):
#             await send_progress(client_id, payload)

#         try:
#             result = await submit_student_feedback(
#                 reg_no, password, subjects, progress_callback
#             )
#             status = "TASK_SUCCESS" if result else "TASK_FAILED"
#             await send_progress(client_id, {"message": f"Execution finished: {status}", "type": "status", "status": status})
#         except Exception as e:
#             await send_progress(client_id, {"message": f"Fatal Task Failure: {str(e)}", "type": "error", "status": "TASK_ERROR"})

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
# async def start_feedback(req: FeedbackRequest, client_id: str):
#     if not req.reg_no.strip() or not req.password.strip():
#         return {"status": "error", "message": "Registration number and password are required."}

#     thread = threading.Thread(
#         target=run_playwright_task,
#         args=(req.reg_no, req.password, req.subjects, client_id),
#         daemon=True
#     )
#     thread.start()
#     return {"status": "started", "message": "Automation worker initialized."}

# @app.get("/")
# async def serve_index():
#     return HTMLResponse(content=INDEX_HTML)

# INDEX_HTML = """
# <!DOCTYPE html>
# <html lang="en" class="dark">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>AutoFeedback Pro - Adamas University</title>
#     <script src="https://cdn.tailwindcss.com"></script>
#     <script src="https://unpkg.com/lucide@latest"></script>
#     <script>
#         tailwind.config = {
#             darkMode: 'class',
#             theme: {
#                 extend: {
#                     colors: {
#                         brand: { 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca' }
#                     }
#                 }
#             }
#         }
#     </script>
#     <style>
#         ::-webkit-scrollbar { width: 6px; }
#         ::-webkit-scrollbar-track { background: #0f172a; }
#         ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
#     </style>
# </head>
# <body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans selection:bg-brand-500 selection:text-white">

#     <!-- Header Navigation -->
#     <header class="border-b border-slate-800 bg-slate-900/50 backdrop-blur sticky top-0 z-50">
#         <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
#             <div class="flex items-center space-x-3">
#                 <div class="p-2 bg-brand-600 rounded-lg shadow-lg shadow-brand-500/20">
#                     <i data-lucide="zap" class="w-5 h-5 text-white"></i>
#                 </div>
#                 <span class="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">AutoFeedback AI</span>
#             </div>
#             <nav class="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-400">
#                 <a href="#app" class="hover:text-white transition">App Portal</a>
#                 <a href="#demo" class="hover:text-white transition">Demo Walkthrough</a>
#                 <a href="#team" class="hover:text-white transition">Project Team</a>
#             </nav>
#         </div>
#     </header>

#     <main class="flex-grow max-w-7xl w-full mx-auto px-6 py-10 space-y-20">

#         <!-- App Section -->
#         <section id="app" class="grid lg:grid-cols-12 gap-8 items-start">
            
#             <!-- Left: Credentials & Subject Config -->
#             <div class="lg:col-span-5 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6 backdrop-blur">
#                 <div>
#                     <h2 class="text-xl font-semibold flex items-center gap-2">
#                         <i data-lucide="shield-check" class="w-5 h-5 text-brand-500"></i> Portal Login
#                     </h2>
#                     <p class="text-xs text-slate-400 mt-1">Automate your pending course evaluations safely.</p>
#                 </div>

#                 <div class="space-y-4">
#                     <div>
#                         <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Registration No.</label>
#                         <input type="text" id="regNo" placeholder="e.g., AU/2022/0001" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition">
#                     </div>
#                     <div>
#                         <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Password</label>
#                         <input type="password" id="password" placeholder="••••••••••••" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition">
#                     </div>
#                     <div>
#                         <div class="flex items-center justify-between mb-2">
#                             <label class="text-xs font-semibold text-slate-300 uppercase tracking-wider">Custom Subjects (Comma Separated)</label>
#                             <button onclick="resetDefaultSubjects()" class="text-[10px] text-brand-500 hover:underline">Reset Defaults</button>
#                         </div>
#                         <textarea id="subjectsInput" rows="4" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition leading-relaxed"></textarea>
#                     </div>

#                     <button id="submitBtn" onclick="startAutomation()" class="w-full py-3 bg-brand-600 hover:bg-brand-700 text-white font-medium text-sm rounded-xl shadow-lg shadow-brand-500/20 transition flex items-center justify-center space-x-2">
#                         <i data-lucide="play" class="w-4 h-4"></i>
#                         <span>Start Automated Submission</span>
#                     </button>
#                 </div>
#             </div>

#             <!-- Right: Real-time Live Log & Progress Stream -->
#             <div class="lg:col-span-7 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col h-[520px] backdrop-blur">
#                 <div class="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
#                     <div class="flex items-center space-x-2">
#                         <span id="statusIndicator" class="w-2.5 h-2.5 rounded-full bg-slate-600"></span>
#                         <h3 class="font-semibold text-sm">Real-time Execution Stream</h3>
#                     </div>
#                     <button onclick="clearLogs()" class="text-xs text-slate-400 hover:text-white flex items-center gap-1">
#                         <i data-lucide="trash-2" class="w-3.5 h-3.5"></i> Clear Log
#                     </button>
#                 </div>

#                 <div id="logs" class="flex-grow overflow-y-auto space-y-2 text-xs font-mono pr-2">
#                     <div class="text-slate-500 italic">Waiting for process initiation...</div>
#                 </div>
#             </div>
#         </section>

#         <!-- Demo Video Section -->
#         <section id="demo" class="space-y-6">
#             <div class="text-center max-w-2xl mx-auto space-y-2">
#                 <h2 class="text-2xl font-bold tracking-tight">Interactive Demonstration</h2>
#                 <p class="text-slate-400 text-sm">Watch the Playwright headless agent automatically identify pending course forms and submit evaluation reports.</p>
#             </div>
#             <div class="max-w-4xl mx-auto bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl aspect-video relative group flex items-center justify-center">
#                 <!-- Video Embed / Local Player Placeholder -->
#                 <video controls class="w-full h-full object-cover">
#                     <source src="https://drive.google.com/file/d/1n8fJNRiCvpT8705h0K7pxNlHdxs7Ykib/view?usp=sharing" type="video/mp4">
#                     Your browser does not support the video tag.
#                 </video>
#             </div>
#         </section>

#         <!-- Project Team Section -->
#         <section id="team" class="space-y-8">
#             <div class="text-center max-w-2xl mx-auto space-y-2">
#                 <h2 class="text-2xl font-bold tracking-tight">Project Team & Mentorship</h2>
#                 <p class="text-slate-400 text-sm">Developed under academic guidance at Adamas University.</p>
#             </div>

#             <div class="grid md:grid-cols-2 gap-6 max-w-3xl mx-auto">
                
#                 <!-- Project Mentor -->
#                 <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 flex items-start space-x-4">
#                     <div class="w-12 h-12 bg-indigo-500/10 border border-indigo-500/30 rounded-xl flex items-center justify-center text-brand-500 flex-shrink-0">
#                         <i data-lucide="graduation-cap" class="w-6 h-6"></i>
#                     </div>
#                     <div class="space-y-1">
#                         <span class="text-[10px] font-bold text-brand-500 uppercase tracking-wider">Project Mentor</span>
#                         <h3 class="font-semibold text-base">NA</h3>
#                         <p class="text-xs text-slate-400">Department of Computer Science & Engineering</p>
#                         <p class="text-xs text-slate-500 pt-1">Guided the architecture, security compliance, and automation workflow optimization.</p>
#                     </div>
#                 </div>

#                 <!-- Lead Developer -->
#                 <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 flex items-start space-x-4">
#                     <div class="w-12 h-12 bg-emerald-500/10 border border-emerald-500/30 rounded-xl flex items-center justify-center text-emerald-400 flex-shrink-0">
#                         <i data-lucide="code" class="w-6 h-6"></i>
#                     </div>
#                     <div class="space-y-1">
#                         <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">Lead Developer</span>
#                         <h3 class="font-semibold text-base">Priyam</h3>
#                         <p class="text-xs text-slate-400">Full-Stack Automation Lead (AUCSE)</p>
#                         <p class="text-xs text-slate-500 pt-1">Designed backend Playwright pipelines, FastAPI WebSocket integrations, and frontend UI.</p>
#                     </div>
#                 </div>

#             </div>
#         </section>

#     </main>

#     <footer class="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
#         &copy; Adamas Knowledge City Automated Feedback Agent. Built with FastAPI & Playwright.
#     </footer>

#     <script>
#         lucide.createIcons();

#         const defaultSubjectsList = """ + str(DEFAULT_SUBJECTS) + """;
#         document.getElementById("subjectsInput").value = defaultSubjectsList.join(", ");

#         function resetDefaultSubjects() {
#             document.getElementById("subjectsInput").value = defaultSubjectsList.join(", ");
#         }

#         const clientId = Math.random().toString(36).substring(7);
#         const wsProtocol = location.protocol === "https:" ? "wss:" : "ws:";
#         const ws = new WebSocket(`${wsProtocol}//${location.host}/ws/${clientId}`);

#         const statusIndicator = document.getElementById("statusIndicator");

#         ws.onopen = () => {
#             statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-emerald-500";
#             addLog("Connected to WebSocket server.", "info");
#         };

#         ws.onmessage = (event) => {
#             const data = JSON.parse(event.data);
#             if(data.type === "status") {
#                 if(data.status === "TASK_SUCCESS") {
#                     statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-emerald-500";
#                 } else {
#                     statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-rose-500";
#                 }
#             }
#             addLog(data.message, data.type || "info");
#         };

#         ws.onclose = () => {
#             statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-slate-600";
#             addLog("WebSocket disconnected.", "warning");
#         };

#         function addLog(message, type = "info") {
#             const logsDiv = document.getElementById("logs");
#             const div = document.createElement("div");
            
#             let color = "text-slate-300";
#             if (type === "error") color = "text-rose-400 font-semibold";
#             if (type === "warning") color = "text-amber-400";
#             if (type === "success") color = "text-emerald-400";

#             const timestamp = new Date().toLocaleTimeString();
#             div.className = `${color} leading-relaxed flex items-start space-x-2`;
#             div.innerHTML = `<span class="text-slate-600 flex-shrink-0">[${timestamp}]</span> <span>${message}</span>`;
            
#             logsDiv.appendChild(div);
#             logsDiv.scrollTop = logsDiv.scrollHeight;
#         }

#         function clearLogs() {
#             document.getElementById("logs").innerHTML = "";
#         }

#         async function startAutomation() {
#             const reg_no = document.getElementById("regNo").value;
#             const password = document.getElementById("password").value;
#             const rawSubjects = document.getElementById("subjectsInput").value;

#             if (!reg_no || !password) {
#                 addLog("Validation Error: Missing registration number or password.", "error");
#                 return;
#             }

#             const subjects = rawSubjects.split(",").map(s => s.trim()).filter(Boolean);

#             statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse";
#             addLog("Initiating request to background worker...", "info");

#             try {
#                 const response = await fetch(`/api/submit-feedback?client_id=${clientId}`, {
#                     method: "POST",
#                     headers: { "Content-Type": "application/json" },
#                     body: JSON.stringify({ reg_no, password, subjects })
#                 });

#                 const data = await response.json();
#                 if (data.status === "error") {
#                     addLog(data.message, "error");
#                     statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-rose-500";
#                 } else {
#                     addLog(data.message, "info");
#                 }
#             } catch (error) {
#                 addLog("HTTP Request Failed: " + error, "error");
#                 statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-rose-500";
#             }
#         }
#     </script>
# </body>
# </html>
# """


# # main.py (at the very bottom)
# if __name__ == "__main__":
#     import uvicorn
#     import os

#     # Read the PORT environment variable provided by Render (defaults to 8000 for local testing)
#     port = int(os.environ.get("PORT", 8000))
#     uvicorn.run("main:app", host="0.0.0.0", port=port)


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
    <title>Agentic AI - Adamas University</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚡</text></svg>">
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
             <a href="/" >
                
           
            <div class="flex items-center space-x-3">
                <div class="p-2 bg-brand-600 rounded-lg shadow-lg shadow-brand-500/20">
                    <i data-lucide="zap" class="w-5 h-5 text-white"></i>
                </div>
                <span class="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">Agentic AI</span>
            </div>
             </a>
            <nav class="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-400">
                <a href="#app" class="hover:text-white transition">App Portal</a>
                <a href="#demo" class="hover:text-white transition">Demo Walkthrough</a>
                <a href="#team" class="hover:text-white transition">Mentorship</a>
                <a href="#github" class="hover:text-white transition flex items-center gap-1.5">
        <i data-lucide="github" class="w-4 h-4"></i> GitHub
    </a>
                <a href="#join" class="hover:text-white transition">Join Team</a>
            </nav>
        </div>
    </header>

    <main class="flex-grow max-w-7xl w-full mx-auto px-6 py-10 space-y-20">
<!-- Feedback Agent Heading Section -->
<div class="border-b border-slate-800/80 pb-4 mb-6">
    <div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-[11px] font-semibold tracking-wide uppercase mb-2">
        <i data-lucide="bot" class="w-3.5 h-3.5"></i> Autonomous Agent v1.0
    </div>
    <h1 class="text-xl font-bold bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent leading-snug">
        Feedback Agent <span class="text-xs font-normal text-slate-400 block sm:inline">(Our First Agentic Model)</span>
    </h1>
    <p class="text-xs text-slate-400 mt-1">Automates pending course evaluations end-to-end via headless web interaction.</p>
</div>
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

        <!-- Demo Video Section (Google Drive Video Player) -->
        <section id="demo" class="space-y-6">
            <div class="text-center max-w-2xl mx-auto space-y-2">
                <h2 class="text-2xl font-bold tracking-tight">Interactive Demonstration</h2>
                <p class="text-slate-400 text-sm">Watch the Playwright headless agent automatically identify pending course forms and submit evaluation reports.</p>
            </div>
            <div class="max-w-4xl mx-auto bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl aspect-video relative">
                <!-- Embedded Google Drive Video Player -->
                <iframe 
                    src="https://drive.google.com/file/d/1n8fJNRiCvpT8705h0K7pxNlHdxs7Ykib/preview" 
                    class="w-full h-full border-0" 
                    allow="autoplay"
                    allowfullscreen>
                </iframe>
            </div>
        </section>

        <!-- Project Team & Mentorship Section (Added 3 Mentors) -->
        <section id="team" class="space-y-8">
            <div class="text-center max-w-2xl mx-auto space-y-2">
                <h2 class="text-2xl font-bold tracking-tight">Project Team & Mentorship</h2>
                <p class="text-slate-400 text-sm">Developed under academic guidance at Adamas University.</p>
            </div>

           <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
            <!-- Research Mentor -->
                <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 flex items-start space-x-4">
                    <div class="w-12 h-12 bg-indigo-500/10 border border-indigo-500/30 rounded-xl flex items-center justify-center text-brand-500 flex-shrink-0">
                        <i data-lucide="shield" class="w-6 h-6"></i>
                    </div>
                    <div class="space-y-1">
                        <span class="text-[10px] font-bold text-brand-500 uppercase tracking-wider">Lead Research Mentor</span>
                        <h3 class="font-semibold text-base">Kalyan Patra</h3>
                        <p class="text-xs text-slate-400">Department of CSE</p>
                        <p class="text-xs text-slate-500 pt-1">Guided browser automation reliability and exception recovery strategies.</p>
                    </div>
                </div>
                           <!-- Frontend Engineer -->
                <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 flex items-start space-x-4">
                    <div class="w-12 h-12 bg-sky-500/10 border border-sky-500/30 rounded-xl flex items-center justify-center text-sky-400 flex-shrink-0">
                        <i data-lucide="layout" class="w-6 h-6"></i>
                    </div>
                    <div class="space-y-1">
                        <span class="text-[10px] font-bold text-sky-400 uppercase tracking-wider">Frontend Engineer</span>
                        <h3 class="font-semibold text-base">Sanchita Ghosh</h3>
                        <p class="text-xs text-slate-400">UI/UX & Component Architect</p>
                        <p class="text-xs text-slate-500 pt-1">Implemented responsive Tailwind layouts, interactive dashboards, and client-side state handling.</p>
                    </div>
                </div>
            



                <!-- Backend Specialist -->
                <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 flex items-start space-x-4">
                    <div class="w-12 h-12 bg-amber-500/10 border border-amber-500/30 rounded-xl flex items-center justify-center text-amber-400 flex-shrink-0">
                        <i data-lucide="server" class="w-6 h-6"></i>
                    </div>
                    <div class="space-y-1">
                        <span class="text-[10px] font-bold text-amber-400 uppercase tracking-wider">Backend Specialist</span>
                        <h3 class="font-semibold text-base">Niraj Neogi     
                          <a href="https://www.nirajneogi.com/" target="_blank" rel="noopener noreferrer" class="text-amber-400 hover:text-amber-300 inline-flex items-center">
                www.nirajneogi.com
            </a></h3>
                        <p class="text-xs text-slate-400">API & Database Engineer</p>
                        <p class="text-xs text-slate-500 pt-1">Managed asynchronous database sessions, REST endpoints, and secure token authentication models.</p>
                    </div>
                </div>

                <!-- Academic Advisor -->
                <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 flex items-start space-x-4">
                    <div class="w-12 h-12 bg-indigo-500/10 border border-indigo-500/30 rounded-xl flex items-center justify-center text-brand-500 flex-shrink-0">
                        <i data-lucide="award" class="w-6 h-6"></i>
                    </div>
                    <div class="space-y-1">
                        <span class="text-[10px] font-bold text-brand-500 uppercase tracking-wider">Academic Advisor</span>
                        <h3 class="font-semibold text-base">Brajesh Kayal</h3>
                        <p class="text-xs text-slate-400">Department of CSE</p>
                        <p class="text-xs text-slate-500 pt-1">Provided technical review on asynchronous task scheduling and system scalability.</p>
                    </div>
                </div>

                <!-- Technical Coordinator -->
                <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 flex items-start space-x-4">
                    <div class="w-12 h-12 bg-indigo-500/10 border border-indigo-500/30 rounded-xl flex items-center justify-center text-brand-500 flex-shrink-0">
                        <i data-lucide="book-open" class="w-6 h-6"></i>
                    </div>
                    <div class="space-y-1">
                        <span class="text-[10px] font-bold text-brand-500 uppercase tracking-wider">Technical Coordinator</span>
                        <h3 class="font-semibold text-base">Sabuj Mandal</h3>
                        <p class="text-xs text-slate-400">Department of CSE</p>
                        <p class="text-xs text-slate-500 pt-1">Advised on web security standards, containerization, and backend integration.</p>
                    </div>
                </div>
    <!-- Lead Developer -->
                <div class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 flex items-start space-x-4">
                    <div class="w-12 h-12 bg-emerald-500/10 border border-emerald-500/30 rounded-xl flex items-center justify-center text-emerald-400 flex-shrink-0">
                        <i data-lucide="code" class="w-6 h-6"></i>
                    </div>
                    <div class="space-y-1">
                        <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">DevOps Engineer</span>
                        <h3 class="font-semibold text-base">Priyam Ghorui
                        <a href="https://www.priyamghorui.com/" target="_blank" rel="noopener noreferrer" class="text-emerald-400 hover:text-emerald-300 inline-flex items-center">
                www.priyamghorui.com
            </a>
                        </h3>
                        <p class="text-xs text-slate-400">Full-Stack And Automation </p>
                        <p class="text-xs text-slate-500 pt-1">Designed backend Playwright pipelines, FastAPI WebSocket integrations, and frontend UI.</p>
                    </div>
                </div>
               
            </div>
        </section>
<!-- GitHub Repository Section -->
<section id="github" class="space-y-6">
    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-8 shadow-xl backdrop-blur max-w-4xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <div class="space-y-2 text-center md:text-left">
            <div class="flex items-center justify-center md:justify-start space-x-2">
                <i data-lucide="github" class="w-6 h-6 text-white"></i>
                <h2 class="text-xl font-bold tracking-tight">Open Source Codebase</h2>
            </div>
            <p class="text-sm text-slate-400 max-w-xl">
                Explore the source code, contribute enhancements, or inspect the Playwright automation pipelines and FastAPI architecture on GitHub.
            </p>
        </div>

        <a href="https://github.com/priyamghorui/deterministicAgent.git" 
           target="_blank" 
           rel="noopener noreferrer" 
           class="px-6 py-3 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white font-medium text-sm rounded-xl shadow-lg transition flex items-center space-x-2 flex-shrink-0 group">
            <i data-lucide="github" class="w-4 h-4 group-hover:scale-110 transition-transform"></i>
            <span>View Repository</span>
            <i data-lucide="external-link" class="w-3.5 h-3.5 text-slate-400 group-hover:text-white transition"></i>
        </a>
    </div>
</section>
        <!-- Join Team Form (Powered by FormSubmit) -->
        <section id="join" class="space-y-6">
            <div class="text-center max-w-2xl mx-auto space-y-2">
                <h2 class="text-2xl font-bold tracking-tight">Join Our Project Team</h2>
                <p class="text-slate-400 text-sm">Interested in collaborating on browser automation, web dev, or AI projects? Send us your details!</p>
            </div>

            <div class="max-w-xl mx-auto bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur">
                <!-- Replace 'your-email@example.com' with your destination email address -->
                <form action="https://formsubmit.co/priyamghorui2004@gmail.com" method="POST" class="space-y-4">
                    <!-- FormSubmit Configuration -->
                    <input type="hidden" name="_subject" value="New Project Join Application - AutoFeedback AI">
                    <input type="hidden" name="_captcha" value="false">
                    <input type="hidden" name="_template" value="table">

                    <div>
                        <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Project Name</label>
                        <input type="text" name="Project_Name" value="Agentic AI" readonly class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-400 focus:outline-none cursor-not-allowed">
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Your Full Name</label>
                        <input type="text" name="Full_Name" required placeholder="John Doe" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition">
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Contact Details (Email / Phone)</label>
                        <input type="text" name="Contact_Details" required placeholder="john@example.com or +91 9876543210" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition">
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Area of Interest</label>
                        <select name="Area_of_Interest" required class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition">
                            <option value="" disabled selected>Select your domain</option>
                            <option value="Frontend Development (React/Tailwind)">Frontend Development (React/Tailwind)</option>
                            <option value="Backend Development (FastAPI/Node.js)">Backend Development (FastAPI/Node.js)</option>
                            <option value="Browser Automation & Scraping (Playwright)">Browser Automation & Scraping (Playwright)</option>
                            <option value="Machine Learning / AI">Machine Learning / AI</option>
                            <option value="UI/UX Design">UI/UX Design</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Brief Note / Message (Optional)</label>
                        <textarea name="Message" rows="3" placeholder="Tell us about your experience or why you want to join..." class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition leading-relaxed"></textarea>
                    </div>

                    <button type="submit" class="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-sm rounded-xl shadow-lg shadow-emerald-500/20 transition flex items-center justify-center space-x-2">
                        <i data-lucide="send" class="w-4 h-4"></i>
                        <span>Submit Application</span>
                    </button>
                </form>
            </div>
        </section>

    </main>

    <footer class="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        &copy; Develop and maintain by Priyam Ghorui      <a href="https://www.priyamghorui.com/" target="_blank" rel="noopener noreferrer" class="text-emerald-400 hover:text-emerald-300 inline-flex items-center">
                www.priyamghorui.com
            </a>
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
    const submitBtn = document.getElementById("submitBtn");

    // Helper functions to manage button UI state
    function disableSubmitButton() {
        submitBtn.disabled = true;
        submitBtn.classList.add("opacity-50", "cursor-not-allowed");
        submitBtn.classList.remove("hover:bg-brand-700");
        submitBtn.innerHTML = `
            <i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i>
            <span>Automation Running...</span>
        `;
        lucide.createIcons();
    }

    function enableSubmitButton() {
        submitBtn.disabled = false;
        submitBtn.classList.remove("opacity-50", "cursor-not-allowed");
        submitBtn.classList.add("hover:bg-brand-700");
        submitBtn.innerHTML = `
            <i data-lucide="play" class="w-4 h-4"></i>
            <span>Start Automated Submission</span>
        `;
        lucide.createIcons();
    }

    ws.onopen = () => {
        statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-emerald-500";
        addLog("Connected to WebSocket server.", "info");
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        // Handle task status updates to re-enable button when execution completes
        if (data.type === "status") {
            if (data.status === "TASK_SUCCESS") {
                statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-emerald-500";
            } else {
                statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-rose-500";
            }
            // Re-enable button when task finishes or fails
            enableSubmitButton();
        }

        if (data.type === "error" && data.status === "TASK_ERROR") {
            statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-rose-500";
            enableSubmitButton();
        }

        addLog(data.message, data.type || "info");
    };

    ws.onclose = () => {
        statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-slate-600";
        addLog("WebSocket disconnected.", "warning");
        enableSubmitButton();
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

        // Immediately disable the button to prevent duplicate executions
        disableSubmitButton();

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
                enableSubmitButton();
            } else {
                addLog(data.message, "info");
            }
        } catch (error) {
            addLog("HTTP Request Failed: " + error, "error");
            statusIndicator.className = "w-2.5 h-2.5 rounded-full bg-rose-500";
            enableSubmitButton();
        }
    }
</script>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
