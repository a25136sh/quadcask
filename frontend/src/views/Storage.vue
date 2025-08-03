<script setup lang="ts">
import axios from 'axios'

const endpoint: string = import.meta.env.VITE_API_ENDPOINT;

const handleClick = () => {
  axios.get(`${endpoint}/hello`)
    .then((response) => {
      console.log(response.data.message);
    })
    .catch((error) => {
      console.log(error);
    });
};
</script>

<template>
  <main>
    aaaa
  </main>
</template>
