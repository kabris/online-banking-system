<template>
  <div class="notifications">
    <h2>📢 Notifications</h2>
    <ul>
      <li v-for="(notification, index) in notifications" :key="index">
        {{ notification }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      notifications: [
        "You received Kshs.5,000 from XYZ",
        "Payment of Kshs.2,000 sent to ABC Corp",
        "Fund transfer of Kshs.10,000 was successful",
      ],
    };
  },
};
</script>

<style>
.notifications {
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #222;  /* Darker heading */
  font-size: 1.5rem;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  background-color: #f3f3f3;  /* Light gray background */
  color: #333;  /* Dark text */
  padding: 10px 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  font-weight: bold;
}
</style>
