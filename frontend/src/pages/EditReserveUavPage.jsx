import { useEffect, useState } from "react";
import axios from "axios";
import { useCookies } from "react-cookie";
import { API_URL } from "../constants";
import { toast } from "react-toastify";
import { useParams } from "react-router-dom";

const EditReserveUavPage = () => {
  const { id } = useParams();
  const [cookies] = useCookies(["user"]);
  const [uavData, setUavData] = useState({});

  const [form, setForm] = useState({
    uav: "",
    start_time: "",
    end_time: "",
  });

  useEffect(() => {
    if (!cookies.user) {
      window.location.href = "/login";
    }
    const getReservation = async () => {
      const { data } = await axios
        .get(API_URL + "/reservations/" + id + "/", {
          headers: {
            Authorization: `Token ${cookies.user.token}`,
          },
        })
        .catch((err) => {
          if (err.response.status === 404) {
            window.location.href = "/reservations";
          }
        });
      setForm({
        uav: data.uav,
        start_time: data.start_time,
        end_time: data.end_time,
      });
    };
    getReservation();
  }, [id, cookies]);

  useEffect(() => {
    const getUav = async () => {
      if (!form.uav) return;
      const { data } = await axios.get(API_URL + "/uav/" + form.uav + "/", {
        headers: {
          Authorization: `Token ${cookies.user.token}`,
        },
      });
      setUavData(data);
    };
    getUav();
  }, [cookies, form.uav]);

  function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    const hour = String(date.getHours()).padStart(2, "0");
    const minute = String(date.getMinutes()).padStart(2, "0");

    return `${year}-${month}-${day} ${hour}:${minute}`;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    const start_time = formatDate(new Date(form.start_time));
    const end_time = formatDate(new Date(form.end_time));

    formData.append("uav", form.uav);
    formData.append("start_time", start_time);
    formData.append("end_time", end_time);

    const response = await axios
      .put(API_URL + "/reservations/" + id + "/", formData, {
        headers: {
          Authorization: `Token ${cookies.user.token}`,
          "Content-Type": "application/json",
        },
      })
      .catch((err) => {
        toast.error(
          err.response.data || "Something went wrong. Please try again later."
        );
      });

    if (response.status === 200) {
      toast.success("Reservation updated!");
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
    window.location.reload();
  };

  return (
    <div className="flex flex-col items-center justify-center">
      <h2 className="text-3xl font-semibold text-center my-4">
        Reserve UAV {id}
      </h2>
      <div className="flex flex-col">
        <label htmlFor="uav" className="text-center font-bold text-3xl">
          UAV Spec
        </label>
        <div className="grid grid-cols-2 gap-2 justify-center text-center my-2">
          {Object.keys(uavData).map((key) => (
            <p key={key} className="flex flex-row ">
              <span className="font-bold">{key}</span>: {uavData[key]}
            </p>
          ))}
        </div>
      </div>

      <form className="flex flex-col gap-y-2 mt-4" onSubmit={handleSubmit}>
        {/* start date - end date calendar select*/}
        <div className="grid grid-cols-2 gap-2 justify-center">
          <div className="flex flex-col">
            <label htmlFor="start_time" className="font-semibold text-xl">
              Start Time
            </label>
            <input
              type="datetime-local"
              name="start_time"
              id="start_time"
              className="border border-gray-300 rounded px-4 py-2 text-black"
              onChange={(e) => setForm({ ...form, start_time: e.target.value })}
              value={form.start_time.split("Z")[0]}
            />
          </div>
          <div className="flex flex-col">
            <label htmlFor="end_time" className="font-semibold text-xl">
              End Time
            </label>
            <input
              type="datetime-local"
              name="end_time"
              id="end_time"
              className="border border-gray-300 rounded px-4 py-2 text-black"
              onChange={(e) => setForm({ ...form, end_time: e.target.value })}
              value={form.end_time.split("Z")[0]}
            />
          </div>
        </div>

        <button
          type="submit"
          className="bg-accent transition duration-150 ease-in-out hover:bg-pink-600 rounded text-white px-8 py-3 text-center"
        >
          Update
        </button>
      </form>
      <button
        className="bg-red-500 text-white rounded-md p-2 mt-2"
        onClick={async () => {
          await axios.delete(API_URL + "/reservations/" + id + "/", {
            headers: {
              Authorization: `Token ${cookies.user.token}`,
            },
          });
          toast.success("Reservation deleted successfully!");
          await new Promise((resolve) => setTimeout(resolve, 1000));
          window.location.href = "/reservations";
        }}
      >
        Delete
      </button>
    </div>
  );
};

export default EditReserveUavPage;
