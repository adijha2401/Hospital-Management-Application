<template>
  <div>
    <h4>Upcoming Appointments</h4>

    <ul class="list-group">
      <li
        v-for="a in appts"
        :key="a.id"
        class="list-group-item d-flex justify-content-between"
      >
        <div>{{ a.start_dt }} — Patient {{ a.patient_id }}</div>

        <div>
          <button
            class="btn btn-sm btn-success me-1"
            @click="mark(a.id, 'Completed')"
          >
            Complete
          </button>

          <button
            class="btn btn-sm btn-danger"
            @click="mark(a.id, 'Cancelled')"
          >
            Cancel
          </button>
        </div>
      </li>
    </ul>
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
        const r = await api.get("/doctor/dashboard");
        appts.value = r.data.upcoming || [];
      } catch (e) {
        console.error("Error fetching appointments", e);
      }
    });

    async function mark(id, status) {
      try {
        await api.put(`/doctor/appointment/${id}/status`, { status });
        appts.value = appts.value.filter((a) => a.id !== id);
      } catch (e) {
        alert("Failed to update appointment");
      }
    }

    return { appts, mark };
  },
};
</script>
