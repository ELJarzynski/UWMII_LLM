<template>
  <div class="chat-container">
    <div v-if="chatHistory.length" class="chat-history" ref="chatHistory">
      <div v-for="(entry, index) in chatHistory" :key="index" class="chat-entry">
        <div class="message user-message">
          <strong> </strong>
          <p>{{ entry.user }}   </p>
          <strong> </strong>
          <img src="./image/user.png" alt="User Icon" class="message-icon" />
        </div>
        <div class="message bot-message">
          <img src="./image/bot.png" alt="Bot Icon" class="message-icon" />
          <strong> </strong>
          <p>{{ entry.bot }}</p>
        </div>
      </div>
    </div>

    <div v-if="!isSending" class="message-input-container">
      <input
        v-model="userMessage"
        type="text"
        placeholder="Wpisz wiadomość..."
        class="message-input"
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage" class="send-button">Wyślij</button>
    </div>

    <div v-if="isSending" class="loading-container">
      <div class="spinner"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userMessage: '',
      botResponse: null,
      isSending: false,
      chatHistory: [],
    };
  },
  created() {
    this.loadChatHistory();
  },
  updated() {
    this.scrollToBottom();
  },
  methods: {
    async sendMessage() {
      if (this.userMessage.trim() === '') return;

      this.isSending = true;
      this.botResponse = null;

      try {
        await axios.post('http://localhost:8000/api/send-message/', {
          message: this.userMessage,
        });

        await this.getBotResponse();

        this.chatHistory.push({
          user: this.userMessage,
          bot: this.botResponse,
        });

        this.userMessage = '';
      } catch (error) {
        console.error('Error:', error);
        this.botResponse = 'Wystąpił błąd podczas komunikacji z botem.';
      } finally {
        this.isSending = false;
      }
    },

    async getBotResponse() {
    try {
        const response = await axios.post('http://localhost:8000/api/get-response-from-rag/', {
            message: this.userMessage, // Wysłanie wiadomości jako JSON
        });
        this.botResponse = response.data.response;
    } catch (error) {
        console.error('Error:', error);
        this.botResponse = 'Wystąpił błąd podczas pobierania odpowiedzi.';
    }
},



    async loadChatHistory() {
      try {
        const response = await axios.get('http://localhost:8000/api/get-chat-history/');
        this.chatHistory = response.data.history || [];
      } catch (error) {
        console.error('Error:', error);
        this.chatHistory = [];
      }
    },

    scrollToBottom() {
      const chatHistory = this.$refs.chatHistory;
      if (chatHistory) {
        chatHistory.scrollTop = chatHistory.scrollHeight;
      }
    },
  },
};
</script>

<style scoped>
body, html {
  height: 100%;
  margin: 0;
  display: flex;
  flex-direction: column;
  background-image: url('./image/uwmii.png');
  background-size: 25%;
  background-position: center;
  background-repeat: no-repeat;
}

.chat-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 600px;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  height: 100%;
  background-image: url('./image/uwmii.png');
  background-size: 25%;
  background-position: center;
  background-repeat: no-repeat;
}

.chat-history {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.chat-entry {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}

.message {
  padding: 10px;
  margin-bottom: 5px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  max-width: 80%;
}

.user-message {
  background-color: rgba(255, 255, 255, 1);
  align-self: flex-end;
}

.bot-message {
  background-color: rgba(255, 255, 255, 1);
  align-self: flex-start;
}

.message img {
  width: 30px;
  height: 30px;
  margin-right: 10px;
  border-radius: 50%;
}

.user-message img {
  margin-right: 10px;
  margin-left: 10px;
}

.bot-message img {
  margin-right: 10px;
}

.message-input-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.message-input {
  width: 80%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.send-button {
  padding: 10px 20px;
  background-color: #00796b;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.send-button:hover {
  background-color: #004d40;
}

.loading-container {
  text-align: center;
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #00796b;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
