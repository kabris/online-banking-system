<template>
  <div class="file-upload-container">
    <!-- ✅ Upload Documents Header (Only One) -->

    <!-- ✅ Drag & Drop Area (Inside Dotted Border) -->
    <div class="drag-drop-area" 
      @drop.prevent="handleDrop"
      @dragover.prevent="dragging = true"
      @dragleave.prevent="dragging = false"
      :class="{ 'dragging': dragging }"
    >
      <p v-if="!dragging">📁 Drag & Drop File Here</p>
      <p v-if="dragging">📁 Release to Upload</p>
    </div>

    <!-- ✅ Choose File Button (Outside Dotted Border) -->
    <button class="file-button" @click="triggerFileInput">Choose File</button>
    <input type="file" ref="fileInput" :accept="allowedTypes.join(',')" @change="handleFileUpload" class="hidden-file-input" />

    <!-- ✅ Display Selected File Name -->
    <p v-if="file" class="file-name">Selected File: {{ file.name }}</p>
    <p v-if="error" class="error-message">{{ error }}</p>
    <p v-if="uploadStatus" class="status-message">{{ uploadStatus }}</p>

    <!-- ✅ Submit Button -->
    <button @click="submitFile" class="submit-button" :disabled="!file || isUploading">
      {{ isUploading ? 'Uploading...' : 'Submit' }}
    </button>

    <!-- Run Script Button (only for admin and security) -->
    <button 
      v-if="(userType === 'admin' || userType === 'security') && canRunScript" 
      class="run-script-button"
      @click="runScript"
    >
      Run Script
    </button>

    <!-- Modal Overlay -->
    <div v-if="showReport" class="modal-overlay" @click="closeReport"></div>
    
    <!-- Report Modal -->
    <div v-if="showReport" class="malware-report-modal">
      <div class="malware-report-header">
        Malware Scan Report
      </div>
      
      <div class="malware-report-content">
        <div class="report-details">
          <div class="report-details-row">
            <span class="report-label">File Name:</span>
            <span class="report-value">{{ report.file_name }}</span>
          </div>
          
          <div class="report-details-row">
            <span class="report-label">File Type:</span>
            <span class="report-value">{{ report.file_type }}</span>
          </div>
          
          <div class="report-details-row">
            <span class="report-label">Scan Status:</span>
            <span class="report-value" :style="{ color: report.status === 'safe' ? '#27ae60' : '#e74c3c' }">
              {{ report.status }}
            </span>
          </div>
          
          <div class="report-details-row">
            <span class="report-label">Scan Date:</span>
            <span class="report-value">{{ report.created_at }}</span>
          </div>
          
          <div class="report-details-row">
            <span class="report-label">Scan Report:</span>
            <span class="report-value">{{ report.scan_report }}</span>
          </div>
        </div>
      </div>
      
      <button class="close-button" @click="closeReport">Close</button>
    </div>

    <!-- Add the MalwareReport component -->
    <MalwareReport ref="malwareReport" />
  </div>
</template>

<script>
import axios from "axios";
import MalwareReport from './MalwareReport.vue'

