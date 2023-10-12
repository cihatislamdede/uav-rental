import { useCookies } from "react-cookie";
import MainHero from "../components/MainHero";
import { Link } from "react-router-dom";

const Home = () => {
  const [cookies] = useCookies(["user"]);

  return (
    <div className="flex flex-col items-center justify-center">
      <div>
        {cookies.user ? (
          <div className="container flex flex-col gap-x-2 justify-center">
            <h1 className="text-3xl text-slate-400 text-center">
              Welcome,{" "}
              <span className="font-bold text-slate-200">
                {cookies.user.username}!
              </span>
            </h1>
            {/* create 3 side buttons */}
            <div className="flex flex-col gap-x-2 mt-4">
              <Link
                to="/new-reservation"
                className="mx-2 my-2 bg-accent transition duration-150 ease-in-out hover:bg-pink-600 rounded text-white px-8 py-3 text-center"
              >
                New Reservation
              </Link>
              <Link
                to="/reservations"
                className="mx-2 my-2 bg-accent transition duration-150 ease-in-out hover:bg-pink-600 rounded text-white px-8 py-3 text-center"
              >
                My Reservations
              </Link>
            </div>
          </div>
        ) : (
          <MainHero />
        )}
      </div>
    </div>
  );
};

export default Home;
