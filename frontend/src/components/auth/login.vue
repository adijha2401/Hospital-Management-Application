<template>
  <div class="row justify-content-center">
    <div class="col-md-5">
      <h3>Login</h3>
      <form @submit.prevent="onSubmit">
        <div class="mb-3">
          <label class="form-label">Username or Email</label>
          <input v-model="identifier" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" v-model="password" class="form-control" required />
        </div>

        <button class="btn btn-primary w-100">Login</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useAuthStore } from "../../store";
import { useRouter } from "vue-router";

export default {
  setup() {
    const auth = useAuthStore();
    const router = useRouter();

    const identifier = ref("");
    const password = ref("");

    async function onSubmit() {
      try {
        await auth.login(identifier.value, password.value);

        const role = auth.user?.role;

        if (role === "admin") router.push("/admin");
        else if (role === "doctor") router.push("/doctor");
        else router.push("/patient");
      } catch (error) {
        alert("Login failed");
      }
    }

    return { identifier, password, onSubmit };
  }
};
</script>
