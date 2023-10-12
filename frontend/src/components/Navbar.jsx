import { Link } from "react-router-dom";
import { useCookies } from "react-cookie";
import { toast } from "react-toastify";

const Navbar = () => {
  const [cookies, setCookie] = useCookies(["user"]);

  function handleLogout() {
    setCookie("user", null, {
      path: "/",
      maxAge: 0,
    });
    toast.success("Logged out successfully");
  }

  return (
    <header className="flex items-center relative justify-between px-5 py-4 w-full ">
      <div>
        <h1 className="text-2xl font-bold hover:dark:text-gray-400 hover:text-gray-600 transition-all">
          <Link to="/">UAV Rental</Link>
        </h1>
      </div>
      <div>
        {cookies.user ? (
          <div className="flex items-center space-x-5">
            <Link
              to="/"
              onClick={() => handleLogout()}
              className="text-lg font-semibold hover:dark:text-gray-400 hover:text-gray-600 transition-all"
            >
              Logout
            </Link>
          </div>
        ) : (
          <Link
            to="/login"
            className="text-lg font-semibold hover:dark:text-gray-400 hover:text-gray-600 transition-all"
          >
            Login
          </Link>
        )}
      </div>
    </header>
  );
};

export default Navbar;
