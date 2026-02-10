<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nodus AI</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --sidebar-bg: #171717;
            --main-bg: #0a0a0a;
            --message-ai: #1e1e1e;
            --message-user: #2d2d2d;
            --accent: #10a37f;
            --accent-hover: #0d8c6d;
            --text-primary: #ffffff;
            --text-secondary: #8e8ea0;
            --border: #2a2a2a;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--main-bg); color: var(--text-primary); height: 100vh; overflow: hidden; }
        
        .app-container { display: flex; height: 100vh; }
        
        /* SIDEBAR */
        .sidebar {
            width: 260px;
            background: var(--sidebar-bg);
            display: flex;
            flex-direction: column;
            height: 100%;
            border-right: 1px solid var(--border);
            transition: transform 0.3s;
        }
        .sidebar.hidden { transform: translateX(-100%); }
        
        .new-chat-btn {
            margin: 12px;
            padding: 12px;
            background: var(--accent);
            border: none;
            border-radius: 8px;
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 500;
        }
        
        .chat-history { flex: 1; overflow-y: auto; padding: 12px; }
        
        .time-group { margin-bottom: 20px; }
        .time-header {
            font-size: 12px;
            color: var(--text-secondary);
            padding: 8px 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .chat-item {
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            margin: 4px 0;
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
        }
        .chat-item:hover { background: rgba(255,255,255,0.05); }
        .chat-item.active { background: rgba(255,255,255,0.08); }
        .chat-item.pinned { background: rgba(255,193,7,0.1); }
        .chat-item.pinned .pin-icon { color: #ffc107; }
        
        .chat-actions {
            display: none;
            position: absolute;
            right: 8px;
            background: var(--sidebar-bg);
            border-radius: 6px;
            border: 1px solid var(--border);
            overflow: hidden;
            z-index: 10;
        }
        .chat-item:hover .chat-actions { display: block; }
        
        .chat-action-btn {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 6px 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            width: 100%;
            white-space: nowrap;
        }
        .chat-action-btn:hover { background: rgba(255,255,255,0.05); }
        .chat-action-btn.delete { color: #ef4444; }
        
        .pin-icon { color: var(--text-secondary); font-size: 12px; }
        
        /* MAIN CONTENT */
        .main-content { flex: 1; display: flex; flex-direction: column; }
        
        .top-bar {
            padding: 16px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border);
            background: var(--sidebar-bg);
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }
        
        .message {
            display: flex;
            gap: 20px;
            animation: slideIn 0.3s;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .input-container {
            padding: 20px;
            border-top: 1px solid var(--border);
            background: var(--sidebar-bg);
        }
        
        .input-wrapper {
            max-width: 768px;
            margin: 0 auto;
            position: relative;
        }
        
        .chat-input {
            width: 100%;
            padding: 16px;
            background: #334155;
            border: 2px solid #475569;
            border-radius: 12px;
            color: white;
            font-size: 16px;
            resize: none;
            min-height: 56px;
            line-height: 1.5;
            font-family: inherit;
        }
        .chat-input:focus { outline: none; border-color: var(--accent); }
        
        .send-btn {
            position: absolute;
            right: 10px;
            bottom: 10px;
            background: var(--accent);
            border: none;
            width: 36px;
            height: 36px;
            border-radius: 8px;
            color: white;
            cursor: pointer;
        }
        
        /* MODALS */
        .modal {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        
        .modal-content {
            background: var(--sidebar-bg);
            padding: 40px;
            border-radius: 16px;
            width: 90%;
            max-width: 400px;
            border: 1px solid var(--border);
        }
        
        .modal-title {
            font-size: 24px;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .modal-buttons {
            display: flex;
            gap: 12px;
            margin-top: 20px;
        }
        
        .modal-btn {
            flex: 1;
            padding: 12px;
            border-radius: 8px;
            border: none;
            font-weight: 500;
            cursor: pointer;
        }
        .modal-btn.cancel { background: transparent; border: 1px solid var(--border); color: var(--text-primary); }
        .modal-btn.delete { background: #ef4444; color: white; }
        
        .google-btn {
            background: #4285f4;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            cursor: pointer;
            margin-bottom: 16px;
        }
        
        .divider {
            display: flex;
            align-items: center;
            margin: 20px 0;
            color: var(--text-secondary);
        }
        .divider::before, .divider::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid var(--border);
        }
        .divider span { padding: 0 16px; }
        
        /* RESPONSIVE */
        @media (max-width: 768px) {
            .sidebar { position: fixed; z-index: 100; }
            .top-bar { padding: 12px; }
        }
    </style>
</head>
<body>
    <!-- Login Modal -->
    <div id="loginModal" class="modal">
        <div class="modal-content">
            <h2 class="modal-title">Welcome to Nodus AI</h2>
            <p style="text-align: center; color: var(--text-secondary); margin-bottom: 30px;">
                Sign in to start chatting with Nodus
            </p>
            
            <button class="google-btn" onclick="loginWithGoogle()">
                <i class="fab fa-google"></i> Sign in with Google
            </button>
            
            <div class="divider">
                <span>Or continue with email</span>
            </div>
            
            <input type="email" id="email" placeholder="Email address" style="width: 100%; padding: 14px; background: #334155; border: 1px solid #475569; border-radius: 8px; color: white; margin-bottom: 12px;">
            <input type="password" id="password" placeholder="Password" style="width: 100%; padding: 14px; background: #334155; border: 1px solid #475569; border-radius: 8px; color: white; margin-bottom: 20px;">
            
            <div class="modal-buttons">
                <button class="modal-btn cancel" onclick="showCreateAccount()">Create Account</button>
                <button class="modal-btn delete" onclick="login()">Sign In</button>
            </div>
            
            <div style="text-align: center; margin-top: 20px; color: var(--text-secondary); font-size: 12px;">
                By signing in, you agree to our <a href="#" style="color: var(--accent);">Terms of Service</a> and <a href="#" style="color: var(--accent);">Privacy Policy</a>
            </div>
        </div>
    </div>

    <!-- Create Account Modal -->
    <div id="createAccountModal" class="modal" style="display: none;">
        <div class="modal-content">
            <h2 class="modal-title">Create Account</h2>
            
            <button class="google-btn" onclick="loginWithGoogle()">
                <i class="fab fa-google"></i> Sign up with Google
            </button>
            
            <div class="divider">
                <span>Or sign up with email</span>
            </div>
            
            <input type="text" id="signupName" placeholder="Full name" style="width: 100%; padding: 14px; background: #334155; border: 1px solid #475569; border-radius: 8px; color: white; margin-bottom: 12px;">
            <input type="email" id="signupEmail" placeholder="Email address" style="width: 100%; padding: 14px; background: #334155; border: 1px solid #475569; border-radius: 8px; color: white; margin-bottom: 12px;">
            <input type="password" id="signupPassword" placeholder="Password" style="width: 100%; padding: 14px; background: #334155; border: 1px solid #475569; border-radius: 8px; color: white; margin-bottom: 12px;">
            <input type="password" id="signupConfirm" placeholder="Confirm password" style="width: 100%; padding: 14px; background: #334155; border: 1px solid #475569; border-radius: 8px; color: white; margin-bottom: 20px;">
            
            <div class="modal-buttons">
                <button class="modal-btn cancel" onclick="showLogin()">Back to Login</button>
                <button class="modal-btn delete" onclick="createAccount()">Create Account</button>
            </div>
        </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div id="deleteModal" class="modal" style="display: none;">
        <div class="modal-content">
            <h2 class="modal-title">Delete Chat</h2>
            <p style="text-align: center; color: var(--text-secondary); margin-bottom: 30px;">
                Are you sure you want to delete this chat? This action cannot be undone.
            </p>
            
            <div class="modal-buttons">
                <button class="modal-btn cancel" onclick="closeDeleteModal()">Cancel</button>
                <button class="modal-btn delete" onclick="confirmDelete()">Delete Chat</button>
            </div>
        </div>
    </div>

    <!-- Rename Chat Modal -->
    <div id="renameModal" class="modal" style="display: none;">
        <div class="modal-content">
            <h2 class="modal-title">Rename Chat</h2>
            
            <input type="text" id="newChatName" placeholder="Enter new chat name" style="width: 100%; padding: 14px; background: #334155; border: 1px solid #475569; border-radius: 8px; color: white; margin-bottom: 20px;">
            
            <div class="modal-buttons">
                <button class="modal-btn cancel" onclick="closeRenameModal()">Cancel</button>
                <button class="modal-btn delete" onclick="confirmRename()">Rename</button>
            </div>
        </div>
    </div>

    <!-- Main App -->
    <div class="app-container" id="appContainer" style="display: none;">
        <!-- Sidebar -->
        <div class="sidebar" id="sidebar">
            <button class="new-chat-btn" onclick="newChat()">
                <i class="fas fa-plus"></i> New Chat
            </button>
            
            <div class="chat-history" id="chatHistory">
                <!-- Chat history will load here with time groups -->
            </div>
            
            <div style="padding: 20px; border-top: 1px solid var(--border);">
                <div style="display: flex; align-items: center; gap: 12px; cursor: pointer;" onclick="logout()">
                    <div style="width: 36px; height: 36px; background: linear-gradient(45deg, #2563eb, #3b82f6); border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                        <i class="fas fa-user"></i>
                    </div>
                    <div>
                        <div id="userName" style="font-weight: 500;">User</div>
                        <div style="font-size: 12px; color: var(--text-secondary);">Free Plan</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <!-- Top Bar -->
            <div class="top-bar">
                <button onclick="toggleSidebar()" style="background: transparent; border: 1px solid var(--border); color: white; width: 36px; height: 36px; border-radius: 8px; cursor: pointer;">
                    <i class="fas fa-bars"></i>
                </button>
                
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="fas fa-brain" style="color: var(--accent);"></i>
                    <span id="currentChatTitle" style="font-weight: 500;">New Chat</span>
                </div>
                
                <div style="display: flex; gap: 10px;">
                    <button onclick="shareChat()" style="background: transparent; border: 1px solid var(--border); color: white; padding: 8px 16px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                        <i class="fas fa-share"></i> Share
                    </button>
                </div>
            </div>

            <!-- Chat Container -->
            <div class="chat-messages" id="chatMessages">
                <!-- Welcome Screen -->
                <div id="welcomeScreen" style="text-align: center; padding: 60px 20px;">
                    <div style="width: 80px; height: 80px; background: linear-gradient(45deg, #2563eb, #3b82f6); border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 40px; margin: 0 auto 30px;">
                        🤖
                    </div>
                    
                    <h1 style="font-size: 36px; margin-bottom: 20px; background: linear-gradient(45deg, #2563eb, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        Welcome to Nodus AI
                    </h1>
                    
                    <p style="color: var(--text-secondary); font-size: 18px; margin-bottom: 40px; max-width: 600px; margin-left: auto; margin-right: auto;">
                        Chat with Nodus AI - an advanced language model for coding, writing, analysis, and creative tasks.
                    </p>
                    
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin: 20px 0; max-width: 400px; margin-left: auto; margin-right: auto;">
                        <div style="background: rgba(59, 130, 246, 0.1); padding: 12px; border-radius: 8px; text-align: center; font-size: 14px;">💻 Code Generation</div>
                        <div style="background: rgba(59, 130, 246, 0.1); padding: 12px; border-radius: 8px; text-align: center; font-size: 14px;">📝 Content Writing</div>
                        <div style="background: rgba(59, 130, 246, 0.1); padding: 12px; border-radius: 8px; text-align: center; font-size: 14px;">🔍 Research & Analysis</div>
                        <div style="background: rgba(59, 130, 246, 0.1); padding: 12px; border-radius: 8px; text-align: center; font-size: 14px;">🎨 Creative Projects</div>
                    </div>
                </div>
            </div>

            <!-- Input Area -->
            <div class="input-container">
                <div class="input-wrapper">
                    <textarea class="chat-input" id="chatInput" placeholder="Message Nodus AI..." rows="1"></textarea>
                    <button class="send-btn" onclick="sendMessage()">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // ========== STATE MANAGEMENT ==========
        let currentUser = null;
        let currentChat = null;
        let chats = JSON.parse(localStorage.getItem('nodusChats') || '[]');
        let chatToDelete = null;
        let chatToRename = null;
        let isTyping = false;

        // ========== INITIALIZATION ==========
        document.addEventListener('DOMContentLoaded', function() {
            // Check for saved user
            const savedUser = localStorage.getItem('nodusUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                showApp();
            }
            
            // Setup Enter key to send message
            const textarea = document.getElementById('chatInput');
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });
            
            // Setup auto-resize for textarea
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 120) + 'px';
            });
            
            // Load chat history
            renderChatHistory();
        });

        // ========== AUTHENTICATION ==========
        function loginWithGoogle() {
            // Simulate Google login
            currentUser = {
                id: 'google_' + Date.now(),
                name: 'Google User',
                email: 'user@gmail.com',
                avatar: 'G',
                plan: 'free'
            };
            
            localStorage.setItem('nodusUser', JSON.stringify(currentUser));
            showApp();
        }
        
        function login() {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (!email || !password) {
                alert('Please enter email and password');
                return;
            }
            
            currentUser = {
                id: 'user_' + Date.now(),
                name: email.split('@')[0],
                email: email,
                avatar: email[0].toUpperCase()
            };
            
            localStorage.setItem('nodusUser', JSON.stringify(currentUser));
            showApp();
        }
        
        function showCreateAccount() {
            document.getElementById('loginModal').style.display = 'none';
            document.getElementById('createAccountModal').style.display = 'flex';
        }
        
        function showLogin() {
            document.getElementById('createAccountModal').style.display = 'none';
            document.getElementById('loginModal').style.display = 'flex';
        }
        
        function createAccount() {
            const name = document.getElementById('signupName').value;
            const email = document.getElementById('signupEmail').value;
            const password = document.getElementById('signupPassword').value;
            const confirm = document.getElementById('signupConfirm').value;
            
            if (!name || !email || !password || !confirm) {
                alert('Please fill all fields');
                return;
            }
            
            if (password !== confirm) {
                alert('Passwords do not match');
                return;
            }
            
            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                email: email,
                avatar: name[0].toUpperCase()
            };
            
            localStorage.setItem('nodusUser', JSON.stringify(currentUser));
            showApp();
        }
        
        function logout() {
            if (confirm('Are you sure you want to logout?')) {
                localStorage.removeItem('nodusUser');
                currentUser = null;
                document.getElementById('appContainer').style.display = 'none';
                document.getElementById('loginModal').style.display = 'flex';
            }
        }

        // ========== CHAT FUNCTIONS ==========
        function newChat() {
            const chatId = 'chat_' + Date.now();
            currentChat = {
                id: chatId,
                title: 'New Chat',
                messages: [],
                createdAt: Date.now(),
                updatedAt: Date.now(),
                pinned: false
            };
            
            chats.unshift(currentChat);
            saveChats();
            renderChatHistory();
            showChat();
            
            // Focus on input
            document.getElementById('chatInput').focus();
        }

        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (!message || isTyping) return;
            
            // Create new chat if none exists
            if (!currentChat) {
                newChat();
            }
            
            // Add user message
            addMessage(message, 'user');
            input.value = '';
            input.style.height = 'auto';
            
            // Show typing indicator
            showTyping();
            
            // Simulate AI response
            setTimeout(() => {
                hideTyping();
                const response = generateAIResponse(message);
                addMessage(response, 'ai');
                
                // Update chat title with first message
                if (currentChat.messages.length === 2) {
                    currentChat.title = message.substring(0, 30) + (message.length > 30 ? '...' : '');
                    saveChats();
                    renderChatHistory();
                    updateChatTitle();
                }
                
                isTyping = false;
            }, 1000 + Math.random() * 1000);
        }

        function addMessage(content, sender) {
            const message = {
                id: 'msg_' + Date.now(),
                content: content,
                sender: sender,
                timestamp: Date.now()
            };
            
            currentChat.messages.push(message);
            currentChat.updatedAt = Date.now();
            saveChats();
            
            // Show chat container if welcome screen is visible
            if (document.getElementById('welcomeScreen').style.display !== 'none') {
                document.getElementById('welcomeScreen').style.display = 'none';
            }
            
            // Add message to UI
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message`;
            messageDiv.innerHTML = `
                <div style="width: 36px; height: 36px; background: ${sender === 'user' ? '#475569' : '#10a37f'}; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    ${sender === 'user' ? (currentUser?.avatar || 'U') : 'N'}
                </div>
                <div style="flex: 1;">
                    <div style="margin-bottom: 8px; font-weight: 500;">
                        ${sender === 'user' ? (currentUser?.name || 'You') : 'Nodus AI'}
                    </div>
                    <div style="line-height: 1.6;">
                        ${formatMessage(content)}
                    </div>
                </div>
            `;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function generateAIResponse(message) {
            const responses = [
                `I'm Nodus AI! I understand you're asking about "${message}". How can I help you further?`,
                `Thanks for your message! Regarding "${message}", I can assist with that.`,
                `I see you mentioned "${message}". Let me help you with that.`,
                `Great question! For "${message}", here's what I can suggest...`,
                `I'm Nodus AI - ready to assist! Regarding "${message}", I can provide detailed information.`
            ];
            
            if (message.toLowerCase().includes('hello') || message.toLowerCase().includes('hi')) {
                return `Hello! I'm Nodus AI. How can I help you today?`;
            }
            
            return responses[Math.floor(Math.random() * responses.length)];
        }

        // ========== CHAT HISTORY ORGANIZATION ==========
        function renderChatHistory() {
            const chatHistory = document.getElementById('chatHistory');
            chatHistory.innerHTML = '';
            
            if (chats.length === 0) {
                chatHistory.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-secondary);">No chats yet</div>';
                return;
            }
            
            // Separate pinned chats
            const pinnedChats = chats.filter(chat => chat.pinned);
            const unpinnedChats = chats.filter(chat => !chat.pinned);
            
            // Group chats by time
            const now = Date.now();
            const oneDay = 24 * 60 * 60 * 1000;
            const sevenDays = 7 * oneDay;
            const thirtyDays = 30 * oneDay;
            
            const todayChats = [];
            const yesterdayChats = [];
            const last7DaysChats = [];
            const last30DaysChats = [];
            const olderChats = [];
            
            unpinnedChats.forEach(chat => {
                const diff = now - chat.createdAt;
                
                if (diff < oneDay) {
                    todayChats.push(chat);
                } else if (diff < 2 * oneDay) {
                    yesterdayChats.push(chat);
                } else if (diff < sevenDays) {
                    last7DaysChats.push(chat);
                } else if (diff < thirtyDays) {
                    last30DaysChats.push(chat);
                } else {
                    olderChats.push(chat);
                }
            });
            
            // Render pinned chats
            if (pinnedChats.length > 0) {
                const pinnedGroup = document.createElement('div');
                pinnedGroup.className = 'time-group';
                pinnedGroup.innerHTML = `<div class="time-header">Pinned</div>`;
                pinnedChats.forEach(chat => {
                    pinnedGroup.innerHTML += createChatItemHTML(chat);
                });
                chatHistory.appendChild(pinnedGroup);
            }
            
            // Render today's chats
            if (todayChats.length > 0) {
                const todayGroup = document.createElement('div');
                todayGroup.className = 'time-group';
                todayGroup.innerHTML = `<div class="time-header">Today</div>`;
                todayChats.forEach(chat => {
                    todayGroup.innerHTML += createChatItemHTML(chat);
                });
                chatHistory.appendChild(todayGroup);
            }
            
            // Render yesterday's chats
            if (yesterdayChats.length > 0) {
                const yesterdayGroup = document.createElement('div');
                yesterdayGroup.className = 'time-group';
                yesterdayGroup.innerHTML = `<div class="time-header">Yesterday</div>`;
                yesterdayChats.forEach(chat => {
                    yesterdayGroup.innerHTML += createChatItemHTML(chat);
                });
                chatHistory.appendChild(yesterdayGroup);
            }
            
            // Render last 7 days chats
            if (last7DaysChats.length > 0) {
                const last7Group = document.createElement('div');
                last7Group.className = 'time-group';
                last7Group.innerHTML = `<div class="time-header">Previous 7 Days</div>`;
                last7DaysChats.forEach(chat => {
                    last7Group.innerHTML += createChatItemHTML(chat);
                });
                chatHistory.appendChild(last7Group);
            }
            
            // Render last 30 days chats
            if (last30DaysChats.length > 0) {
                const last30Group = document.createElement('div');
                last30Group.className = 'time-group';
                last30Group.innerHTML = `<div class="time-header">Previous 30 Days</div>`;
                last30DaysChats.forEach(chat => {
                    last30Group.innerHTML += createChatItemHTML(chat);
                });
                chatHistory.appendChild(last30Group);
            }
            
            // Render older chats
            if (olderChats.length > 0) {
                const olderGroup = document.createElement('div');
                olderGroup.className = 'time-group';
                olderGroup.innerHTML = `<div class="time-header">Older</div>`;
                olderChats.forEach(chat => {
                    olderGroup.innerHTML += createChatItemHTML(chat);
                });
                chatHistory.appendChild(olderGroup);
            }
        }

        function createChatItemHTML(chat) {
            const isActive = currentChat && currentChat.id === chat.id;
            return `
                <div class="chat-item ${isActive ? 'active' : ''} ${chat.pinned ? 'pinned' : ''}" onclick="showChat('${chat.id}')">
                    <i class="fas fa-comment chat-icon"></i>
                    <div style="flex: 1; overflow: hidden;">
                        <div style="font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${chat.title}</div>
                    </div>
                    ${chat.pinned ? '<i class="fas fa-thumbtack pin-icon"></i>' : ''}
                    
                    <div class="chat-actions">
                        <button class="chat-action-btn" onclick="event.stopPropagation(); togglePin('${chat.id}')">
                            <i class="fas ${chat.pinned ? 'fa-thumbtack-slash' : 'fa-thumbtack'}"></i>
                            ${chat.pinned ? 'Unpin' : 'Pin'}
                        </button>
                        <button class="chat-action-btn" onclick="event.stopPropagation(); renameChat('${chat.id}')">
                            <i class="fas fa-edit"></i>
                            Rename
                        </button>
                        <button class="chat-action-btn delete" onclick="event.stopPropagation(); showDeleteModal('${chat.id}')">
                            <i class="fas fa-trash"></i>
                            Delete
                        </button>
                    </div>
                </div>
            `;
        }

        // ========== CHAT MANAGEMENT ==========
        function showChat(chatId = null) {
            if (chatId) {
                currentChat = chats.find(c => c.id === chatId);
            }
            
            if (!currentChat) {
                document.getElementById('welcomeScreen').style.display = 'block';
                return;
            }
            
            document.getElementById('welcomeScreen').style.display = 'none';
            
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = '';
            
            currentChat.messages.forEach(msg => {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message`;
                messageDiv.innerHTML = `
                    <div style="width: 36px; height: 36px; background: ${msg.sender === 'user' ? '#475569' : '#10a37f'}; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                        ${msg.sender === 'user' ? (currentUser?.avatar || 'U') : 'N'}
                    </div>
                    <div style="flex: 1;">
                        <div style="margin-bottom: 8px; font-weight: 500;">
                            ${msg.sender === 'user' ? (currentUser?.name || 'You') : 'Nodus AI'}
                        </div>
                        <div style="line-height: 1.6;">
                            ${formatMessage(msg.content)}
                        </div>
                    </div>
                `;
                chatMessages.appendChild(messageDiv);
            });
            
            chatMessages.scrollTop = chatMessages.scrollHeight;
            updateChatTitle();
            renderChatHistory();
        }

        function togglePin(chatId) {
            const chat = chats.find(c => c.id === chatId);
            if (chat) {
                chat.pinned = !chat.pinned;
                saveChats();
                renderChatHistory();
            }
        }

        function renameChat(chatId) {
            chatToRename = chatId;
            const chat = chats.find(c => c.id === chatId);
            if (chat) {
                document.getElementById('newChatName').value = chat.title;
                document.getElementById('renameModal').style.display = 'flex';
            }
        }

        function closeRenameModal() {
            document.getElementById('renameModal').style.display = 'none';
            chatToRename = null;
        }

        function confirmRename() {
            const newName = document.getElementById('newChatName').value.trim();
            if (newName && chatToRename) {
                const chat = chats.find(c => c.id === chatToRename);
                if (chat) {
                    chat.title = newName;
                    saveChats();
                    renderChatHistory();
                    if (currentChat && currentChat.id === chatToRename) {
                        updateChatTitle();
                    }
                }
            }
            closeRenameModal();
        }

        function showDeleteModal(chatId) {
            chatToDelete = chatId;
            document.getElementById('deleteModal').style.display = 'flex';
        }

        function closeDeleteModal() {
            document.getElementById('deleteModal').style.display = 'none';
            chatToDelete = null;
        }

        function confirmDelete() {
            if (chatToDelete) {
                chats = chats.filter(c => c.id !== chatToDelete);
                if (currentChat && currentChat.id === chatToDelete) {
                    currentChat = null;
                    showChat();
                }
                saveChats();
                renderChatHistory();
            }
            closeDeleteModal();
        }

        function updateChatTitle() {
            if (currentChat) {
                document.getElementById('currentChatTitle').textContent = currentChat.title;
            }
        }

        // ========== UTILITY FUNCTIONS ==========
        function showApp() {
            document.getElementById('loginModal').style.display = 'none';
            document.getElementById('createAccountModal').style.display = 'none';
            document.getElementById('appContainer').style.display = 'flex';
            
            if (currentUser) {
                document.getElementById('userName').textContent = currentUser.name;
            }
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('hidden');
        }

        function showTyping() {
            isTyping = true;
            const chatMessages = document.getElementById('chatMessages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message';
            typingDiv.id = 'typingIndicator';
            typingDiv.innerHTML = `
                <div style="width: 36px; height: 36px; background: #10a37f; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    N
                </div>
                <div style="flex: 1;">
                    <div style="margin-bottom: 8px; font-weight: 500;">Nodus AI</div>
                    <div style="display: flex; gap: 4px; align-items: center;">
                        <div style="width: 8px; height: 8px; background: var(--text-secondary); border-radius: 50%; animation: typing 1.4s infinite;"></div>
                        <div style="width: 8px; height: 8px; background: var(--text-secondary); border-radius: 50%; animation: typing 1.4s infinite 0.2s;"></div>
                        <div style="width: 8px; height: 8px; background: var(--text-secondary); border-radius: 50%; animation: typing 1.4s infinite 0.4s;"></div>
                    </div>
                </div>
            `;
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function hideTyping() {
            const indicator = document.getElementById('typingIndicator');
            if (indicator) indicator.remove();
        }

        function formatMessage(text) {
            return text
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/`(.*?)`/g, '<code style="background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; font-family: monospace;">$1</code>')
                .replace(/\n/g, '<br>');
        }

        function saveChats() {
            localStorage.setItem('nodusChats', JSON.stringify(chats));
        }

        function shareChat() {
            if (!currentChat) {
                alert('No active chat to share');
                return;
            }
            
            const shareText = `Nodus AI Chat: ${currentChat.title}\n\n` +
                currentChat.messages.map(m => `${m.sender === 'user' ? 'You' : 'Nodus AI'}: ${m.content}`).join('\n\n');
            
            navigator.clipboard.writeText(shareText);
            alert('Chat copied to clipboard!');
        }
    </script>
</body>
</html>
