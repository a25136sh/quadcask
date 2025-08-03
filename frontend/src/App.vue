<script setup lang="ts">
import { ref } from 'vue'
import router from './router/index.ts'

const activeIndex = ref('/')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key)
  router.push({ path: key })
}

const message = ref<string>("Push the button!");
</script>

<template>
  <header>
    <el-menu
      :default-active="activeIndex"
      mode="horizontal"
      :ellipsis="false"
      @select="handleSelect"
    >
      <el-menu-item>Quadcask</el-menu-item>
      <el-menu-item index="/">Storage</el-menu-item>
      <el-menu-item index="/wishlist">Wishlist</el-menu-item>
    </el-menu>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  width: 100%;
}
.el-menu--horizontal > .el-menu-item:nth-child(1) {
  margin-right: auto;
}
</style>
