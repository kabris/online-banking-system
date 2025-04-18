<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="registerUser">
      <input v-model="email" type="email" placeholder="Enter Email" required />
      <input v-model="password" type="password" placeholder="Enter Password" required />
      <select v-model="role" required>
        <option value="" disabled>Select Role</option>
        <option value="customer">Customer</option>
        <option value="security">IT Security Expert</option>
        <option value="admin">System Administrator</option>
      </select>
      <button type="submit">Register</button>
    </form>
    <p>Already have an account? <router-link to="/login">Login</router-link></p>
  </div>
</template>

<script>
export default {
  name: "UserRegister",
  data() {
    return {
      email: "",
      password: "",
      role: ""
    };
  },
  methods: {
    registerUser() {
      if (!this.email || !this.password || !this.role) {
        alert("Please fill in all fields.");
        return;
      }
      
      // Save user details (mock backend)
      const userData = { email: this.email, password: this.password, role: this.role };
      localStorage.setItem(this.email, JSON.stringify(userData));

      alert("Registration Successful! You can now login.");
      this.$router.push("/login"); // Redirect to login page
    }
  }
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background-image: url('@/assets/background.jpg');
  background-size: cover;
  background-position: center;
  border-radius: 8px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  color: #2c3e50;
}

input, select {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  background: #27ae60;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  width: 100%;
}

p {
  margin-top: 15px;
}
</style>
