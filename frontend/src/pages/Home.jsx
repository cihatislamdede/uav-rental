import { useCookies } from "react-cookie";
import { Link } from "react-router-dom";

const Home = () => {
  const [cookies] = useCookies(["user"]);

  return (
    <div className="flex flex-col items-center justify-center w-full h-full">
      <div className="grid grid-row-3 gap-4">
        {cookies.user ? (
          <>
            <Link
              to="/brands"
              className="flex items-center justify-center p-4 bg-secondary rounded shadow-md hover:bg-secondary-light hover:bg-secondary/80"
            >
              <h1 className="text-2xl font-bold">Brands</h1>
            </Link>
            <Link
              to="/categories"
              className="flex items-center justify-center p-4 bg-secondary rounded shadow-md hover:bg-secondary-light hover:bg-secondary/80"
            >
              <h1 className="text-2xl font-bold">Categories</h1>
            </Link>
            <Link
              to="/uavs"
              className="flex items-center justify-center p-4 bg-secondary rounded shadow-md hover:bg-secondary-light hover:bg-secondary/80"
            >
              <h1 className="text-2xl font-bold">UAVs</h1>
            </Link>
          </>
        ) : (
          <Link
              to="/rentals"
              className="flex items-center justify-center p-4 bg-secondary rounded shadow-md hover:bg-secondary-light hover:bg-secondary/80"
            >
              <h1 className="text-2xl font-bold">My Rentals</h1>
            </Link>
        )}
      </div>
    </div>
  );
};

export default Home;
