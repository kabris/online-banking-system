<template>
  <div :class="{ 'dark-mode': isDarkMode }">
    <AppNavbar @toggle-theme="toggleTheme" />
    <div class="container">
     
      
      <main>
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import AppNavbar from "@/components/AppNavbar.vue";


export default {
  components: { AppNavbar },
  data() {
    return {
      isDarkMode: false
    };
  },
  computed: {
   
  },
  methods: {
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
    }
  }
};
</script>
