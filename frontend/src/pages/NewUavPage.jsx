import { useEffect, useState } from "react";
import axios from "axios";
import { useCookies } from "react-cookie";
import { API_URL } from "../constants";
import { toast } from "react-toastify";

const NewUavPage = () => {
  const [cookies] = useCookies(["user"]);
  const [brandsAndCategories, setBrandsAndCategories] = useState({
    brands: [],
    categories: [],
  });

  const [form, setForm] = useState({
    brand: "",
    model: "",
    category: "",
    hourly_rate: "",
    payload_capacity: "",
    maximum_speed: "",
    wingspan: "",
    endurance: "",
    image: "",
  });

  useEffect(() => {
    if (!cookies.user) {
      window.location.href = "/login";
    }
    const getBrands = async () => {
      const { data } = await axios.get(
        API_URL + "/all-brands-and-categories/",
        {
          headers: {
            Authorization: `Token ${cookies.user.token}`,
          },
        }
      );
      setBrandsAndCategories(data);
    };
    getBrands();
  }, [cookies]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    for (const [key, value] of Object.entries(form)) {
      if (value) formData.append(key, value);
    }
    const response = await axios
      .post(API_URL + "/create-uav/", formData, {
        headers: {
          Authorization: `Token ${cookies.user.token}`,
        },
      })
      .catch((err) => {
        toast.error(
          Object.keys(err.response.data)[0] +
            ": " +
            Object.values(err.response.data)[0]
        );
      });
    if (response.status === 201) {
      toast.success("UAV created successfully!");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center">
      <h2 className="text-3xl font-semibold text-center my-4">Add UAV</h2>
      <form className="grid grid-cols-2 gap-4">
        <label htmlFor="brand">Brand</label>
        <select
          id="brand"
          name="brand"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) => setForm({ ...form, brand: e.target.value })}
        >
          <option value="">Select a brand</option>
          {brandsAndCategories.brands.map((brand) => (
            <option key={brand.id} value={brand.id}>
              {brand.company} - {brand.country}
            </option>
          ))}
        </select>
        <label htmlFor="model">Model</label>
        <input
          type="text"
          id="model"
          name="model"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) => setForm({ ...form, model: e.target.value })}
        />
        <label htmlFor="category">Category</label>
        <select
          id="category"
          name="category"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) => setForm({ ...form, category: e.target.value })}
        >
          <option value="">Select a category</option>
          {brandsAndCategories.categories.map((brand) => (
            <option key={brand.id} value={brand.id}>
              {brand.category} - {brand.class_name}
            </option>
          ))}
        </select>
        <label htmlFor="hourly_rate">Hourly Rate</label>
        <input
          type="number"
          id="hourly_rate"
          name="hourly_rate"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) => setForm({ ...form, hourly_rate: e.target.value })}
        />
        <label htmlFor="payload_capacity">Payload Capacity</label>
        <input
          type="number"
          id="payload_capacity"
          name="payload_capacity"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) =>
            setForm({ ...form, payload_capacity: e.target.value })
          }
        />
        <label htmlFor="maximum_speed">Maximum Speed</label>
        <input
          type="number"
          id="maximum_speed"
          name="maximum_speed"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) => setForm({ ...form, maximum_speed: e.target.value })}
        />
        <label htmlFor="wingspan">Wingspan</label>
        <input
          type="number"
          id="wingspan"
          name="wingspan"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) => setForm({ ...form, wingspan: e.target.value })}
        />
        <label htmlFor="endurance">Endurance</label>
        <input
          type="number"
          id="endurance"
          name="endurance"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) => setForm({ ...form, endurance: e.target.value })}
        />
        <label htmlFor="image">Image</label>
        <input
          type="file"
          id="image"
          name="image"
          accept="image/*"
          className="border border-gray-300 rounded-md p-2 text-white"
          onChange={(e) => setForm({ ...form, image: e.target.files[0] })}
        />
        <button
          className="bg-blue-500 text-white rounded-md p-2"
          onClick={handleSubmit}
          type="submit"
        >
          Create
        </button>
      </form>
      {/* TODO:  Create Brand and Category */}
    </div>
  );
};

export default NewUavPage;
