import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import LandingPage from "./LandingPage";
import Login from "./pages/Login";
import Register from "./pages/Register";
import VerifyOTP from "./pages/VerifyOTP";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Landing */}
        <Route
          path="/"
          element={<LandingPage />}
        />

        {/* Authentication */}
        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        <Route
          path="/verify-otp"
          element={<VerifyOTP />}
        />

        <Route
          path="/forgot-password"
          element={<ForgotPassword />}
        />

        <Route
          path="/reset-password"
          element={<ResetPassword />}
        />

        {/* Dashboard */}
        <Route
          path="/dashboard/*"
          element={<Dashboard />}
        />

        {/* Unknown route */}
        <Route
          path="*"
          element={
            <Navigate
              to="/"
              replace
            />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;