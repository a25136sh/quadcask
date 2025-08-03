<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import axios from 'axios'

const endpoint = import.meta.env.VITE_API_ENDPOINT as string;

const message = ref<string>("Push the button!");

const handleClick = () => {
  const config = {
    method: "get",
    url: endpoint + "/hello",
  };
  
  // Python側に処理をリクエストする
  axios(config)
    .then((response) => {
      console.log(response);
      response.data.message && (message.value = response.data.message);
    })
    .catch((error) => {
      console.log(error);
    });
};
</script>

<template>
  <header>
    Quadcask
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
    <button type="button" @click="handleClick">{{ message }}</button>

    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
</style>
