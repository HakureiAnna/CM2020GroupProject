import axios from "axios";

// axios.defaults.baseURL = <endpoint />

axios.defaults.headers.common["Authorization"] = localStorage.getItem("user");
