import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import LandingPage from "./LandingPage";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* =====================================================
            PUBLIC LANDING PAGE
        ====================================================== */}

        <Route
          path="/"
          element={<LandingPage />}
        />

        {/* =====================================================
            AUTHENTICATION
        ====================================================== */}

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        {/* =====================================================
            APPLICATION
        ====================================================== */}

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        {/* =====================================================
            FALLBACK
            Unknown URL -> Landing Page
        ====================================================== */}

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