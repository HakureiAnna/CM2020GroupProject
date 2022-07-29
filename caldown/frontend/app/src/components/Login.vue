<script setup>
import { Form, Field } from "vee-validate";
import * as Yup from "yup";

import { useAuthStore } from "@/stores";

const schema = Yup.object().shape({
  username: Yup.string().required("Username is required"),
  password: Yup.string().required("Password is required")
})

async function handleSubmit(values) {
  const authStore = useAuthStore();
  const { username, password } = values;
  await authStore.login(username, password);
}
</script>

<template>
  <div class="login_wrapper">
    <div class="logo">
      <img src="./icons/logoidea2.png" alt="" />
    </div>
    <div class="container">
        <Form @submit="handleSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }">
          <div class="form-group input-field">
            <i class="fa fa-user" aria-hidden="true"></i>
            <Field name="username" type="text" class="form-control" :class="{ 'is-invalid': errors.username }" />
            <div class="invalid-feedback">{{ errors.username }}</div>
          </div>
          <div class="form-group input-field">
            <i class="fa fa-lock" aria-hidden="true"></i>
            <Field name="password" type="password" class="form-control" :class="{ 'is-invalid': errors.password }" />
            <div class="invalid-feedback">{{ errors.password }}</div>
          </div>
          <div class="form-group">
            <button type="submit" class="btn solid">Login</button>
            <button type="reset" class="btn btn-secondary">Reset</button>
          </div>
        </Form>
      </div>
    </div>
</template>

<style>
@import "@/assets/login.css";
</style>
