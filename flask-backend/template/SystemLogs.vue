<template>
  <div class="logs">
    <h2>System Logs</h2>
    <table>
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>Action</th>
          <th>Performed By</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in logs" :key="log.id">
          <td>{{ log.timestamp }}</td>
          <td>{{ log.action }}</td>
          <td>{{ log.performedBy }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      logs: [
        { id: 1, timestamp: "2025-03-13 12:05:23", action: "User Login", performedBy: "customer01@gmail.com" },
        { id: 2, timestamp: "2025-03-13 12:10:45", action: "Funds Transfer", performedBy: "customer02@gmail.com" },
        { id: 3, timestamp: "2025-03-13 12:15:30", action: "File Upload", performedBy: "itsec001@gmail.com" },
        { id: 4, timestamp: "2025-03-13 12:20:12", action: "User Deleted", performedBy: "sysadmin01@gmail.com" },
        { id: 5, timestamp: "2025-03-13 12:25:00", action: "Security Alert Reviewed", performedBy: "itsec002@gmail.com" }
      ]
    };
  },
  async created() {
    try {
      const response = await fetch("http://localhost:5000/api/system-logs");
      if (!response.ok) throw new Error("Failed to fetch logs");
      this.logs = await response.json();
    } catch (error) {
      console.error("Error fetching system logs:", error);
    }
  }
};
</script>

<style scoped>
.logs {
  text-align: center;
  padding: 20px;
}

h2 {
  font-size: 22px;
  color: #fff; /* White text for visibility */
  background: #007bff;
  padding: 10px;
  border-radius: 5px;
  display: inline-block;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 10px;
  border: 1px solid #444;
  text-align: center;
}

th {
  background: #222;
  color: white;
  font-weight: bold;
}

td {
  background: rgba(255, 255, 255, 0.9);
  color: #000;
}
</style>
