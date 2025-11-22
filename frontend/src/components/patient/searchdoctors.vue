<template>
  <div>
    <h4>Search Doctors</h4>
    <div class="mb-3 input-group">
      <input v-model="q" class="form-control" placeholder="specialization" />
      <button class="btn btn-primary" @click="search">Search</button>
    </div>
    <div v-if="doctors.length===0">No doctors found</div>
    <div v-else class="list-group">
      <a v-for="d in doctors" :key="d.id" class="list-group-item list-group-item-action" :href="`/patient/book/${d.id}`">
        <strong>{{d.username}}</strong> — {{d.specialization}}
      </a>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";
export default {
  data(){ return { q: "", doctors: [] } },
  methods: {
    async search() {
      const r = await api.get("/patient/doctors", { specialization: this.q });
      this.doctors = r.data.doctors || [];
    }
  }
};
</script>
