<template>
  <div class="change-password">
    <h3>Change Password</h3>
    <input type="text" v-model="accountOrEmail" placeholder="Enter Account Number or Email" />
    <input type="password" v-model="oldPassword" placeholder="Enter Old Password" />
    <input type="password" v-model="newPassword" placeholder="Enter New Password" />
    <input type="password" v-model="confirmPassword" placeholder="Confirm New Password" />
    <button @click="updatePassword">Update Password</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      accountOrEmail: '',
      oldPassword: '',
      newPassword: '',
      confirmPassword: '',
    };
  },
  methods: {
    updatePassword() {
      if (this.newPassword !== this.confirmPassword) {
        alert("Passwords do not match!");
        return;
      }
      console.log(`Updating password for ${this.accountOrEmail}`);
      alert("Password updated successfully!");
    },
  },
};
</script>

<style scoped>
.change-password {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
}
input {
  display: block;
  width: 100%;
  padding: 8px;
  margin: 5px 0;
}
button {
  background: #3498db;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
}
</style>
