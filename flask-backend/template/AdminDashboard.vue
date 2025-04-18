<template>
  <div>
    <h2>Admin Dashboard</h2>
    <button @click="navigateToAddUser">Add User</button>
    <button @click="deleteUser">Delete User</button>
    <ul>
      <li v-for="(log, index) in logs" :key="index">
        {{ log }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      logs: [],
    };
  },
  methods: {
    navigateToAddUser() {
      this.$router.push("/add-user");
    },
    async fetchLogs() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/logs");
        if (!response.ok) throw new Error("Failed to fetch logs");

        this.logs = await response.json();
      } catch (error) {
        console.error(error.message);
      }
    },
  },
  created() {
    this.fetchLogs();
  },
};
</script>

<style scoped>
/* 🎨 General Layout */
.dashboard {
  display: flex;
  justify-content: center;
  padding: 20px;
}
.content {
  width: 100%;
  text-align: center;
}

/* 📦 Grid Layout for Even Distribution */
.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* Two columns */
  gap: 20px;
  justify-content: center;
  padding: 20px;
}

/* 📦 Box Style for Each Section */
.box {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* 🎨 Individual Box Colors */
.user-management { background: #3498db; color: white; }
.system-logs { background: #f39c12; color: white; }
.transaction-history { background: #f1c40f; color: black; }
.file-upload { background: #2ecc71; color: white; }

/* 🖱️ Button Styling */
button {
  background: white;
  color: black;
  padding: 10px 15px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 10px;
  transition: background 0.3s ease;
}

button:hover {
  background: lightgray;
}

/* 🏷️ Titles */
h2, h3 {
  color: #2c3e50;
}

/* 🟢 Run Update Button Inside Upload Box */
.file-upload .run-btn {
  background: #e74c3c;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  width: 100%;
  margin-top: 10px;
}

.file-upload .run-btn:hover {
  background: #c0392b;
}

/* 🟦 Space Between "Add User" & "Delete User" Buttons */
.button-group {
  display: flex;
  justify-content: center;
  gap: 20px; /* ✅ Added space between buttons */
  margin-top: 10px;
}

.add-user, .delete-user {
  background: #007bff;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background 0.3s ease;
}

.add-user:hover, .delete-user:hover {
  background: #0056b3;
}
</style>


