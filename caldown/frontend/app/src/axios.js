import axios from "axios";

// axios.defaults.baseURL = <endpoint />

// remove unwanted double quotation marks
const token = localStorage.getItem("user").replace(/["]/g, '');
axios.defaults.headers.common["Authorization"] = token ? `Bearer ${token}` : '';
