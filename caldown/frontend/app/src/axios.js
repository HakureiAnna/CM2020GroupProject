import axios from "axios";

// axios.defaults.baseURL = <endpoint />

// remove unwanted double quotation marks
axios.defaults.headers.common["Authorization"] = localStorage.getItem("user") ? `Bearer ${localStorage.getItem("user").replace(/["]/g, '')}` : '';
