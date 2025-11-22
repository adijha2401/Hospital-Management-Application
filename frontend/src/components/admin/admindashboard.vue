<template>
  <div>
    <h2>Admin Dashboard</h2>

    <div class="row">
      <div class="col-md-4">
        <div class="card p-3">Doctors: {{ stats.doctors }}</div>
      </div>

      <div class="col-md-4">
        <div class="card p-3">Patients: {{ stats.patients }}</div>
      </div>

      <div class="col-md-4">
        <div class="card p-3">Appointments: {{ stats.appointments }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import api from "../../services/api";

export default {
  setup() {
    const stats = reactive({
      doctors: 0,
      patients: 0,
      appointments: 0,
    });

    onMounted(async () => {
      try {
        const r = await api.get("/admin/dashboard");
        Object.assign(stats, r.data);
      } catch (e) {
        console.error(e);
      }
    });

    return { stats };
  },
};
</script>
