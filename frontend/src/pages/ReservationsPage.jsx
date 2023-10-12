import { useState } from "react";
import axios from "axios";
import { API_URL, PAGE_SIZE } from "../constants";
import { useCookies } from "react-cookie";
import { Card, Typography } from "@material-tailwind/react";
import { Link } from "react-router-dom";

const ReservationsPage = () => {
  const [data, setData] = useState([]);
  const [tableHeaders, setTableHeaders] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState("");
  const [cookies] = useCookies(["user"]);

  const fetchData = async (page = currentPage) => {
    const response = await axios.get(
      API_URL + `/reservations/?user=${cookies.user.id}&search=${search}&page=${page}`,
      {
        headers: {
          Authorization: `Token ${cookies.user.token}`,
        },
      }
    );
    setData(response.data);
    setTableHeaders(Object.keys(response.data.results[0]));
  };

  useState(() => {
    if (!cookies.user) {
      window.location.href = "/";
    }
    fetchData();
  }, [cookies]);

  const next = (e) => {
    e.preventDefault();
    setCurrentPage(currentPage + 1);
    fetchData(currentPage + 1);
  };

  const prev = (e) => {
    e.preventDefault();
    setCurrentPage(currentPage - 1);
    fetchData(currentPage - 1);
  };

  return (
    <div className="container mx-auto">
      <h2 className="text-3xl font-semibold text-center my-4">
        My Reservations
      </h2>
      <div className="flex justify-between">
        {cookies.user.is_renter && (
          <Link
            to="/new-reservation"
            className="bg-primary text-white rounded-md p-2 mb-4"
          >
            Create Reservation
          </Link>
        )}
        <form className="flex mb-2" onSubmit={(e) => e.preventDefault()}>
          <input
            type="text"
            className="border-2 border-blue-200 rounded-md p-2 text-black"
            placeholder="Search"
            onChange={(e) => setSearch(e.target.value)}
          />
          <button
            className="bg-slate-300 text-black rounded-md p-2 ml-2"
            onClick={() => {
              fetchData(1);
            }}
            type="submit"
          >
            Search
          </button>
        </form>
      </div>
      <Card className="container mx-auto rounded-md text-black">
        <table className="table-auto text-center">
          {" "}
          <thead>
            <tr>
              {tableHeaders.map((head) => (
                <th
                  key={head}
                  className="border-b border-blue-gray-100 bg-blue-100 p-4"
                >
                  <Typography
                    variant="small"
                    color="blue-gray"
                    className="font-bold leading-none opacity-70"
                  >
                    {head}
                  </Typography>
                </th>
              ))}
              <th
                key="action"
                className="border-b border-blue-gray-100 bg-blue-100 p-4"
              >
                <Typography
                  variant="small"
                  color="blue-gray"
                  className="font-bold leading-none opacity-70"
                >
                  action
                </Typography>
              </th>
            </tr>
          </thead>
          <tbody className="text-blue-gray-500 text-sm font-light">
            {data.results?.map((row) => (
              <tr key={row.id} className="border-t border-blue-200">
                {tableHeaders.map((head) => (
                  <td key={head} className="p-4">
                    {["start_time", "end_time", "created_at"].includes(head) &&
                    row[head]
                      ? new Date(row[head]).toLocaleString()
                      : row[head] || "-"}
                  </td>
                ))}
                <td className="p-2 flex flex-col">
                  <Link
                    to={`/reservations/${row.id}/edit`}
                    className="bg-secondary text-white rounded-md p-2"
                  >
                    Update
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
      <div className="mx-auto flex justify-center mt-4 gap-x-8 items-center">
        <button
          className={`bg-secondary text-white rounded-md p-2 ${
            currentPage === 1 ? "opacity-50 cursor-not-allowed" : ""
          }`}
          onClick={prev}
          disabled={currentPage === 1}
        >
          Prev
        </button>
        <div>
          <strong className="text-gray-100">{currentPage}</strong> of{" "}
          <strong className="text-gray-100">
            {(data.count / PAGE_SIZE).toFixed(0) == 0
              ? 1
              : (data.count / PAGE_SIZE).toFixed(0)}
          </strong>
        </div>
        <button
          onClick={next}
          className={`bg-secondary text-white rounded-md p-2 ${
            currentPage === data.count / PAGE_SIZE ||
            (data.count / PAGE_SIZE).toFixed(0) == 0
              ? "opacity-50 cursor-not-allowed"
              : ""
          }`}
          disabled={
            currentPage === data.count / PAGE_SIZE ||
            (data.count / PAGE_SIZE).toFixed(0) == 0
          }
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default ReservationsPage;
