<script setup>
import { reactive } from "vue";
import { useAuthStore } from "@/stores";

const login_info = reactive({
  username: "",
  password: "",
});

function handleSubmit(event) {
  const authStore = useAuthStore();

  return authStore
    .login(login_info.username, login_info.password)
    .catch((err) => {
      console.log(err);
    });
}
</script>

<template>
  <div class="login_wrapper">
    <div class="logo">
      <img src="./icons/logoidea2.png" alt="" />
    </div>
    <div class="container">
      <div class="login">
        <form @submit.prevent="handleSubmit">
          <div class="form-group input-field">
            <i class="fa fa-user" aria-hidden="true"></i>
            <input
              type="text"
              placeholder="Username"
              class="form-control"
              v-model="login_info.username"
            />
          </div>
          <div class="form-group input-field">
            <i class="fa fa-lock" aria-hidden="true"></i>
            <input
              type="password"
              placeholder="Password"
              class="form-control"
              v-model="login_info.password"
            />
          </div>
          <button class="btn solid">Login</button>
        </form>
      </div>
    </div>
  </div>
</template>

<style>
@import "@/assets/login.css";
</style>
