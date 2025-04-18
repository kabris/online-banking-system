<template>
  <div class="landing-page">
    <img src="@/assets/logo.png" alt="Bank Logo" class="logo" />
    <h1>Welcome to Secure Online Banking</h1>

    <div class="role-selection">
      <h2>Select Your Role</h2>
      <div class="buttons-container">
        <button class="role-btn" @click="selectRole('customer')">Customer</button>
        <button class="role-btn" @click="selectRole('admin')">System Admin</button>
        <button class="role-btn" @click="selectRole('security')">IT Security Expert</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedRole: ''
    };
  },
  methods: {
    selectRole(role) {
      this.selectedRole = role;
      console.log(`Selected Role: ${this.selectedRole}`);

      // Navigate based on the selected role
      this.navigateToLoginPage();
    },
    navigateToLoginPage() {
      if (this.selectedRole === 'customer') {
        this.$router.push('/customer-login');
      } else if (this.selectedRole === 'admin') {
        this.$router.push('/admin-login');
      } else if (this.selectedRole === 'security') {
        this.$router.push('/security-login');
      } else {
        console.error('Role not recognized');
      }
    }
  }
};
</script>


<style scoped>
.landing-page {
  text-align: center;
  height: 100vh;
  background-image: url("@/assets/background.jpg");
  background-size: cover;
  background-position: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
}

.logo {
  width: 150px;
  margin-bottom: 20px;
}

.role-selection {
  margin-top: 20px;
}

.buttons-container {
  display: flex;
  gap: 15px; /* Adds spacing between buttons */
  justify-content: center;
}

.role-btn {
  padding: 15px 25px;
  background: #3498db;
  color: white;
  border-radius: 5px;
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.role-btn:hover {
  background: #2980b9;
}
</style>
