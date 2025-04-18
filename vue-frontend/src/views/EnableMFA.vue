<template>
  <div class="mfa-container">
    <h2>🔐 Enable Multi-Factor Authentication (MFA)</h2>
    <p>Enter a 4-digit PIN to enable MFA for additional security.</p>
    <input type="password" v-model="mfaPin" maxlength="4" placeholder="Enter 4-digit PIN" />
    <button @click="enableMFA">Enable MFA</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      mfaPin: "",
    };
  },
  methods: {
    enableMFA() {
      if (this.mfaPin.length !== 4 || isNaN(this.mfaPin)) {
        alert("PIN must be exactly 4 digits.");
        return;
      }
      alert("MFA Enabled Successfully!");
    },
  },
};
</script>

<style>
.mfa-container {
  text-align: center;
  padding: 20px;
  font-family: Arial, sans-serif;
}

/* 🌑 Darker Text */
.mfa-container h2, 
.mfa-container p, 
.mfa-container input, 
.mfa-container button {
  color: #111;  /* Darker Text Color */
}

/* 🔳 Darker Input Text */
input {
  width: 120px;
  padding: 10px;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  color: #111; /* Dark Text */
  border: 2px solid #333; /* Darker Border */
}

/* 🔲 Darker Button */
button {
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  color: white; /* White Text */
  background-color: #333; /* Dark Button */
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #111; /* Even Darker on Hover */
}
</style>
