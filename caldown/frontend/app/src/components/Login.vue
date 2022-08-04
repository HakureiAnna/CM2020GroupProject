<script setup>
import { ref, computed } from "vue";
import { useForm } from "vee-validate";
import * as Yup from "yup";

import { useAuthStore } from "@/stores";

const schema = Yup.object().shape({
  username: Yup.string().required("Username is required"),
  password: Yup.string().required("Password is required")
})

const { meta, errors, useFieldModel, handleSubmit, isSubmitting, submitCount } = useForm({
  validationSchema: schema,
});

const [username, password] = useFieldModel(["username", "password"]);

const onSubmit = handleSubmit(async values => {
  const authStore = useAuthStore();
  const response = await authStore.login(username.value, password.value);

  // Dear Calvin / Latifa
  // the variable "response" has the responses from the bad end, can you make a display message that notify users about this, Thank you.
  console.log(response);
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
        </form>
      </div>
    </div>
</template>

<style>
@import "@/assets/login.css";
</style>
