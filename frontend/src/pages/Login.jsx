import { Link } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import { useCookies } from "react-cookie";
import { API_URL } from "../constants";
import { toast } from "react-toastify";


const Login = () => {
  const [cookies, setCookie] = useCookies(["user"]);
  useState(() => {
    if (cookies.user && cookies.user.token) {
      window.location.href = "/";
    }
  }, [cookies]);
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.username || !formData.password) {
      alert("Please fill out all fields");
      return;
    }
    axios.post(API_URL + "/auth/login/", formData).then((res) => {
      setCookie("user", res.data, { path: "/" });
      toast.success("Logged in successfully");
      window.location.href = "/";
    }).catch((err) => {
      toast.error(err.response.data.error);
    });
  };

  return (
    <div className="flex flex-col items-center justify-center w-full h-full">
      <h1 className="text-5xl font-bold">Login</h1>
      <Link to="/signup" className="mt-3 text-primary hover:text-orange-300">
        Don&apos;t have an account? Sign up here.
      </Link>
      <div className="max-w-md mx-auto mt-8 p-4 bg-white rounded shadow-md">
        <form onSubmit={handleSubmit}>
          {/* Username */}
          <div className="mb-4">
            <label
              htmlFor="username"
              className="block text-sm font-medium text-gray-600"
            >
              Username
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="w-full px-4 py-2 mt-2 border rounded-lg text-black"
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-600"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="w-full px-4 py-2 mt-2 border rounded-lg text-black"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-secondary text-white font-semibold p-3 rounded-lg hover:bg-secondary/90 transition-all"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
