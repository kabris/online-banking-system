<template>
  <div class="dashboard">
    <!-- Account Details Box -->
    <section class="box grey">
      <h3>📄 Account Details</h3>
      <p><strong>Balance:</strong> Kshs.50,000</p>
    </section>

    <!-- Transaction History Box -->
    <section class="box maroon">
      <h3>📜 Transaction History</h3>
      <p>🔻 Payment to ABC Corp - Kshs.2,000</p>
      <p>🔺 Received from XYZ - Kshs.5,000</p>
    </section>

    <!-- Fund Transfer Box -->
    <section class="box blue">
      <h3>💰 Fund Transfer</h3>
      <label>Recipient Phone Number</label>
      <select v-model="countryCode">
        <option v-for="(code, country) in countryCodes" :key="country" :value="code">
          {{ code }} ({{ country }})
        </option>
      </select>
      <input type="text" v-model="phoneNumber" @input="validatePhoneNumber" placeholder="Phone Number" class="small-input" maxlength="9"/>


      <label>Amount</label>
      <input type="number" v-model="amount" @input="validateAmount" placeholder="Enter Amount" class="small-input" />

      <!-- Success Message -->
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

      <button @click="transferFunds" :disabled="!phoneNumber || !amount || amount > 100000">Transfer</button>
    </section>

    <!-- File Upload Box -->
    <section class="box green">
      <h3>📂 Upload Documents</h3>
      <FileUpload :allowedTypes="['.docx', '.doc', '.xls', '.jpeg', '.pdf', '.jpg']" />
    </section>

    <!-- Security Settings Box -->
    <section class="box orange">
      <h2>🔒 Security Settings</h2>

      <div class="button-container">
        <button @click="$router.push('/change-password')" class="nav-button">🔒 Change Password</button>
        <button @click="$router.push('/enable-mfa')" class="nav-button">🔐 Enable MFA</button>
        <button @click="$router.push('/notifications')" class="nav-button">📢 Notifications</button>
        <button @click="$router.push('/login-history')" class="nav-button">📜 Login History</button>
      </div>
    </section>

    <!-- About Us Section -->
    <footer class="about-us">
      <h3>About Us</h3>
      <p>For contact support, reach us at:</p>
      <p><strong>Website:</strong> <a href="#">www.sizu@bank.com</a></p>
      <p><strong>Email:</strong> <a href="#">sizubank254@gmail.com</a></p>
      <p><strong>Phone:</strong> +254 757 598 337</p>
      <p><strong>Follow us on:</strong> 
        <a href="#">Facebook</a> | 
        <a href="#">Twitter</a> | 
        <a href="#">LinkedIn</a>
      </p>
    </footer>
  </div>
</template>

<script>
import FileUpload from '@/components/FileUpload.vue';

export default {
  components: { FileUpload },
  data() {
    return {
      countryCode: "+254",
      phoneNumber: "",
      amount: "",
      successMessage: "", // ✅ Properly initialized
      countryCodes: {
        "USA": "+1", "UK": "+44", "Uganda": "+256", "Canada": "+1", "Germany": "+49",
        "France": "+33", "India": "+91", "China": "+86", "Japan": "+81", "Australia": "+61",
        "South Africa": "+27", "Kenya": "+254", "Brazil": "+55", "Mexico": "+52"
      }
    };
  },
  methods: {
    validateAmount() {
      if (this.amount > 100000) {
        alert("Amount exceeds transfer limit!");
      }
    },
    validatePhoneNumber() {
      // Remove any non-numeric characters
      this.phoneNumber = this.phoneNumber.replace(/\D/g, '');
      
      // Ensure the first digit is between 1-9
      if (this.phoneNumber.length > 0 && !/^[1-9]/.test(this.phoneNumber)) {
        alert("Phone number must start with a digit from 1 to 9.");
        this.phoneNumber = ""; // Clear invalid input
      }
      
      // Restrict to exactly 9 digits
      if (this.phoneNumber.length > 9) {
        alert("Phone number must be exactly 9 digits long.");
        this.phoneNumber = this.phoneNumber.slice(0, 9); // Trim to 9 digits
      }
    },
    transferFunds() {
      // 🛑 Input Validation
      if (!this.phoneNumber || this.phoneNumber.startsWith("0")) {
        alert("Invalid phone number! Do not start with 0.");
        return;
      }

      // Validate phone number length
      if (this.phoneNumber.length !== 9) {
        alert("Phone number must be exactly 9 digits long.");
        return;
      }

      if (!this.amount || this.amount <= 0) {
        alert("Please enter a valid transfer amount.");
        return;
      }

      if (this.amount > 100000) {
        alert("Transaction not allowed! Amount exceeds limit.");
        return;
      }

      // 🚀 Show success message
      this.successMessage = `✅ Transaction successful! Sent Kshs. ${this.amount} to ${this.countryCode} ${this.phoneNumber}`;

      // 🛑 Log transaction AFTER updating values
      console.log(`✅ Transferring Kshs. ${this.amount} to ${this.countryCode} ${this.phoneNumber}`);

      // ✅ Clear input fields after successful transfer
      setTimeout(() => {
        this.phoneNumber = "";
        this.amount = "";
        this.successMessage = ""; // Clear success message after 3 seconds
      }, 3000);
    }
  }
}
</script>


<style scoped>
/* Layout */
.dashboard {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  padding: 20px;
}

/* Colored Boxes */
.box {
  width: 25%;
  padding: 20px;
  margin: 10px;
  border-radius: 10px;
  color: white;
}

/* Fund Transfer Input Styling */
.small-input {
  font-size: 14px;
  padding: 8px;
  width: 100%;
  margin: 5px 0;
}

.success-message {
  color: #28a745;
  font-weight: bold;
  margin-top: 10px;
}

/* Button Styling */
.nav-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  transition: background 0.3s ease;
  width: 100%;
  text-align: left;
}

.nav-button:hover {
  background-color: #0056b3;
}

/* Arrange Buttons in a Column */
.button-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Box Colors */
.grey { background-color: grey; }
.maroon { background-color: maroon; }
.blue { background-color: blue; }
.green { background-color: green; }
.orange { background-color: orange; color: black; }

/* About Us Section */
.about-us {
  width: 100%;
  background: black;
  color: white;
  text-align: center;
  padding: 15px;
  margin-top: 20px;
}

.about-us a {
  color: yellow;
  text-decoration: none;
  font-weight: bold;
}
</style>
