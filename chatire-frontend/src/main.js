import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import './assets/main.css'
// Bootstrap 5 (no jQuery)
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('app_auth_token')}`
// Mount the Vue app
createApp(App)
  .use(router)
  .mount('#app')
