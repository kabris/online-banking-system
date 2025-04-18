<template>
  <div class="add-user-container">
    <h2>Secure Bank</h2>
    <h3>Add User</h3>
    <form @submit.prevent="submitForm">

      <!-- User Type -->
      <label class="input-label">User Type:</label>
      <select v-model="userType" class="input-field" @change="resetEmail" required>
        <option value="">Select User Type</option>
        <option value="customer">Customer</option>
        <option value="admin">System Administrator</option>
        <option value="itsec">IT Security Expert</option>
      </select>

      <!-- Email Address -->
      <label class="input-label">Email Address:</label>
      <input type="text" v-model="email" class="input-field"
             placeholder="Enter email" @blur="validateEmail" required />

      <!-- Phone Number with Country Code -->
      <label class="input-label">Phone Number:</label>
      <div class="phone-input">
        <select v-model="countryCode" class="country-code">
          <option value="+254">+254 (Kenya)</option>
          <option value="+255">+255 (Tanzania)</option>
          <option value="+256">+256 (Uganda)</option>
          <option value="+250">+250 (Rwanda)</option>
          <option value="+257">+257 (Burundi)</option>
          <option value="+251">+251 (Ethiopia)</option>
          <option value="+252">+252 (Somalia)</option>
          <option value="+211">+211 (South Sudan)</option>
        </select>
        <input type="text" v-model="phoneNumber" class="input-field"
               placeholder="Enter phone number" @input="validatePhone" required />
      </div>

      <!-- Password Field -->
      <label class="input-label">Password:</label>
      <input type="password" v-model="password" class="input-field"
          placeholder="8 chars: 2U, 2L, 4D" @blur="validatePassword" maxlength="8" required />  

      <button type="submit" class="submit-btn">Add User</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userType: '',
      email: '',
      countryCode: '+254', // Default Kenya
      phoneNumber: '',
      password: ''
    };
  },
  methods: {
    resetEmail() {
      this.email = ''; // Clear email when role changes
    },
    validateEmail() {
      if (!this.email || !this.userType) return;

      const patterns = {
        customer: /^(?!itsec|sysadmin)[a-zA-Z]+[0-9]*@gmail\.com$/, // ✅ Restricts "sysadmin" & "itsec"
        itsec: /^itsec[0-9]+@gmail\.com$/,  // ✅ Allow any "itsecXXX@gmail.com"
        admin: /^sysadmin[0-9]+@gmail\.com$/ // ✅ Allow any "sysadminXXX@gmail.com"
      };

      if (!patterns[this.userType].test(this.email)) {
        alert(`Invalid email for ${this.userType}. Example: ${
          this.userType === 'customer' ? 'john01@gmail.com' :
          this.userType === 'itsec' ? 'itsec123@gmail.com' : 'sysadmin007@gmail.com'
        }`);
        this.email = "";
      }
    },
    validatePhone() {
      this.phoneNumber = this.phoneNumber.replace(/[^0-9]/g, ''); // Only numbers

      if (this.phoneNumber.length > 9) {
        this.phoneNumber = this.phoneNumber.slice(0, 9); // Ensure max 9 digits
      }

      if (this.phoneNumber.length < 9) {
        return; // Allow user to enter digits until 9
      }

      if (this.phoneNumber.startsWith("0")) {
        alert("Phone number should not start with 0. Start with 1-9.");
        this.phoneNumber = "";
      }
    },
    validatePassword() {
      // Password pattern: exactly 8 characters, 2 uppercase, 2 lowercase, 4 digits
      const passwordPattern = /^(?=(.*[A-Z]){2})(?=(.*[a-z]){2})(?=(.*\d){4})[A-Za-z\d]{8}$/;
      if (!passwordPattern.test(this.password)) {
        alert("Password must be exactly 8 characters, with 2 uppercase, 2 lowercase, and 4 digits.");
        this.password = "";
      }
    },
    submitForm() {
      this.validateEmail();
      this.validatePhone();
      this.validatePassword();

      if (!this.userType || !this.email || !this.phoneNumber || !this.password) {
        alert("Please fill in all required fields correctly.");
        return;
      }

      // ✅ Simulate user addition (Replace with actual API call if needed)
      alert("User added successfully!");

      // ✅ Clear fields after adding user
      this.userType = "";
      this.email = "";
      this.phoneNumber = "";
      this.countryCode = "+254"; // Reset to default (Kenya)
      this.password = "";
    }
  }
};
</script>

<style scoped>
.add-user-container {
  text-align: center;
  max-width: 400px;
  margin: auto;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.1);
}

/* ✅ Darker Labels */
.input-label {
  font-weight: bold;
  color: #222; /* Darker text */
  display: block;
  margin: 8px 0 5px;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #444; /* Darker border */
  border-radius: 4px;
  color: #000;
  background-color: #f8f8f8;
}

.phone-input {
  display: flex;
  gap: 5px;
}

.country-code {
  width: 30%;
  padding: 10px;
  border: 1px solid #444;
  border-radius: 4px;
  font-size: 14px;
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
</style>
