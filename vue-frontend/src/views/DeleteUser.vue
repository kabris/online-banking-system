<template>
  <div class="delete-user-container">
    <h2>Secure Bank</h2>
    <h3 class="title">Delete User</h3> <!-- Title should always be visible -->

    <form @submit.prevent="submitForm">
      <!-- User Type -->
      <label class="input-label">User Type:</label>
      <select v-model="userType" class="input-field" @change="resetFields" required>
        <option value="">Select User Type</option>
        <option value="customer">Customer</option>
        <option value="admin">System Administrator</option>
        <option value="itsec">IT Security Expert</option>
      </select>

      <!-- Account Number (only for Customers) -->
      <div v-if="userType === 'customer'">
        <label class="input-label">Account Number:</label>
        <input type="text" v-model="accountNumber" class="input-field"
               placeholder="Enter 8-character account number"
               @input="limitAccountNumber"
               required />
      </div>

      <!-- Email Address -->
      <label class="input-label">Email Address:</label>
      <input type="text" v-model="email" class="input-field"
             placeholder="Enter email"
             @blur="validateEmail"
             required />

      <!-- Password Field -->
      <label class="input-label">Password:</label>
      <input type="password" v-model="password" class="input-field"
             placeholder="8 chars: 2U, 2L, 4D"
             @input="limitPassword"
             required />

      <!-- Error Message -->
      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

      <!-- Delete Button -->
      <button type="submit" class="submit-btn" :disabled="!canDeleteUser()">Delete User</button>
    </form>
  </div>
</template>
<script>
export default {
  data() {
    return {
      userType: '',
      accountNumber: '',
      email: '',
      password: '',
      errorMessage: '' // Store error messages
    };
  },
  methods: {
    resetFields() {
      this.accountNumber = ''; 
      this.email = ''; 
      this.password = ''; 
      this.errorMessage = ''; // Clear error messages
    },
    limitAccountNumber() {
      this.accountNumber = this.accountNumber.replace(/[^a-z0-9]/g, '').slice(0, 8);
      
      const pattern = /^\d{6}[a-z]{2}$/; 
      if (this.accountNumber.length === 8 && !pattern.test(this.accountNumber)) {
        this.errorMessage = "Invalid account number! Must be 6 digits followed by 2 lowercase letters (e.g., 123456ab).";
        this.accountNumber = "";
      } else {
        this.errorMessage = "";
      }
    },
    validateEmail() {
      const customerPattern = /^(?!sysadmin|itsec)[a-zA-Z0-9._%+-]+@gmail\.com$/;
      const itsecPattern = /^itsec[0-9]+@gmail\.com$/;
      const adminPattern = /^sysadmin[0-9]+@gmail\.com$/;

      if (
        (this.userType === 'customer' && !customerPattern.test(this.email)) ||
        (this.userType === 'itsec' && !itsecPattern.test(this.email)) ||
        (this.userType === 'admin' && !adminPattern.test(this.email))
      ) {
        this.errorMessage = `Invalid email for ${this.userType}. Example: ${
          this.userType === 'customer' ? 'john01@gmail.com (Cannot start with sysadmin or itsec)' :
          this.userType === 'itsec' ? 'itsec123@gmail.com' : 'sysadmin007@gmail.com'
        }`;
        this.email = "";
      } else {
        this.errorMessage = "";
      }
    },
    limitPassword() {
      this.password = this.password.replace(/[^A-Za-z0-9]/g, '').slice(0, 8);
      const pattern = /^(?=(.*[A-Z]){2})(?=(.*[a-z]){2})(?=(.*\d){4})[A-Za-z\d]{8}$/;
      if (this.password.length === 8 && !pattern.test(this.password)) {
        this.errorMessage = "Password must be exactly 8 characters: 2 uppercase, 2 lowercase, and 4 digits.";
        this.password = "";
      } else {
        this.errorMessage = "";
      }
    },
    canDeleteUser() {
      return this.userType && this.email && this.password && (this.userType !== 'customer' || this.accountNumber);
    },
    submitForm() {
      this.validateEmail();
      if (!this.userType || !this.email || !this.password || (this.userType === 'customer' && !this.accountNumber)) {
        this.errorMessage = "Please fill in all required fields correctly.";
        return;
      }
      alert("User deleted successfully!");
      this.resetFields();
    }
  }
};
</script>
<style scoped>
.delete-user-container {
  text-align: center;
  max-width: 400px;
  margin: auto;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.1);
}

.title {
  font-weight: bold;
  font-size: 18px;
  color: #222; /* Ensure visibility */
  margin-bottom: 10px;
}

.input-label {
  font-weight: bold;
  color: #222; 
  display: block;
  margin: 8px 0 5px;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #444;
  border-radius: 4px;
  color: #000;
  background-color: #f8f8f8;
}

.error-text {
  color: red;
  font-size: 14px;
  margin-top: 5px;
}

.submit-btn {
  width: 100%;
  background-color: #007bff;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-btn:hover {
  background-color: #0056b3;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
