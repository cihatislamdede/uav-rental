import { useState } from "react";
import { toast } from "react-toastify";
import axios from "axios";
import { API_URL } from "../constants";
import { useCookies } from "react-cookie";

function SignUp() {
  const [cookies, setCookie] = useCookies(["user"]);
  useState(() => {
    if (cookies.user && cookies.user.token) {
      window.location.href = "/";
    }
  }, [cookies]);

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    country: "",
    company: "",
    is_renter: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.username || !formData.email || !formData.password) {
      toast.error("Please fill out all required fields");
      return;
    }
    if (formData.password.length < 8) {
      toast.error("Password must be at least 8 characters long");
      return;
    }
    axios
      .post(API_URL + "/auth/register/", formData)
      .then((res) => {
        setCookie("user", res.data, { path: "/" });
        toast.success("Registered successfully");
        window.location.href = "/";
      })
      .catch((err) => {
        toast.error(err.response.data.error);
      });
  };

  return (
    <div className="max-w-md mx-auto mt-8 p-4 bg-white rounded shadow-md">
      <form onSubmit={handleSubmit}>
        {/* Username */}
        <div className="mb-4">
          <label
            htmlFor="username"
            className="block text-sm font-medium text-gray-600"
          >
            Username*
          </label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 mt-2 border rounded-lg text-black"
          />
        </div>

        {/* Email */}
        <div className="mb-4">
          <label
            htmlFor="email"
            className="block text-sm font-medium text-gray-600"
          >
            Email*
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 mt-2 border rounded-lg text-black"
          />
        </div>

        {/* Password */}
        <div className="mb-4">
          <label
            htmlFor="password"
            className="block text-sm font-medium text-gray-600"
          >
            Password*
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 mt-2 border rounded-lg text-black"
          />
        </div>

        {/* First Name */}
        <div className="mb-4">
          <label
            htmlFor="first_name"
            className="block text-sm font-medium text-gray-600"
          >
            First Name
          </label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            className="w-full px-4 py-2 mt-2 border rounded-lg text-black"
          />
        </div>

        {/* Last Name */}
        <div className="mb-4">
          <label
            htmlFor="last_name"
            className="block text-sm font-medium text-gray-600"
          >
            Last Name
          </label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            className="w-full px-4 py-2 mt-2 border rounded-lg text-black"
          />
        </div>

        {/* Country */}
        <div className="mb-4">
          <label
            htmlFor="country"
            className="block text-sm font-medium text-gray-600"
          >
            Country
          </label>
          <input
            type="text"
            id="country"
            name="country"
            value={formData.country}
            onChange={handleChange}
            className="w-full px-4 py-2 mt-2 border rounded-lg text-black"
          />
        </div>

        {/* Company */}
        <div className="mb-4">
          <label
            htmlFor="company"
            className="block text-sm font-medium text-gray-600"
          >
            Company
          </label>
          <input
            type="text"
            id="company"
            name="company"
            value={formData.company}
            onChange={handleChange}
            className="w-full px-4 py-2 mt-2 border rounded-lg text-black"
          />
        </div>

        {/* Checkbox for 'is_renter' */}
        <div className="mb-4">
          <input
            type="checkbox"
            id="is_renter"
            name="is_renter"
            checked={formData.is_renter}
            onChange={handleChange}
            className="mr-2"
          />
          <label
            htmlFor="is_renter"
            className="text-sm font-medium text-gray-600"
          >
            I am a renter
          </label>
        </div>

        <button
          type="submit"
          className="w-full bg-secondary text-white font-semibold p-3 rounded-lg hover:bg-secondary/90 transition-all"
        >
          Register
        </button>
      </form>
    </div>
  );
}

export default SignUp;
