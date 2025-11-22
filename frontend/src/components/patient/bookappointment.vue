<template>
  <div>
    <h4>Book Appointment</h4>
    <div v-if="!doctor">Loading...</div>
    <div v-else>
      <p><strong>{{doctor.username}}</strong> — {{doctor.specialization}}</p>
      <form @submit.prevent="book">
        <div class="mb-3"><label>Start (ISO)</label><input v-model="start" class="form-control" placeholder="2025-12-12T09:00:00" required></div>
        <div class="mb-3"><label>End (ISO)</label><input v-model="end" class="form-control" placeholder="2025-12-12T09:30:00" required></div>
        <button class="btn btn-success">Book</button>
      </form>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";
export default {
  props: ["doctorId"],
  data() { return { doctor: null, start: "", end: "" } },
  async mounted() {
    const r = await api.get(`/patient/doctors`); // small fetch; in real app fetch single doctor endpoint
    this.doctor = r.data.doctors.find(d=>d.id==this.$route.params.doctorId) || {};
  },
  methods: {
    async book() {
      try {
        await api.post("/patient/appointment", { doctor_id: Number(this.$route.params.doctorId), start_dt: this.start, end_dt: this.end });
        alert("Booked");
        this.$router.push("/patient/history");
      } catch (e) { alert("Failed to book: " + (e.response?.data?.error || e.message)); }
    }
  }
};
</script>
