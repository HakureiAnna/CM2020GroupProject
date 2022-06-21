<script setup>
import { reactive } from "vue";
import { useAuthStore } from "@/stores";

// A proxy object
const signup_info = reactive({
  username: "",
  password: "",
  password_confirm: "",
});

// Static Transition to Login Page
const handleSubmit = () => {
  const authStore = useAuthStore();

  return authStore
    .signup(
      signup_info.username,
      signup_info.password,
      signup_info.password_confirm
    )
    .catch((err) => {
      console.log(err);
    });
};
</script>

<template>
  <div class="signup_wrapper">
    <div class="logo">
      <img src="./icons/logoidea2.png" alt="" />
    </div>
    <div class="container">
      <div class="signup">
        <form @submit.prevent="handleSubmit">
          <div class="form-group input-field">
            <i class="fa fa-user" aria-hidden="true"></i>
            <input
              type="text"
              placeholder="Username"
              class="form-control"
              v-model="signup_info.username"
            />
          </div>
          <div class="form-group input-field">
            <i class="fa fa-lock" aria-hidden="true"></i>
            <input
              type="password"
              placeholder="Password"
              class="form-control"
              v-model="signup_info.password"
            />
          </div>
          <div class="form-group input-field">
            <i class="fa fa-lock" aria-hidden="true"></i>
            <input
              type="password"
              placeholder="Confirm Password"
              class="form-control"
              v-model="signup_info.password_confirm"
            />
          </div>
          <button class="btn solid">Sign Up</button>
        </form>
      </div>
    </div>
  </div>
</template>

<style></style>
