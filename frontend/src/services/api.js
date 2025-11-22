import axios from "axios";

const base = (import.meta.env.VITE_API_BASE) || "/api";

const instance = axios.create({
  baseURL: base,
  withCredentials: true,
  headers: { "Content-Type": "application/json" }
});

// simple interceptor
instance.interceptors.response.use(
  resp => resp,
  err => {
    // global error handling
    if (err.response && err.response.status === 401) {
      // optionally redirect to login
    }
    return Promise.reject(err);
  }
);

export default {
  get: (url, params) => instance.get(url, { params }),
  post: (url, data) => instance.post(url, data),
  put: (url, data) => instance.put(url, data),
  delete: (url) => instance.delete(url)
};
