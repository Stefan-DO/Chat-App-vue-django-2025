<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <h1 class="auth-header glitch">$$Welcome$$</h1>

      <ul class="nav nav-tabs justify-content-center mb-3">
        <li class="nav-item">
          <button
            class="nav-link"
            :class="{ active: activeTab === 'signup' }"
            @click="activeTab = 'signup'"
          >
            Sign Up
          </button>
        </li>
        <li class="nav-item">
          <button
            class="nav-link"
            :class="{ active: activeTab === 'signin' }"
            @click="activeTab = 'signin'"
          >
            Sign In
          </button>
        </li>
      </ul>

      <div v-if="activeTab === 'signup'">
        <form @submit.prevent="signUp">
          <div class="mb-3">
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="Email"
              required
            />
          </div>
          <div class="mb-3">
            <input
              v-model="username"
              type="text"
              class="form-control"
              placeholder="Username"
              required
            />
          </div>
          <div class="mb-3">
            <input
              v-model="password"
              type="password"
              class="form-control"
              placeholder="Password"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary">Sign Up</button>
        </form>
      </div>

      <div v-else>
        <form @submit.prevent="signIn">
          <div class="mb-3">
            <input
              v-model="username"
              type="text"
              class="form-control"
              placeholder="Username"
              required
            />
          </div>
          <div class="mb-3">
            <input
              v-model="password"
              type="password"
              class="form-control"
              placeholder="Password"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary">Sign In</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const activeTab = ref('signup')
const email = ref('')
const username = ref('')
const password = ref('')

// SIGN UP
async function signUp() {
  try {
    await axios.post(
      'http://localhost:8000/auth/users/',
      {
        email: email.value,
        username: username.value,
        password: password.value,
      },
      { headers: { Authorization: '' } }
    )
    alert('Account created successfully. Logging in...')
    await signIn()
  } catch (error) {
    console.error('Sign-up error:', error)
    alert(
      error.response?.data?.detail ||
        JSON.stringify(error.response?.data) ||
        'Sign-up failed.'
    )
  }
}

// SIGN IN
async function signIn() {
  try {
    const { data } = await axios.post(
      'http://localhost:8000/auth/token/login/',
      { username: username.value, password: password.value },
      { headers: { 'Content-Type': 'application/json', Authorization: '' } }
    )

    localStorage.setItem('app_auth_token', data.auth_token)
    localStorage.setItem('username', username.value)
    axios.defaults.headers.common['Authorization'] = `Token ${data.auth_token}`

    router.push('/chats')
  } catch (error) {
    console.error('Sign-in error:', error)
    alert(
      error.response?.data?.detail ||
        JSON.stringify(error.response?.data) ||
        'Login failed.'
    )
  }
}
</script>

<style scoped>
input::placeholder {
  color: #dbc9bc; /* change to any color you like */
  opacity: 1; /* ensures full visibility */
}
.auth-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #06070a;
  font-family: 'Orbitron', sans-serif;
  color: #fff;
}

.auth-card {
  background: rgba(10, 10, 10, 0.95);
  border: 2px solid #ff003c;
  box-shadow: 0 0 20px rgba(255, 0, 60, 0.5);
  border-radius: 8px;
  padding: 2rem 3rem;
  width: 380px;
  text-align: center;
}

.auth-header {
  font-size: 1.8rem;
  font-weight: 700;
  color: #ff003c;
  text-transform: uppercase;
  letter-spacing: 3px;
  margin-bottom: 1rem;
}

.nav-tabs .nav-link {
  color: #aaa;
  font-weight: 600;
  border: none;
  background: transparent;
}

.nav-tabs .nav-link.active {
  color: #ff003c;
  border-bottom: 2px solid #ff003c;
}

input.form-control {
  background-color: #111;
  border: 1px solid #ff003c;
  color: #fff;
  border-radius: 4px;
}

input.form-control:focus {
  outline: none;
  box-shadow: 0 0 10px #ff003c;
  border-color: #ff003c;
}

.btn-primary {
  background: linear-gradient(90deg, #ff003c, #ff6a00);
  border: none;
  color: #fff;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  width: 100%;
  padding: 10px;
  transition: 0.2s;
}

.btn-primary:hover {
  transform: scale(1.03);
  box-shadow: 0 0 10px #ff003c;
}

/* Glitch flicker effect for title */
.glitch {
  position: relative;
  color: #ff003c;
  animation: flicker 2s infinite;
}

@keyframes flicker {
  0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
    opacity: 1;
  }
  20%, 24%, 55% {
    opacity: 0.3;
  }
}
</style>
