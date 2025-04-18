<template>
  <h2>📜 Login History</h2>
  <table>
    <thead>
      <tr>  
        <th>Date</th>  
        <th>Time</th>  
      </tr>
    </thead>
    <tbody>
      <tr v-for="entry in loginHistory" :key="entry.id">  
        <td>{{ entry.date }}</td>  
        <td>{{ entry.time }}</td>  
      </tr>
    </tbody>
  </table>
</template>



<script>
export default {
  data() {
    return {
      loginHistory: [
        { date: "March 10, 2025", time: "10:00 AM" },
        { date: "March 9, 2025", time: "5:45 PM" },
        { date: "March 7, 2025", time: "2:15 PM" },
      ],
    };
  },
};
</script>

<style>
/* ✅ Darker text for headers and table content */
h2 {
  color: #222;  /* Darker heading */
  font-weight: bold;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #f9f9f9; /* Light gray background */
}

/* ✅ Darker table borders */
th, td {
  padding: 10px;
  border: 2px solid #333; /* Darker border */
  color: #111; /* Darker text */
}

/* ✅ Bold column headers */
th {
  background-color: #444; /* Darker background */
  color: #fff; /* White text */
}
</style>
