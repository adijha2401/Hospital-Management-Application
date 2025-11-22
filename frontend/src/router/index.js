import { createRouter, createWebHistory } from "vue-router";

import Login from "../components/auth/login.vue";
import Register from "../components/auth/register.vue";

import AdminDashboard from "../components/admin/admindashboard.vue";
import AdminAppointmentList from "../components/admin/appointmentlist.vue";

import DoctorDashboard from "../components/doctor/doctordashboard.vue";
import DoctorAppointments from "../components/doctor/doctorappointments.vue";
import PatientHistory from "../components/doctor/patienthistory.vue";

import PatientDashboard from "../components/patient/patientdashboard.vue";
import SearchDoctors from "../components/patient/searchdoctors.vue";
import BookAppointment from "../components/patient/bookappointment.vue";
import AppointmentHistory from "../components/patient/appointmenthistory.vue";
import ExportData from "../components/patient/exportdata.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/register", component: Register },

  { path: "/admin", component: AdminDashboard },
  { path: "/admin/appointments", component: AdminAppointmentList },

  { path: "/doctor", component: DoctorDashboard },
  { path: "/doctor/appointments", component: DoctorAppointments },
  { path: "/doctor/patient-history", component: PatientHistory },

  { path: "/patient", component: PatientDashboard },
  { path: "/patient/search", component: SearchDoctors },
  { path: "/patient/book/:doctorId", component: BookAppointment, props: true },
  { path: "/patient/history", component: AppointmentHistory },
  { path: "/patient/export", component: ExportData },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
