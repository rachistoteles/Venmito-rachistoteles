<template>
    <div>
      <h1>File Data</h1>
      <div v-if="data">
        <pre>{{ data }}</pre>
      </div>
      <div v-else>
        <p>Loading...</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  const data = ref(null);
  
  const fetchData = async (fileName, fileType) => {
    try {
      const response = await axios.get(`http://localhost:8000/process-file/${fileName}/${fileType}`);
      data.value = response.data.data;
    } catch (error) {
      console.error("Error fetching file:", error);
    }
  };
  
  onMounted(() => {
    fetchData('people.json', 'json');  // Example: Fetch the people.json file
  });
  </script>
  