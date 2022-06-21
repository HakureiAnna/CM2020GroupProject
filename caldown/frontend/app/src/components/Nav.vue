<script setup>
import { RouterLink } from "vue-router";
import { useAuthStore } from "@/stores";

const authStore = useAuthStore();
</script>

<template>
  <nav class="navbar navbar-expand-md bg-dark navbar-dark">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/">Home</RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <RouterLink to="/login">Login</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/signup">Sign Up</RouterLink>
          </li>
          <li class="nav-item">
            <a @click="authStore.logout()" class="">Logout</a>
          </li>
          <li class="nav-item">
            <RouterLink to="/questions">Questions</RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style>
a,
.green {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
}

@media (hover: hover) {
  a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
  }
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}
</style>
