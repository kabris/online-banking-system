<template>
  <nav class="AppNavbar">
    <img :src="require('/src/assets/logo.png')" alt="Bank Logo" class="logo" />
    <h1>Secure Bank</h1>
    <button @click="toggleDarkMode">Toggle Mode</button>
  </nav>
</template>

<script>
export default {
  name: "AppNavbar",
  methods: { 
    toggleDarkMode() { 
      document.body.classList.toggle('dark-mode'); 
      document.querySelector('.AppNavbar').classList.toggle('dark-mode'); 
    } 
  }
};
</script>

<style scoped>
/* Navbar container */
.AppNavbar {
  background: #3498db;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
  font-size: 18px;
  font-weight: bold;
}

/* Logo image */
.logo {
  height: 50px;
  margin-right: 10px;
}

/* Dark mode styles */
.dark-mode {
  background: black !important;
  color: white !important;
}

/* Toggle button */
button {
  background: white;
  color: #3498db;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #ddd;
}

/* Landing page background */
.landing-page {
  background-image: url('/src/assets/background.jpg');
  background-size: cover;
  background-position: center;
}
</style>
