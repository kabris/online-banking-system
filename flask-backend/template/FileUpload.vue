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

    <!-- ✅ Submit Button -->
    <button @click="submitFile" class="submit-button" :disabled="!file">Submit</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      file: null,
      dragging: false,
      allowedTypes: ["application/pdf", "image/png", "image/jpeg"]  // Example allowed file types
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.file = file;
      const formData = new FormData();
      formData.append("file", file);
      // Process the formData (e.g., send it to the server)
    },
    
    handleDrop(event) {
      event.preventDefault();
      const file = event.dataTransfer.files[0];
      if (file) {
        this.file = file; // Set the dropped file to the data
        console.log("File dropped: ", file);
      }
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    submitFile() {
      this.uploadFile();
    },

    uploadFile() {
      let formData = new FormData();
      formData.append("file", this.file);

      axios.post("http://localhost:5000/upload", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        if (response.data.scan_result) {
          let scanResult = response.data.scan_result;
          if (scanResult === "Safe") {
            alert("The file is safe!");
          } else {
            alert("The file is malicious!");
          }
        }
      })
      .catch(error => {
        console.error("Error uploading file:", error);
        alert("Error uploading file");
      });
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
</style>
