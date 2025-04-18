<template>
  <div class="dashboard">
    <div class="content">
      <h2>Upload Security Scripts</h2>

      <!-- Upload Security Scripts -->
      <section class="file-upload">
        <FileUpload 
          :allowedTypes="['.js', '.py']" 
          :userType="'security'"
          @file-uploaded="handleFileUploaded"
        />
      </section>

      <!-- Run Security Script -->
      <section class="run-script" v-if="canRunScript">
        <button class="run-btn" @click="runSecurityScript">
          Run Script
        </button>
      </section>

      <!-- Malware Scan Reports Table -->
      <section class="scan-reports">
        <h3>Malware Scan Reports</h3>
        <div class="filters">
          <select v-model="filterStatus" class="status-filter">
            <option value="">All Status</option>
            <option value="safe">Safe</option>
            <option value="malicious">Malicious</option>
          </select>
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search by filename..."
            class="search-input"
          >
        </div>
        <table>
          <thead>
            <tr>
              <th>Filename</th>
              <th>File Type</th>
              <th>Size (Bytes)</th>
              <th>Date</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="report in filteredReports" :key="report.id">
              <td>{{ report.filename }}</td>
              <td>{{ report.fileType }}</td>
              <td>{{ report.fileSize }}</td>
              <td>{{ formatDate(report.date) }}</td>
              <td :class="report.status.toLowerCase()">{{ report.status }}</td>
              <td>
                <button 
                  class="view-btn" 
                  @click="viewReport(report)"
                >
                  View
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Scan Details Modal -->
      <div v-if="selectedReport" class="modal">
        <div class="modal-content">
          <h3>Scan Details</h3>
          <div class="details">
            <p><strong>Filename:</strong> {{ selectedReport.filename }}</p>
            <p><strong>Status:</strong> <span :class="selectedReport.status.toLowerCase()">{{ selectedReport.status }}</span></p>
            <p><strong>Scan Date:</strong> {{ formatDate(selectedReport.date) }}</p>
            <p><strong>File Size:</strong> {{ formatFileSize(selectedReport.fileSize) }}</p>
            <div class="scan-logs">
              <h4>Scan Logs:</h4>
              <div class="logs-content">
                {{ selectedReport.scanLogs || 'No logs available' }}
              </div>
            </div>
          </div>
          <button class="close-btn" @click="selectedReport = null">Close</button>
        </div>
      </div>

      <!-- Logs Modal -->
      <div v-if="showLogsModal" class="logs-modal">
        <div class="logs-modal-content">
          <h3>Scan Report Details</h3>
          <div class="logs-content">
            <div v-if="currentFileDetails">
              <div class="report-detail-item">
                <strong>File Name:</strong> {{ currentFileDetails.file_name }}
              </div>
              <div class="report-detail-item">
                <strong>File Type:</strong> {{ currentFileDetails.file_type }}
              </div>
              <div class="report-detail-item">
                <strong>Upload Date:</strong> {{ currentFileDetails.created_at }}
              </div>
              <div class="report-detail-item">
                <strong>Status:</strong> 
                <span :class="{'status-safe': currentFileDetails.status === 'safe', 
                             'status-malicious': currentFileDetails.status === 'malicious'}">
                  {{ currentFileDetails.status }}
                </span>
              </div>
              <div class="report-detail-item">
                <strong>Scan Report:</strong>
                <pre class="scan-report">{{ currentFileDetails.scan_report || 'No detailed scan report available' }}</pre>
              </div>
            </div>
            <div v-else>
              <p>No logs available</p>
            </div>
          </div>
          <button @click="closeLogsModal" class="close-button">Close</button>
        </div>
      </div>

      <!-- Malware Report Modal -->
      <MalwareReport ref="malwareReport" @close="handleReportClose" />
    </div>
  </div>
</template>

<script>
import FileUpload from '@/components/FileUpload.vue';
import axios from 'axios';
import MalwareReport from '@/components/MalwareReport.vue';

