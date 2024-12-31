// Thêm sự kiện click cho nút "Go"
document.getElementById('go').addEventListener('click', function () {
    fetch('/compare')
.then(response => {
if (!response.ok) {
    throw new Error('Network response was not ok ' + response.statusText);
}
// Chuyển hướng sang trang mới
window.location.href = '/compare';
})
.catch(error => {
console.error('There has been a problem with your fetch operation:', error);
});

});
    function toggleChatbot() {
        const chatbot = document.querySelector('.chatbot');
        chatbot.classList.toggle('hidden');
    }


    document.getElementById('send_btn').addEventListener('click', function () {
        const userInput = document.getElementById('user_input').value.trim();
    
        if (userInput === '') {
            alert('Please enter a message!');
            return;
        }
    
        const messagesContainer = document.getElementById('chatbot_messages');
    
        // Hiển thị tin nhắn của user
        const userMessage = document.createElement('div');
        userMessage.className = 'user-message';
        userMessage.innerText = userInput;
        messagesContainer.appendChild(userMessage);
    
        // Hiển thị trạng thái "Processing..."
        const processingMessage = document.createElement('div');
        processingMessage.className = 'bot-message';
        processingMessage.innerText = 'Processing...';
        messagesContainer.appendChild(processingMessage);
    
        // Tự động cuộn xuống cuối
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
        // Gọi API Flask
        fetch('/api/chat_bot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_text: userInput }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    processingMessage.innerHTML = `<span style="color: red;">Error: ${data.error}</span>`;
                } else {
                    // Loại bỏ dấu '*' trước khi hiển thị
                    const cleanedResponse = data.response.replace(/\*/g, '');
                    processingMessage.innerText = cleanedResponse;
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                processingMessage.innerHTML = `<span style="color: red;">Error connecting to the server.</span>`;
            })
            .finally(() => {
                // Tự động cuộn xuống cuối
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            });
    
        // Xóa input sau khi gửi
        document.getElementById('user_input').value = '';
    });
    