export default {
  name: 'FileUpload',
  components: {
    MalwareReport
  },
  props: {
    allowedTypes: {
      type: Array,
      default: () => ['application/pdf', 'image/png', 'image/jpeg']
    },
    userType: {
      type: String,
      required: true,
      validator: value => ['customer', 'admin', 'security'].includes(value)
    }
  },
  data() {
    return {
      file: null,
      dragging: false,
      error: null,
      uploadStatus: null,
      isUploading: false,
      canRunScript: false,
      mimeTypeMap: {
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc': 'application/msword',
        '.xls': 'application/vnd.ms-excel',
        '.jpeg': 'image/jpeg',
        '.jpg': 'image/jpeg',
        '.pdf': 'application/pdf',
        '.js': 'application/javascript',
        '.py': 'text/x-python'
      },
      showReport: false,
      report: {
        file_name: '',
        file_type: '',
        status: '',
        created_at: '',
        scan_report: ''
      },
      scanReports: [],
      selectedReport: null
    };
  },
  methods: {
    getFileExtension(filename) {
      return filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2);
    },
    
    isValidFileType(file) {
      const extension = '.' + this.getFileExtension(file.name).toLowerCase();
      const mimeType = file.type.toLowerCase();
      
      // Check if the file extension is in allowedTypes
      if (this.allowedTypes.some(type => type.toLowerCase() === extension)) {
        return true;
      }
      
      // Check if the MIME type is in allowedTypes
      if (this.allowedTypes.some(type => type.toLowerCase() === mimeType)) {
        return true;
      }
      
      // Check if the MIME type matches the extension's expected MIME type
      if (this.mimeTypeMap[extension] && this.mimeTypeMap[extension].toLowerCase() === mimeType) {
        return true;
      }
      
      return false;
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      if (!this.isValidFileType(file)) {
        this.error = `Invalid file type. Allowed types: ${this.allowedTypes.join(', ')}`;
        return;
      }
      
      this.file = file;
      this.error = null;
      this.canRunScript = false; // Reset run script permission when new file is selected
    },
    
    handleDrop(event) {
      event.preventDefault();
      this.dragging = false;
      const file = event.dataTransfer.files[0];
      
      if (file) {
        if (!this.isValidFileType(file)) {
          this.error = `Invalid file type. Allowed types: ${this.allowedTypes.join(', ')}`;
          return;
        }
        
        this.file = file;
        this.error = null;
        this.canRunScript = false; // Reset run script permission when new file is selected
      }
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    async submitFile() {
      if (!this.file) return;
      
      this.isUploading = true;
      this.error = null;
      this.uploadStatus = 'Uploading file...';
      
      const formData = new FormData();
      formData.append("file", this.file);
      formData.append("userType", this.userType);
      formData.append("user_email", "user@example.com");

      try {
        const response = await axios.post('http://localhost:5000/files/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        this.uploadStatus = `File uploaded successfully. Scan result: ${response.data.scan_result}`;
        
        // Emit the upload event with all necessary data
        this.$emit('file-uploaded', {
          filename: this.file.name,
          fileType: this.file.type,
          scanResult: response.data.scan_result,
          userType: this.userType,
          scanLogs: response.data.scan_report
        });
      } catch (error) {
        this.error = error.response?.data?.error || "Error uploading file";
      } finally {
        this.isUploading = false;
      }
    },

    async runScript() {
      if (!this.file || !this.canRunScript) return;

      try {
        const baseUrl = process.env.VUE_APP_API_URL || 'http://localhost:5000';
        const response = await axios.post(`${baseUrl}/files/run-script`, {
          filename: this.file.name,
          userType: this.userType
        }, {
          timeout: 30000 // 30 second timeout
        });

        this.$emit('script-executed', {
          success: true,
          message: response.data.message,
          logs: response.data.logs
        });
      } catch (error) {
        let errorMessage = "Error running script";
        if (error.code === 'ECONNABORTED') {
          errorMessage = "Script execution timeout. Please try again.";
        } else if (!navigator.onLine) {
          errorMessage = "No internet connection. Please check your network.";
        } else {
          errorMessage = error.response?.data?.error || "Error running script";
        }
        
        this.$emit('script-executed', {
          success: false,
          message: errorMessage
        });
      }
    },

    viewReport(file) {
      this.$refs.malwareReport.show({
        fileName: file.filename,
        fileType: file.fileType,
        status: file.status,
        scanDate: file.date,
        scanDetails: file.scanLogs
      });
    },

    closeReport() {
      this.showReport = false;
    },

    handleFileUploaded(uploadData) {
      this.scanReports.unshift({
        id: Date.now(),
        filename: uploadData.filename,
        status: uploadData.scanResult,
        date: new Date(),
        fileSize: uploadData.fileSize || 0,
        fileType: uploadData.fileType || 'Unknown',
        scanLogs: uploadData.scanLogs || 'Detailed scan analysis not available'
      });
    },
    
    showDetails(report) {
      // Fetch detailed scan logs if they're not already loaded
      if (!report.scanLogs) {
        // You can add an API call here to fetch detailed logs
        axios.get(`http://localhost:5000/api/scan-logs/${report.id}`)
          .then(response => {
            report.scanLogs = response.data.logs || 'No logs available';
            this.selectedReport = {...report};
          })
          .catch(error => {
            console.error('Error fetching scan logs:', error);
            report.scanLogs = 'Error loading scan logs';
            this.selectedReport = {...report};
          });
      } else {
        this.selectedReport = {...report};
      }
    }
  }
};
</script>

<style scoped>
/* ✅ File Upload Container */
.file-upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 20px;
  background-color: green;
  border-radius: 10px;
}

/* ✅ Upload Title */
.upload-title {
  color: white;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

/* ✅ Hidden File Input */
.hidden-file-input {
  display: none;
}

/* ✅ Drag & Drop Area (Inside Dotted Border) */
.drag-drop-area {
  width: 90%;
  padding: 20px;
  border: 2px dashed white;
  text-align: center;
  margin-bottom: 10px;
  border-radius: 10px;
  transition: background 0.3s ease-in-out;
}

/* ✅ Highlight when dragging */
.dragging {
  background-color: #cce5ff;
  border-color: #0056b3;
}

/* ✅ Choose File Button (Outside Dotted Border) */
.file-button {
  background: white;
  color: green;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  border: none;
  font-weight: bold;
  margin-bottom: 10px;
}

/* ✅ Submit Button */
.submit-button {
  background: blue;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  border: none;
}

/* ✅ Disabled Submit Button */
.submit-button:disabled {
  background: grey;
  cursor: not-allowed;
}

/* ✅ Display Selected File Name */
.file-name {
  margin-top: 10px;
  font-weight: bold;
  color: white;
}

.error-message {
  color: red;
  margin-top: 10px;
  font-weight: bold;
}

.status-message {
  color: white;
  margin-top: 10px;
  font-weight: bold;
}

.run-script-button {
  background: #e74c3c;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  border: none;
  font-weight: bold;
}

.run-script-button:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

/* ✅ Malware Report Modal */
.malware-report-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-width: 80%;
  max-height: 80vh;
  overflow-y: auto;
}

.malware-report-header {
  font-size: 1.2em;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 15px;
}

.malware-report-content {
  color: #333;
  background-color: white;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin: 10px 0;
}

.report-details {
  margin: 10px 0;
}

.report-details-row {
  display: flex;
  margin: 5px 0;
}

.report-label {
  font-weight: bold;
  width: 150px;
  color: #34495e;
}

.report-value {
  color: #2c3e50;
}

.close-button {
  background-color: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  float: right;
  margin-top: 10px;
}

.close-button:hover {
  background-color: #45a049;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 10px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  color: #333;  /* Ensure text is dark and visible */
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
  background: #45a049;
}

.safe {
  color: #2ecc71;
  font-weight: bold;
}

.malicious {
  color: #e74c3c;
  font-weight: bold;
}
</style>
