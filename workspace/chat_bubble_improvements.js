// Enhanced message positioning based on who sent it
const positionMessage = (messageDiv, type) => {
    // Better cleanup of message content to prevent overlap
    // User messages: right-aligned with rounded corners pointing left
    // Sara messages: left-aligned with rounded corners pointing right
    this.addMessage = function(type, content, timestamp = Date.now()) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.style.marginBottom = type === 'user' ? '1.2rem' : '1.5rem';
        
        const avatar = document.createElement('div');
        avatar.className = `avatar ${type}`;
        avatar.textContent = type === 'user' ? 'B' : 'S';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'timestamp';
        timeDiv.textContent = new Date(timestamp).toLocaleTimeString();
        
        messageContent.appendChild(timeDiv);
        
        if (type === 'user') {
            // User: avatar on right, content first
            messageDiv.appendChild(messageContent);
            messageDiv.appendChild(avatar);
        } else {
            // Sara: avatar first, then content
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(messageContent);
        }
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    };
};

// Prevent message clutter by limiting message density
const debounceScroll = () => {
    let scrollTimeout;
    return () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            if (this.messagesContainer) {
                this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
            }
        }, 100);
    };
};

// Clean message formatting function
const formatMessageText = (text) => {
    // Remove any character formatting that might cause display issues
    return text.replace(/\[\?\d+[hlmK]/g, '').trim();
};

// Enhanced bubble positioning to prevent overlap