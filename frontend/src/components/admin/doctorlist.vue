<template>
  <div>
    <h4>Doctors</h4>

    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Spec</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="d in doctors" :key="d.id">
          <td>{{ d.id }}</td>
          <td>{{ d.username }}</td>
          <td>{{ d.specialization }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import api from "../../services/api";

export default {
  setup() {
    const doctors = ref([]);

    onMounted(async () => {
      try {
        const r = await api.get("/admin/search?type=doctor&q=");
        doctors.value = r.data.doctors || [];
      } catch (e) {
        console.error(e);
      }
    });

    return { doctors };
  },
};
</script>
