import { Link } from "react-router-dom";

const MainHero = () => {
  return (
    <div className="container mx-auto py-9">
      <div className="relative mx-4">
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Bayraktar_TB2_Runway.jpg/1920px-Bayraktar_TB2_Runway.jpg"
          alt="A work table with house plants"
          className="w-full bg-secondary/80 rounded blur-sm"
        />
        <div className="absolute z-10 top-0 left-0 mx-4 sm:mx-0 mt-36 sm:mt-0 sm:py-20 md:py-28 lg:py-20 xl:py-28 sm:pl-14 flex flex-col sm:justify-start items-start">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-semibold text-white sm:text-secondary sm:w-8/12">
            Rent UAVs
          </h1>
          <Link
            to="/login"
            className="flex bg-secondary rounded py-4 px-8 text-base font-medium text-white mt-8 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-800 hover:bg-gray-700"
          >
            Login
          </Link>
        </div>
      </div>
    </div>
  );
};

export default MainHero;
