<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <a class="navbar-brand" href="#">HMS</a>
      <button class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#nav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="nav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item"><router-link class="nav-link" to="/patient">Patient</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/doctor">Doctor</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/admin">Admin</router-link></li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item"><router-link class="nav-link" to="/login">Login</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/register">Register</router-link></li>
        </ul>
      </div>
    </div>
  </nav>
</template>