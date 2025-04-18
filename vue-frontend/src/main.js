import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import './assets/styles.css';
import './assets/background.jpg';
import './assets/logo.png';

const app = createApp(App);
app.use(router).use(store).mount('#app');

