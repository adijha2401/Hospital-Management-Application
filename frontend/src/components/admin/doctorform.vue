<template>
  <div>
    <h4>Add Doctor</h4>

    <form @submit.prevent="onAdd">
      <input v-model="username" placeholder="Username" class="form-control mb-2" />
      <input v-model="email" placeholder="Email" class="form-control mb-2" />
      <input v-model="specialization" placeholder="Specialization" class="form-control mb-2" />

      <button class="btn btn-primary">Add</button>
    </form>
  </div>
</template>

<script>
import { ref } from "vue";
import api from "../../services/api";

export default {
  setup() {
    const username = ref("");
    const email = ref("");
    const specialization = ref("");

    const onAdd = async () => {
      try {
        await api.post("/admin/doctor", {
          username: username.value,
          email: email.value,
          specialization: specialization.value,
        });

        alert("Doctor Added");
      } catch (e) {
        alert("Failed");
      }
    };

    return { username, email, specialization, onAdd };
  },
};
</script>