export default {
  name: 'SecurityDashboard',
  components: {
    FileUpload,
    MalwareReport
  },
  data() {
    return {
      canRunScript: false,
      filterStatus: '',
      searchQuery: '',
      selectedReport: null,
      scanReports: [],
      showLogsModal: false,
      currentFileDetails: null
    };
  },
  computed: {
    filteredReports() {
      return this.scanReports.filter(report => {
        const matchesStatus = !this.filterStatus || report.status.toLowerCase() === this.filterStatus.toLowerCase();
        const matchesSearch = !this.searchQuery || report.filename.toLowerCase().includes(this.searchQuery.toLowerCase());
        return matchesStatus && matchesSearch;
      });
    }
  },
  methods: {
    handleFileUploaded(uploadData) {
      this.scanReports.unshift({
        id: Date.now(),
        filename: uploadData.filename,
        fileType: uploadData.fileType || this.getFileType(uploadData.filename),
        fileSize: uploadData.fileSize || 0,
        date: new Date(),
        status: uploadData.scanResult,
        scanLogs: uploadData.scanLogs || 'No scan logs available'
      });
      
      if (uploadData.scanResult.toLowerCase() === 'safe') {
        this.canRunScript = true;
      }
    },
    getFileType(filename) {
      const extension = filename.split('.').pop().toLowerCase();
      const mimeTypes = {
        'js': 'text/javascript',
        'py': 'text/x-python',
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      };
      return mimeTypes[extension] || 'Unknown';
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
    viewReport(report) {
      this.$refs.malwareReport.show({
        fileName: report.filename,
        fileType: report.fileType,
        status: report.status,
        scanDate: report.date,
        scanDetails: report.scanLogs
      });
    },
    runSecurityScript() {
      // Implement script running logic here
      console.log('Running security script...');
    },
    async viewReportDetails(fileId) {
      try {
        const response = await fetch(`/api/file-report/${fileId}`);
        const data = await response.json();
        
        if (data.success) {
          this.currentFileDetails = data.report;
          this.showLogsModal = true;
        } else {
          console.error('Failed to fetch report:', data.error);
        }
      } catch (error) {
        console.error('Error fetching report:', error);
      }
    },
    closeLogsModal() {
      this.showLogsModal = false;
      this.currentFileDetails = null;
    },
    handleReportClose() {
      this.selectedReport = null;
    }
  },
  mounted() {
    // Fetch existing scan reports from the backend
    axios.get('http://localhost:5000/scan/reports')
      .then(response => {
        this.scanReports = response.data.map(report => ({
          ...report,
          date: new Date(report.date)
        }));
      })
      .catch(error => {
        console.error('Error fetching scan reports:', error);
      });
  }
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.content {
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  color: #333;
  margin-bottom: 20px;
}

.file-upload {
  margin-bottom: 20px;
}

.scan-reports {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.status-filter {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 120px;
}

.search-input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex-grow: 1;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
  font-weight: bold;
  color: #333;
}

.safe {
  color: #2ecc71;
  font-weight: bold;
}

.malicious {
  color: #e74c3c;
  font-weight: bold;
}

.view-btn {
  padding: 6px 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.view-btn:hover {
  background-color: #45a049;
}

.run-btn {
  width: 100%;
  padding: 12px;
  background-color: #2980b9;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  margin-bottom: 20px;
}

.run-btn:hover {
  background-color: #2573a7;
}

.run-script {
  margin-bottom: 20px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 10px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  color: #333;
}

.scan-logs {
  margin-top: 20px;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.logs-content {
  color: #333;
  font-family: monospace;
  white-space: pre-wrap;
  word-wrap: break-word;
  background: white;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #eee;
  margin-top: 10px;
  min-height: 100px;
  max-height: 300px;
  overflow-y: auto;
}

.details p {
  margin: 10px 0;
  color: #333;
}

.details strong {
  color: #2c3e50;
  margin-right: 10px;
}

h3, h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.close-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.close-btn:hover {
  background-color: #45a049;
}

.logs-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.logs-modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.report-detail-item {
  margin: 10px 0;
  line-height: 1.5;
}

.report-detail-item strong {
  color: #2c3e50;
  margin-right: 10px;
  min-width: 100px;
  display: inline-block;
}

.scan-report {
  background-color: #f1f1f1;
  padding: 10px;
  border-radius: 4px;
  white-space: pre-wrap;
  margin-top: 5px;
}

.status-safe {
  color: #27ae60;
  font-weight: bold;
}

.status-malicious {
  color: #e74c3c;
  font-weight: bold;
}

.close-button {
  background-color: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 15px;
  float: right;
}

.close-button:hover {
  background-color: #45a049;
}
</style>
