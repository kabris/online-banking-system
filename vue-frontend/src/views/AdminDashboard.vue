<template>
  <div class="dashboard">
    <div class="content">
      <h2>Admin Dashboard</h2>

      <div class="grid-container">
        <!-- 🟦 User Management Box -->
        <section class="box user-management">
          <h3>Manage Users</h3>
          <div class="button-group">
            <button class="add-user" @click="goToAddUser">Add User</button>
            <button class="delete-user" @click="goToDeleteUser">Delete User</button>
          </div>
        </section>

        <!-- 🟧 System Logs Box -->
        <section class="box system-logs">
          <h3>System Logs & Activity Tracking</h3>
          <button @click="goToSystemLogs">View Logs</button>
        </section>

        <!-- 🟨 Transaction History Box -->
        <section class="box transaction-history">
          <h3>Transaction & Login History</h3>
          <ul>
            <li>User: Alice | Transaction: Sent $200 | Date: 2025-03-10</li>
            <li>User: Bob | Login Attempt: Successful | Date: 2025-03-10</li>
          </ul>
        </section>

        <!-- 🟩 Upload Executable Files (With "Run Update" Button) -->
        <section class="box file-upload">
          <h3>Upload System Updates (Executables)</h3>
          <FileUpload :allowedTypes="['.exe', '.dll']" />
          <button class="run-btn">Run Update</button>
        </section>
      </div>
    </div>
  </div>
</template>



---

<script>
import FileUpload from '@/components/FileUpload.vue';

export default {
  components: { FileUpload },
  methods: {
    goToAddUser() {
      this.$router.push("/add-user");
    },
    goToDeleteUser() {
      this.$router.push("/delete-user");
    },
    goToSystemLogs() {
      this.$router.push("/system-logs");
    }
  }
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


