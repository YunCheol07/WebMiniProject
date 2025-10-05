<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useAuth } from './stores/auth'

const { fetchUser, isAuthenticated } = useAuth()

onMounted(async () => {
  if (isAuthenticated.value) {
    await fetchUser()
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #121212;
  color: white;
}

#app {
  min-height: 100vh;
}
</style>


<!-- npm run dev -->