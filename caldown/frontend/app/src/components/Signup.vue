<script setup>
import { Form, Field } from "vee-validate";
import * as Yup from "yup";

import { useUsersStore } from "@/stores";
import { router } from "@/helpers";

const schema = Yup.object().shape({
  username: Yup.string()
            .required("username is required"),
  password: Yup.string()
            .min(12, "Password must be at least 6 characters")
            .required("Password is required"),
  confirmPassword: Yup.string()
            .oneOf([Yup.ref("password"), null], "Password Must Match")
            .required("Confirm Password is required")
})

// Static Transition to Login Page
async function handleSubmit(values) {
  const usersStore = useUsersStore();
  const { username, password, confirmPassword } = values;
  await usersStore.signUp(username, password, confirmPassword).catch(error=>{
    console.log(error);
  });
};
</script>

<template>
  <div class="signup_wrapper">
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
          <div class="form-group input-field">
            <i class="fa fa-lock" aria-hidden="true"></i>
            <Field name="confirmPassword" type="password" class="form-control" :class="{ 'is-invalid': errors.confirmPassword }" />
            <div class="invalid-feedback">{{ errors.confirmPassword }}</div>
          </div>
          <div class="form-group">
            <button type="submit" class="btn solid">Sign Up</button>
            <button type="reset" class="btn btn-secondary">Reset</button>
          </div>
        </Form>
      </div>
    </div>
</template>

<style></style>
