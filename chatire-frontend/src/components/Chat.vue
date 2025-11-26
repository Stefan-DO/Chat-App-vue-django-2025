<template>
  <div class="chat-wrapper">
    <div class="chat-header">MESSAGES</div>

    <div class="chat-body">
      <div v-for="(m, i) in messages" :key="i" class="message-row">
        <!-- Outgoing -->
        <div v-if="m.user.username === username" class="message outgoing">
          <p class="text">{{ m.message }}</p>
          <span class="sender">{{ m.user.username }}</span>
        </div>

        <!-- Incoming -->
        <div v-else class="message incoming">
          <p class="text">{{ m.message }}</p>
          <span class="sender">{{ m.user.username }}</span>
        </div>
      </div>
    </div>

    <form @submit.prevent="sendMessage" class="chat-input">
      <input v-model="input" type="text" placeholder="Type a message..." />
      <button type="submit">Send</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const messages = ref([])
const input = ref('')
const chatUri = ref(route.params.uri || null)
const token = localStorage.getItem('app_auth_token')
const username = localStorage.getItem('username')
const sessionStarted = ref(false)

function connectWebSocket() {
  ws = new WebSocket(`ws://localhost:8000/ws/chat/${chatUri.value}/`)
  ws.onopen = () => console.log('WebSocket connected')
  ws.onmessage = e => {
    const data = JSON.parse(e.data)
    messages.value.push({
      message: data.message,
      user: { username: data.username }
    })
  }
}


onMounted(async () => {
  try {
    if (!chatUri.value) {
      // Create new chat session if URI not provided
      const createRes = await axios.post(
        'http://localhost:8000/chat/sessions/',
        {},
        { headers: { Authorization: `Token ${token}` } }
      )
      chatUri.value = createRes.data.uri
      router.push(`/chats/${chatUri.value}`)
    } else {
      // Join existing chat session
      await joinChatSession()
    }

    await fetchChatSessionHistory()
    sessionStarted.value = true
  } catch (err) {
    console.error('Error creating or joining chat:', err)
    alert('Could not create or join chat. Please check login or server.')
  }
})


async function joinChatSession() {
  try {
    const res = await axios.patch(
      `http://localhost:8000/chat/sessions/${chatUri.value}/`,
      { username },
      { headers: { Authorization: `Token ${token}` } }
    )

    const user = res.data.members.find((m) => m.username === username)
    if (user) {
      console.log('Joined chat successfully')
    } else {
      alert('Could not join chat session.')
    }
  } catch (err) {
    console.error('Join chat failed:', err)
  }
}

async function fetchChatSessionHistory() {
  try {
    const res = await axios.get(
      `http://localhost:8000/chat/sessions/${chatUri.value}/messages/`,
      { headers: { Authorization: `Token ${token}` } }
    )
    messages.value = res.data.messages || []
  } catch (err) {
    console.error('Failed to fetch chat history:', err)
  }
}

async function sendMessage() {
  const text = input.value.trim()
  if (!text) return
  try {
    const res = await axios.post(
      `http://localhost:8000/chat/sessions/${chatUri.value}/messages/`,
      { message: text },
      { headers: { Authorization: `Token ${token}` } }
    )
    messages.value.push(res.data)
    input.value = ''
  } catch (err) {
    console.error('Error sending message:', err)
    alert('Could not send message. Please try again.')
  }
}
</script>

<style scoped>

.card {
  border-radius: 1rem;
}
</style>
<style scoped>
.chat-wrapper {
  background-color: #06070a;
  color: #fff;
  font-family: 'Orbitron', sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.chat-header {
  color: #ff1b1c;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 2px;
  border-bottom: 2px solid #ff1b1c;
  width: 80%;
  text-align: left;
  padding: 10px;
  font-size: 1.2rem;
}

.chat-body {
  width: 80%;
  height: 60vh;
  background-color: #0e0f14;
  border: 2px solid #ff1b1c;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  overflow-y: auto;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message-row {
  display: flex;
  flex-direction: column;
}

.message {
  padding: 10px 15px;
  border-radius: 4px;
  max-width: 60%;
  position: relative;
}

.incoming {
  background-color: rgba(255, 255, 0, 0.1);
  border: 1px solid #ffc300;
  color: #ffc300;
  align-self: flex-start;
}

.outgoing {
  background-color: rgba(0, 255, 255, 0.1);
  border: 1px solid #00ffe7;
  color: #00ffe7;
  align-self: flex-end;
}

.sender {
  font-size: 0.7rem;
  opacity: 0.7;
  position: absolute;
  bottom: -15px;
  right: 10px;
}

.text {
  margin: 0;
}

.chat-input {
  width: 80%;
  display: flex;
  margin-top: 20px;
}

.chat-input input {
  flex: 1;
  background-color: #0e0f14;
  border: 2px solid #ff1b1c;
  color: #fff;
  padding: 10px;
  outline: none;
}

.chat-input button {
  background-color: #ff1b1c;
  border: none;
  color: #fff;
  padding: 10px 20px;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.chat-input button:hover {
  background-color: #ff4041;
}
</style>
