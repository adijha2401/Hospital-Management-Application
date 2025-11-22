<template>
  <div>
    <h4>All Appointments</h4>

    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Doctor</th>
          <th>Patient</th>
          <th>Start</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="a in appts" :key="a.id">
          <td>{{ a.id }}</td>
          <td>{{ a.doctor_id }}</td>
          <td>{{ a.patient_id }}</td>
          <td>{{ a.start_dt }}</td>
          <td>{{ a.status }}</td>
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
    const appts = ref([]);

    onMounted(async () => {
      try {
        const r = await api.get("/admin/appointments");
        appts.value = r.data.appointments || [];
      } catch (e) {
        console.error(e);
      }
    });

    return { appts };
  },
};
</script>
