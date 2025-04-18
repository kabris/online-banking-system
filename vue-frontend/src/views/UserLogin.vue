<template>
  <div class="login-container">
    <h2>Login</h2>
    
    <form @submit.prevent="login">
      <input v-model="email" type="text" placeholder="Enter Email" required />
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

        console.log("Login Successful! Role:", data.role); // 🔍 Debugging

        // ✅ Redirect based on role
        if (data.role === "customer") {
          console.log("Redirecting to /customer-dashboard"); // 🔍 Debugging
          this.$router.push("/customer-dashboard");
        } else if (data.role === "system_admin") {
          console.log("Redirecting to /admin-dashboard"); // 🔍 Debugging
          this.$router.push("/admin-dashboard");
        } else if (data.role === "it_security") {
          console.log("Redirecting to /security-dashboard"); // 🔍 Debugging
          this.$router.push("/security-dashboard");
        } else {
          throw new Error("Invalid user role");
        }
      } catch (error) {
        this.errorMessage = error.message;
        console.error("Login Error:", error); // 🔍 Debugging
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
