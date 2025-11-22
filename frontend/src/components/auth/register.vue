<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <h3>Register as Patient</h3>

      <form @submit.prevent="onRegister">
        <div class="mb-3">
          <label>Username</label>
          <input v-model="username" class="form-control" required />
        </div>

        <div class="mb-3">
          <label>Email</label>
          <input v-model="email" class="form-control" type="email" required />
        </div>

        <div class="mb-3">
          <label>Password</label>
          <input v-model="password" class="form-control" type="password" required />
        </div>

        <div class="mb-3">
          <label>Contact</label>
          <input v-model="contact" class="form-control" />
        </div>

        <button class="btn btn-success w-100">Register</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import api from "../../services/api";
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();

    const username = ref("");
    const email = ref("");
    const password = ref("");
    const contact = ref("");

    async function onRegister() {
      try {
        await api.post("/auth/register", {
          username: username.value,
          email: email.value,
          password: password.value,
          contact: contact.value
        });

        alert("Registered — login now");
        router.push("/login");

      } catch (e) {
        alert("Registration failed");
      }
    }

    return { username, email, password, contact, onRegister };
  }
};
</script>
