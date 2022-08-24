<script setup>
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useForm } from "vee-validate";
import * as Yup from "yup";

import { useAuthStore } from "@/stores";

const schema = Yup.object().shape({
  username: Yup.string().required("Username is required"),
  password: Yup.string().required("Password is required")
})

const { useFieldModel, handleSubmit, submitCount } = useForm({
  validationSchema: schema,
});

const [username, password] = useFieldModel(["username", "password"]);

const authStore = useAuthStore();
const { message } = storeToRefs(authStore);

const onSubmit = handleSubmit(async values => {
  const response = await authStore.login(username.value, password.value);
});

const isTooManyAttempts = computed(() => {
  return submitCount.value >= 10;
})
</script>

<template>
  <div class="login_wrapper">
    <div class="logo">
      <img src="./icons/logoidea2.png" alt="" />
    </div>
    <div class="container">
        <form @submit="onSubmit">
          <div class="form-group input-field">
            <i class="fa fa-user" aria-hidden="true"></i>
            <input name="username" v-model="username" type="text" class="form-control" />
          </div>
          <div class="form-group input-field">
            <i class="fa fa-lock" aria-hidden="true"></i>
            <input name="password" v-model="password" type="password" class="form-control" />
          </div>
          <div class="form-group">
            <button :disabled="isTooManyAttempts" type="submit" class="btn solid">Login</button>
          </div>
          <button class="btn solid">Login</button>
          <button class="btn clear" @click = "$router.push('signup')">Sign Up
          </button>
        </form>

        <!-- Hello Calvin/Lat
        I have moved error message to message.response, just to make it easier to access in Vue.
        All text messages are in the 'message' object, 'response' field
        -->
        <div v-if="message.error">{{ message.error }}</div>
      </div>
    </div>
</template>

<style>
@import "@/assets/login.css";
</style>
