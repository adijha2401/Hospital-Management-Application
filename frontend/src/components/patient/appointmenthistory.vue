<template>
  <div>
    <h4>My Appointments</h4>
    <ul class="list-group">
      <li v-for="a in appts" :key="a.id" class="list-group-item">
        {{a.start_dt}} — Dr {{a.doctor_id}} — {{a.status}}
        <button v-if="a.status==='Booked'" class="btn btn-sm btn-danger float-end" @click="cancel(a.id)">Cancel</button>
      </li>
    </ul>
  </div>
</template>

<script>
import api from "../../services/api";
export default {
  data(){ return { appts: [] } },
  async mounted(){ const r = await api.get("/patient/history"); this.appts = r.data.appointments || []; },
  methods: {
    async cancel(id){ await api.delete(`/patient/appointment/${id}`); this.appts = this.appts.filter(x=>x.id!==id); }
  }
};
</script>
