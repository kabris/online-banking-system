<template>
  <div class="login-container">
    <h2>{{ pageTitle }}</h2> <!-- Title changes based on user type -->
    
    <form @submit.prevent="login">
      <input v-model="email" type="text" placeholder="Enter Email or Account Number" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  computed: {
    pageTitle() {
      const role = this.$route.query.role;
      if (role === "customer") return "Customer Login";
      if (role === "system_admin") return "System Admin Login";
      if (role === "it_security") return "IT Security Expert Login";
      return "User Login";
    },
  },
  methods: {
    async login() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: this.email, password: this.password }),
        });
        
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || "Invalid login credentials");
        }

        // Redirect based on user role
        if (data.role === "customer") {
          this.$router.push("/CustomerDashboard");
        } else if (data.role === "system_admin") {
          this.$router.push("/AdminDashboard");
        } else if (data.role === "it_security") {
          this.$router.push("/SecurityDashboard");
        } else {
          throw new Error("Invalid user role");
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  text-align: center;
  padding: 20px;
}

.error {
  color: red;
  font-size: 14px;
}
</style>
