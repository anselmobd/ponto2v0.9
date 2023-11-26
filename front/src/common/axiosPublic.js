import axios from "axios";

export const axiosPublic = axios.create({
  baseURL: "http://tt.o2:8902",
  headers: {
    "Content-Type": "application/json",
  },
});
