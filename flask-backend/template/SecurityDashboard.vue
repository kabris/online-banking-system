<template>
  <div class="dashboard">
    <h2>IT Security Expert Dashboard - Malware Scan Reports</h2>
    
    <div class="filters">
      <input 
        v-model="searchQuery" 
        placeholder="Search by filename or email..."
        class="search-input"
      >
      <select v-model="statusFilter" class="status-filter">
        <option value="">All Status</option>
        <option value="safe">Safe</option>
        <option value="malicious">Malicious</option>
      </select>
      <select v-model="userTypeFilter" class="user-type-filter">
        <option value="">All Users</option>
        <option value="customer">Customer</option>
        <option value="admin">Admin</option>
        <option value="security">Security</option>
      </select>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Upload Date</th>
            <th>User Email</th>
            <th>User Type</th>
            <th>File Name</th>
            <th>File Type</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="report in filteredReports" :key="report.id">
            <td>{{ formatDate(report.created_at) }}</td>
            <td>{{ report.email }}</td>
            <td>{{ report.user_type }}</td>
            <td>{{ report.file_name }}</td>
            <td>{{ report.file_type }}</td>
            <td :class="getStatusClass(report.status)">{{ report.status }}</td>
            <td>
              <button @click="viewReport(report)" class="view-btn">
                View Details
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Report Modal -->
    <MalwareReport ref="malwareReport" @close="handleReportClose" />
  </div>
</template>

<script>
import MalwareReport from '@/components/MalwareReport.vue'

export default {
  name: 'SecurityDashboard',
  components: {
    MalwareReport
  },
  data() {
    return {
      malwareReports: [],
      searchQuery: '',
      statusFilter: '',
      userTypeFilter: '',
      loading: false,
      error: null
    }
  },
  computed: {
    filteredReports() {
      return this.malwareReports.filter(report => {
        const matchesSearch = !this.searchQuery || 
          report.file_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          report.email.toLowerCase().includes(this.searchQuery.toLowerCase());
        const matchesStatus = !this.statusFilter || 
          report.status.toLowerCase() === this.statusFilter.toLowerCase();
        const matchesUserType = !this.userTypeFilter || 
          report.user_type.toLowerCase() === this.userTypeFilter.toLowerCase();
        return matchesSearch && matchesStatus && matchesUserType;
      });
    }
  },
  methods: {
    async fetchMalwareReports() {
      this.loading = true;
      try {
        const response = await fetch("http://localhost:5000/api/file-uploads");
        if (!response.ok) throw new Error("Failed to fetch reports");
        
        const data = await response.json();
        if (data.files) {
          // Update reports and store in localStorage
          this.malwareReports = data.files;
          localStorage.setItem('malwareReports', JSON.stringify(data.files));
          console.log(`Fetched ${data.files.length} reports`); // Debug log
        }
      } catch (error) {
        console.error('Error fetching reports:', error);
        this.error = error.message;
        
        // Try to load from localStorage if fetch fails
        const savedReports = localStorage.getItem('malwareReports');
        if (savedReports) {
          this.malwareReports = JSON.parse(savedReports);
          console.log('Loaded reports from localStorage'); // Debug log
        }
      } finally {
        this.loading = false;
      }
    },
    formatDate(date) {
      if (!date) return '';
      return new Date(date).toLocaleString();
    },
    getStatusClass(status) {
      return {
        'status-safe': status.toLowerCase() === 'safe',
        'status-malicious': status.toLowerCase() === 'malicious'
      };
    },
    viewReport(report) {
      this.$refs.malwareReport.show({
        fileName: report.file_name,
        fileType: report.file_type,
        status: report.status,
        scanDate: report.created_at,
        scanDetails: report.scan_report || 'No detailed scan report available'
      });
    },
    handleReportClose() {
      // Nothing to do here as the modal handles its own state
    },
    loadSavedData() {
      const savedReports = localStorage.getItem('malwareReports');
      if (savedReports) {
        this.malwareReports = JSON.parse(savedReports);
        console.log('Loaded saved reports from localStorage'); // Debug log
      }
    }
  },
  created() {
    // Load saved data first
    this.loadSavedData();
    
    // Fetch fresh data
    this.fetchMalwareReports();
    
    // Set up polling for new data every 10 seconds
    this.pollInterval = setInterval(() => {
      this.fetchMalwareReports();
    }, 10000);
  },
  beforeDestroy() {
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input, .status-filter, .user-type-filter {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-input {
  flex-grow: 1;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f8f9fa;
  font-weight: bold;
  color: #2c3e50;
}

.status-safe {
  color: #2ecc71;
  font-weight: bold;
}

.status-malicious {
  color: #e74c3c;
  font-weight: bold;
}

.view-btn {
  padding: 6px 12px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.view-btn:hover {
  background-color: #2980b9;
}
</style>
