<script setup lang="ts">
import { ref } from 'vue'
import { List, Star } from '@element-plus/icons-vue'
import { useExchangeStore } from './stores/exchange'

const activeIndex = ref('/')
const storeExchange = useExchangeStore()
storeExchange.load()
</script>

<template>
  <header>
    <el-menu
      :default-active="activeIndex"
      mode="horizontal"
      :router="true"
      :ellipsis="false"
    >
      <el-menu-item index="/about">Quadcask</el-menu-item>
      <el-menu-item index="/"><el-icon><List /></el-icon>Storage</el-menu-item>
      <el-menu-item index="/wishlist"><el-icon><Star /></el-icon>Wishlist</el-menu-item>
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
