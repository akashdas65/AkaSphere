import { useEffect, useState } from "react";
import {
  LogOut,
  MessageSquare,
  Sparkles,
  Users,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  is_active: boolean;
  is_verified: boolean;
}

function Dashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const response = await api.get("/auth/me");
        setUser(response.data);
      } catch {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        navigate("/login");
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, [navigate]);

  const logout = async () => {
    const refreshToken = localStorage.getItem("refresh_token");

    try {
      if (refreshToken) {
        await api.post("/auth/logout", {
          refresh_token: refreshToken,
        });
      }
    } catch {
      // Token may already be invalid.
    } finally {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      navigate("/login");
    }
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <Sparkles className="loading-icon" size={30} />
        <p>Loading your workspace...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <header className="dashboard-navbar">
        <div className="logo">
          <div className="logo-mark">
            <Sparkles size={18} />
          </div>

          <span>AkaSphere</span>
        </div>

        <button
          className="btn btn-secondary"
          type="button"
          onClick={logout}
        >
          <LogOut size={16} />
          Logout
        </button>
      </header>

      <main className="workspace">
        <div className="welcome-card">
          <div>
            <span className="eyebrow">
              YOUR WORKSPACE
            </span>

            <h1>
              Welcome, {user?.full_name || user?.username} 👋
            </h1>

            <p>
              Your AkaSphere workspace is ready.
            </p>
          </div>

          <div className="workspace-avatar">
            {user?.full_name?.charAt(0).toUpperCase() ||
              "A"}
          </div>
        </div>

        <div className="dashboard-grid">
          <div className="workspace-card">
            <MessageSquare size={25} />

            <h2>Messages</h2>

            <p>
              Communicate with your team through
              organized channels.
            </p>
          </div>

          <div className="workspace-card">
            <Users size={25} />

            <h2>Team</h2>

            <p>
              Manage members and collaborate on
              projects.
            </p>
          </div>

          <div className="workspace-card">
            <Sparkles size={25} />

            <h2>AI Assistant</h2>

            <p>
              Get intelligent assistance directly
              inside your workspace.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;