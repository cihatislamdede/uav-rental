import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./index.css";
import "react-toastify/dist/ReactToastify.min.css";
import { ToastContainer } from "react-toastify";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import NewReservation from "./pages/NewReservation";
import NewUavPage from "./pages/NewUavPage";
import EditUavPage from "./pages/EditUavPage";
import ReserveUavPage from "./pages/ReserveUavPage";
import EditReserveUavPage from "./pages/EditReserveUavPage";
import ReservationsPage from "./pages/ReservationsPage";

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <ToastContainer
        pauseOnFocusLoss={false}
        closeOnClick
        draggable
        pauseOnHover={false}
        position="bottom-right"
        rtl={false}
        hideProgressBar={false}
        autoClose={2000}
        newestOnTop={true}
      />
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/new-reservation" element={<NewReservation />} />
          <Route path="/uavs/new" element={<NewUavPage />} />
          <Route path="/uavs/:id/edit" element={<EditUavPage />} />
          <Route path="/uavs/:id/reserve" element={<ReserveUavPage />} />
          <Route path="/reservations" element={<ReservationsPage />} />
          <Route path="/reservations/:id/edit" element={<EditReserveUavPage />} />
        </Routes>
        <Footer />
      </Router>
    </div>
  );
}

export default App;
