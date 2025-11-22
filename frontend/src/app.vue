<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <router-view />
    </div>
  </div>
</template>

<script>
import Navbar from "./components/common/navbar.vue";
export default { components: { Navbar } };
</script>
