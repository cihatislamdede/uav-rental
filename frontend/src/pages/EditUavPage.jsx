import { useEffect, useState } from "react";
import axios from "axios";
import { useCookies } from "react-cookie";
import { API_URL } from "../constants";
import { toast } from "react-toastify";
import { useParams } from "react-router-dom";

const EditUavPage = () => {
  const { id } = useParams();

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

  const [oldImageUrl, setOldImageUrl] = useState("");

  useEffect(() => {
    if (!cookies.user) {
      window.location.href = "/login";
    }
    const getUav = async () => {
      const { data } = await axios.get(API_URL + "/uav/" + id + "/", {
        headers: {
          Authorization: `Token ${cookies.user.token}`,
        },
      }).catch((err) => {
        if (err.response.status === 404) {
          window.location.href = "/new-reservation";
        }
      });
      setOldImageUrl(data.image);
      delete data.image;
      setForm(data);
    };
    const getBrands = async () => {
      const { data } = await axios.get(
        API_URL + "/all-brands-and-categories/",
        {
          headers: {
            Authorization: `Token ${cookies.user.token}`,
          },
        }
      )
      setBrandsAndCategories(data);
    };
    getUav();
    getBrands();
  }, [id, cookies]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    for (const [key, value] of Object.entries(form)) {
      if (value) formData.append(key, value);
    }
    const response = await axios
      .put(API_URL + "/update-uav/" + id + "/", formData, {
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
    if (response.status === 202) {
      toast.success("UAV updated successfully!");
      await new Promise((resolve) => setTimeout(resolve, 1000));
      window.location.reload();
    }
  };

  return (
    <div className="flex flex-col items-center justify-center">
      <h2 className="text-3xl font-semibold text-center my-4">Edit UAV {id}</h2>
      <form className="grid grid-cols-2 gap-4">
        <label htmlFor="brand">Brand</label>
        <select
          id="brand"
          name="brand"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) => setForm({ ...form, brand: e.target.value })}
          value={form.brand}
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
          value={form.model}
        />
        <label htmlFor="category">Category</label>
        <select
          id="category"
          name="category"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) => setForm({ ...form, category: e.target.value })}
          value={form.category}
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
          value={form.hourly_rate}
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
          value={form.payload_capacity}
        />
        <label htmlFor="maximum_speed">Maximum Speed</label>
        <input
          type="number"
          id="maximum_speed"
          name="maximum_speed"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) => setForm({ ...form, maximum_speed: e.target.value })}
          value={form.maximum_speed}
        />
        <label htmlFor="wingspan">Wingspan</label>
        <input
          type="number"
          id="wingspan"
          name="wingspan"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) => setForm({ ...form, wingspan: e.target.value })}
          value={form.wingspan}
        />
        <label htmlFor="endurance">Endurance</label>
        <input
          type="number"
          id="endurance"
          name="endurance"
          className="border border-gray-300 rounded-md p-2 text-black"
          onChange={(e) => setForm({ ...form, endurance: e.target.value })}
          value={form.endurance}
        />
        <label htmlFor="image">Image</label>
        <div>
          <input
            type="file"
            id="image"
            name="image"
            accept="image/*"
            className="border border-gray-300 rounded-md p-2 text-white"
            onChange={(e) => setForm({ ...form, image: e.target.files[0] })}
          />
          {oldImageUrl && (
            <img
              src={"http://localhost:8000" + oldImageUrl}
              alt="current-image"
              className="h-24 object-cover rounded mt-2 mx-auto"
            />
          )}
        </div>
        <button
          className="bg-blue-500 text-white rounded-md p-2"
          onClick={handleSubmit}
          type="submit"
        >
          Edit
        </button>
      </form>
      <button
        className="bg-red-500 text-white rounded-md p-2 mt-2"
        onClick={async () => {
          await axios.delete(API_URL + "/update-uav/" + id + "/", {
            headers: {
              Authorization: `Token ${cookies.user.token}`,
            },
          });
          toast.success("UAV deleted successfully!");
          await new Promise((resolve) => setTimeout(resolve, 1000));
          window.location.href = "/new-reservation";
        }}
      >
        Delete
      </button>
    </div>
  );
};

export default EditUavPage;
