<template>
  <div>
    <h4>Export Treatment Data</h4>
    <form @submit.prevent="startExport">
      <div class="mb-3"><label>Email (optional)</label><input v-model="email" class="form-control" type="email" /></div>
      <button class="btn btn-primary">Export CSV</button>
    </form>
    <div v-if="jobId" class="mt-3">Export started — job id: {{jobId}}</div>
  </div>
</template>

<script>
import api from "../../services/api";
export default {
  data(){ return { email: "", jobId: null } },
  methods: {
    async startExport(){
      const r = await api.post("/patient/export_csv", { email: this.email || null });
      this.jobId = r.data.job_id;
      alert("Export triggered");
    }
  }
};
</script>
