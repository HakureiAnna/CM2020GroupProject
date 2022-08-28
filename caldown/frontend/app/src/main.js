import { createApp } from "vue";
import { createPinia } from "pinia";

import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

import App from "./App.vue";
import { router } from "./helpers";
import "./axios";

const app = createApp(App);
const pinia = createPinia();

app.component('Datepicker', Datepicker);

app.use(pinia);
app.use(router);
app.mount("#app");
