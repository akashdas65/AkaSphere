import { useEffect, useMemo, useState } from "react";

import {
  Bell,
  Bot,
  ChevronDown,
  Hash,
  Home,
  LogOut,
  MessageSquare,
  Plus,
  Search,
  Settings,
  Sparkles,
  Users,
  Zap,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import api from "../services/api";

/* ============================================================
   TYPES
============================================================ */

interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  is_active: boolean;
  is_verified: boolean;
}

interface Channel {
  name: string;
  unread: number;
}

/* ============================================================
   STATIC UI DATA
   These will later be replaced with real API data.
============================================================ */

const channels: Channel[] = [
  {
    name: "general",
    unread: 0,
  },
  {
    name: "engineering",
    unread: 4,
  },
  {
    name: "design",
    unread: 2,
  },
  {
    name: "projects",
    unread: 0,
  },
];

/* ============================================================
   DASHBOARD
============================================================ */

function Dashboard() {
  const navigate = useNavigate();

  /* ----------------------------------------------------------
     STATE
  ---------------------------------------------------------- */

  const [user, setUser] = useState<User | null>(null);

  const [loading, setLoading] = useState(true);

  const [activeNav, setActiveNav] = useState("Overview");

  const [searchQuery, setSearchQuery] = useState("");

  const [notificationsOpen, setNotificationsOpen] =
    useState(false);

  const [profileOpen, setProfileOpen] =
    useState(false);

  /* ----------------------------------------------------------
     LOAD CURRENT USER
  ---------------------------------------------------------- */

  useEffect(() => {
    let mounted = true;

    const loadUser = async () => {
      const accessToken =
        localStorage.getItem("access_token");

      if (!accessToken) {
        navigate("/login", {
          replace: true,
        });

        return;
      }

      try {
        const response = await api.get("/auth/me");

        if (mounted) {
          setUser(response.data);
        }
      } catch (error) {
        console.error(
          "Failed to load current user:",
          error,
        );

        localStorage.removeItem(
          "access_token",
        );

        localStorage.removeItem(
          "refresh_token",
        );

        if (mounted) {
          navigate("/login", {
            replace: true,
          });
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadUser();

    return () => {
      mounted = false;
    };
  }, [navigate]);

  /* ----------------------------------------------------------
     LOGOUT
  ---------------------------------------------------------- */

  const logout = async () => {
    const refreshToken =
      localStorage.getItem("refresh_token");

    try {
      if (refreshToken) {
        await api.post(
          "/auth/logout",
          {
            refresh_token: refreshToken,
          },
        );
      }
    } catch (error) {
      console.error(
        "Logout API request failed:",
        error,
      );
    } finally {
      localStorage.removeItem(
        "access_token",
      );

      localStorage.removeItem(
        "refresh_token",
      );

      navigate("/login", {
        replace: true,
      });
    }
  };

  /* ----------------------------------------------------------
     USER DISPLAY DATA
  ---------------------------------------------------------- */

  const firstName = useMemo(() => {
    if (user?.full_name) {
      return user.full_name.split(" ")[0];
    }

    if (user?.username) {
      return user.username;
    }

    return "Akash";
  }, [user]);

  const avatarLetter = useMemo(() => {
    if (user?.full_name) {
      return user.full_name
        .charAt(0)
        .toUpperCase();
    }

    if (user?.username) {
      return user.username
        .charAt(0)
        .toUpperCase();
    }

    return "A";
  }, [user]);

  /* ----------------------------------------------------------
     SEARCH
  ---------------------------------------------------------- */

  const handleSearch = (
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    const query =
      searchQuery.trim();

    if (!query) {
      return;
    }

    console.log(
      "Workspace search:",
      query,
    );
  };

  /* ----------------------------------------------------------
     NAVIGATION HANDLER
  ---------------------------------------------------------- */

  const handleNavigation = (
    name: string,
  ) => {
    setActiveNav(name);

    setNotificationsOpen(false);
    setProfileOpen(false);
  };

  /* ----------------------------------------------------------
     CHANNEL HANDLER
  ---------------------------------------------------------- */

  const handleChannelClick = (
    channelName: string,
  ) => {
    setActiveNav(channelName);

    console.log(
      "Selected channel:",
      channelName,
    );
  };

  /* ----------------------------------------------------------
     LOADING SCREEN
  ---------------------------------------------------------- */

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-logo">
          <Sparkles size={26} />
        </div>

        <h2>
          Loading AkaSphere
        </h2>

        <p>
          Preparing your workspace...
        </p>
      </div>
    );
  }

  /* ==========================================================
     MAIN DASHBOARD
  ========================================================== */

  return (
    <div className="dashboard-page">

      {/* ======================================================
          SIDEBAR
      ======================================================= */}

      <aside className="dashboard-sidebar">

        {/* ----------------------------------------------------
            BRAND
        ----------------------------------------------------- */}

        <div className="dashboard-brand">

          <div className="dashboard-brand-icon">
            <Sparkles size={19} />
          </div>

          <div>
            <strong>
              AkaSphere
            </strong>

            <span>
              Workspace
            </span>
          </div>

        </div>

        {/* ----------------------------------------------------
            WORKSPACE SELECTOR
        ----------------------------------------------------- */}

        <button
          className="workspace-selector"
          type="button"
          onClick={() =>
            handleNavigation("Overview")
          }
        >
          <div className="workspace-selector-icon">
            A
          </div>

          <div className="workspace-selector-info">
            <strong>
              AkaSphere
            </strong>

            <span>
              Personal workspace
            </span>
          </div>

          <ChevronDown size={16} />
        </button>

        {/* ----------------------------------------------------
            MAIN NAVIGATION
        ----------------------------------------------------- */}

        <div className="sidebar-group">

          <span className="sidebar-heading">
            WORKSPACE
          </span>

          {/* Overview */}

          <button
            type="button"
            className={`sidebar-nav ${
              activeNav === "Overview"
                ? "active"
                : ""
            }`}
            onClick={() =>
              handleNavigation("Overview")
            }
          >
            <Home size={18} />

            <span>
              Overview
            </span>
          </button>

          {/* Messages */}

          <button
            type="button"
            className={`sidebar-nav ${
              activeNav === "Messages"
                ? "active"
                : ""
            }`}
            onClick={() =>
              handleNavigation("Messages")
            }
          >
            <MessageSquare size={18} />

            <span>
              Messages
            </span>

            <span className="nav-count">
              6
            </span>
          </button>

          {/* Team */}

          <button
            type="button"
            className={`sidebar-nav ${
              activeNav === "Team"
                ? "active"
                : ""
            }`}
            onClick={() =>
              handleNavigation("Team")
            }
          >
            <Users size={18} />

            <span>
              Team
            </span>
          </button>

          {/* AI Assistant */}

          <button
            type="button"
            className={`sidebar-nav ${
              activeNav === "AI Assistant"
                ? "active"
                : ""
            }`}
            onClick={() =>
              handleNavigation(
                "AI Assistant",
              )
            }
          >
            <Bot size={18} />

            <span>
              AI Assistant
            </span>

            <span className="ai-badge">
              AI
            </span>
          </button>

        </div>

        {/* ----------------------------------------------------
            CHANNELS
        ----------------------------------------------------- */}

        <div className="sidebar-group channels-group">

          <div className="sidebar-heading-row">

            <span className="sidebar-heading">
              CHANNELS
            </span>

            <button
              type="button"
              className="sidebar-add"
              aria-label="Create channel"
              onClick={() =>
                console.log(
                  "Create channel clicked",
                )
              }
            >
              <Plus size={15} />
            </button>

          </div>

          {channels.map(
            (channel) => (
              <button
                type="button"
                className={`sidebar-channel ${
                  activeNav === channel.name
                    ? "active"
                    : ""
                }`}
                key={channel.name}
                onClick={() =>
                  handleChannelClick(
                    channel.name,
                  )
                }
              >
                <Hash size={16} />

                <span>
                  {channel.name}
                </span>

                {channel.unread > 0 && (
                  <span className="channel-unread">
                    {channel.unread}
                  </span>
                )}
              </button>
            ),
          )}

        </div>

        {/* ----------------------------------------------------
            BOTTOM NAVIGATION
        ----------------------------------------------------- */}

        <div className="sidebar-bottom">

          <button
            type="button"
            className={`sidebar-nav ${
              activeNav === "Settings"
                ? "active"
                : ""
            }`}
            onClick={() =>
              handleNavigation("Settings")
            }
          >
            <Settings size={18} />

            <span>
              Settings
            </span>
          </button>

          <button
            type="button"
            className="sidebar-nav logout-nav"
            onClick={logout}
          >
            <LogOut size={18} />

            <span>
              Logout
            </span>
          </button>

        </div>

      </aside>

      {/* ======================================================
          MAIN AREA
      ======================================================= */}

      <div className="dashboard-main">

        {/* ====================================================
            TOP NAVBAR
        ===================================================== */}

        <header className="dashboard-topbar">

          {/* SEARCH */}

          <form
            className="dashboard-search"
            onSubmit={handleSearch}
          >
            <Search size={18} />

            <input
              type="text"
              value={searchQuery}
              onChange={(event) =>
                setSearchQuery(
                  event.target.value,
                )
              }
              placeholder="Search workspace..."
              aria-label="Search workspace"
            />

            <kbd>
              Ctrl K
            </kbd>
          </form>

          {/* TOP ACTIONS */}

          <div className="topbar-actions">

            {/* Notifications */}

            <div className="topbar-menu">

              <button
                type="button"
                className="topbar-icon"
                aria-label="Notifications"
                onClick={() =>
                  setNotificationsOpen(
                    (previous) =>
                      !previous,
                  )
                }
              >
                <Bell size={19} />

                <span className="notification-dot" />
              </button>

              {notificationsOpen && (
                <div className="topbar-dropdown notification-dropdown">

                  <strong>
                    Notifications
                  </strong>

                  <p>
                    No new notifications.
                  </p>

                </div>
              )}

            </div>

            <div className="topbar-divider" />

            {/* Profile */}

            <div className="topbar-menu">

              <button
                type="button"
                className="profile-button"
                onClick={() =>
                  setProfileOpen(
                    (previous) =>
                      !previous,
                  )
                }
              >

                <div className="profile-avatar">
                  {avatarLetter}
                </div>

                <div className="profile-info">

                  <strong>
                    {user?.full_name ||
                      "Akash Das"}
                  </strong>

                  <span>
                    {user?.email ||
                      "akash@example.com"}
                  </span>

                </div>

                <ChevronDown size={16} />

              </button>

              {profileOpen && (
                <div className="topbar-dropdown profile-dropdown">

                  <div className="dropdown-user">

                    <div className="profile-avatar">
                      {avatarLetter}
                    </div>

                    <div>
                      <strong>
                        {user?.full_name ||
                          "Akash Das"}
                      </strong>

                      <span>
                        {user?.email ||
                          "akash@example.com"}
                      </span>
                    </div>

                  </div>

                  <button
                    type="button"
                    onClick={() =>
                      handleNavigation(
                        "Settings",
                      )
                    }
                  >
                    <Settings
                      size={16}
                    />

                    Settings
                  </button>

                  <button
                    type="button"
                    onClick={logout}
                  >
                    <LogOut
                      size={16}
                    />

                    Logout
                  </button>

                </div>
              )}

            </div>

          </div>

        </header>

        {/* ====================================================
            CONTENT
        ===================================================== */}

        <main className="dashboard-content">

          {/* --------------------------------------------------
              HEADING
          --------------------------------------------------- */}

          <section className="dashboard-heading">

            <div>

              <span className="dashboard-eyebrow">
                YOUR WORKSPACE
              </span>

              <h1>
                Good morning,{" "}
                {firstName} 👋
              </h1>

              <p>
                Here's what's happening
                across your workspace
                today.
              </p>

            </div>

            <button
              type="button"
              className="dashboard-primary-button"
              onClick={() =>
                console.log(
                  "Create project clicked",
                )
              }
            >
              <Plus size={18} />

              New project
            </button>

          </section>

          {/* ==================================================
              STATS
          =================================================== */}

          <section className="stats-grid">

            {/* Messages */}

            <article className="stat-card">

              <div className="stat-card-top">

                <div className="stat-icon">
                  <MessageSquare
                    size={20}
                  />
                </div>

                <span className="stat-change positive">
                  +18%
                </span>

              </div>

              <div className="stat-value">
                128
              </div>

              <div className="stat-label">
                Messages this week
              </div>

            </article>

            {/* Team */}

            <article className="stat-card">

              <div className="stat-card-top">

                <div className="stat-icon">
                  <Users size={20} />
                </div>

                <span className="stat-change positive">
                  +3
                </span>

              </div>

              <div className="stat-value">
                24
              </div>

              <div className="stat-label">
                Team members
              </div>

            </article>

            {/* Projects */}

            <article className="stat-card">

              <div className="stat-card-top">

                <div className="stat-icon">
                  <Zap size={20} />
                </div>

                <span className="stat-change positive">
                  +12%
                </span>

              </div>

              <div className="stat-value">
                12
              </div>

              <div className="stat-label">
                Active projects
              </div>

            </article>

            {/* AI */}

            <article className="stat-card">

              <div className="stat-card-top">

                <div className="stat-icon ai-stat-icon">
                  <Sparkles
                    size={20}
                  />
                </div>

                <span className="stat-change">
                  AI
                </span>

              </div>

              <div className="stat-value">
                94%
              </div>

              <div className="stat-label">
                AI productivity score
              </div>

            </article>

          </section>

          {/* ==================================================
              MAIN GRID
          =================================================== */}

          <section className="dashboard-grid">

            {/* =================================================
                RECENT CONVERSATIONS
            ================================================== */}

            <article className="dashboard-card conversations-card">

              <div className="card-header">

                <div>

                  <h2>
                    Recent conversations
                  </h2>

                  <p>
                    Stay up to date with
                    your team.
                  </p>

                </div>

                <button
                  type="button"
                  className="card-link"
                  onClick={() =>
                    handleNavigation(
                      "Messages",
                    )
                  }
                >
                  View all
                </button>

              </div>

              <div className="conversation-list">

                {/* Rahul */}

                <div className="conversation-item">

                  <div className="conversation-avatar avatar-purple">
                    R
                  </div>

                  <div className="conversation-content">

                    <div className="conversation-title">

                      <strong>
                        Rahul
                      </strong>

                      <span>
                        10:43 AM
                      </span>

                    </div>

                    <p>
                      The new collaboration
                      dashboard looks
                      amazing.
                    </p>

                    <span className="conversation-channel">
                      # general
                    </span>

                  </div>

                  <span className="unread-badge">
                    2
                  </span>

                </div>

                {/* Priya */}

                <div className="conversation-item">

                  <div className="conversation-avatar avatar-blue">
                    P
                  </div>

                  <div className="conversation-content">

                    <div className="conversation-title">

                      <strong>
                        Priya
                      </strong>

                      <span>
                        10:21 AM
                      </span>

                    </div>

                    <p>
                      I've uploaded the
                      latest design files
                      for review.
                    </p>

                    <span className="conversation-channel">
                      # design
                    </span>

                  </div>

                </div>

                {/* Ankit */}

                <div className="conversation-item">

                  <div className="conversation-avatar avatar-green">
                    A
                  </div>

                  <div className="conversation-content">

                    <div className="conversation-title">

                      <strong>
                        Ankit
                      </strong>

                      <span>
                        09:48 AM
                      </span>

                    </div>

                    <p>
                      Backend deployment
                      completed
                      successfully.
                    </p>

                    <span className="conversation-channel">
                      # engineering
                    </span>

                  </div>

                  <span className="unread-badge">
                    4
                  </span>

                </div>

              </div>

            </article>

            {/* =================================================
                AI ASSISTANT
            ================================================== */}

            <article className="dashboard-card ai-card">

              <div className="ai-card-glow" />

              <div className="ai-card-header">

                <div className="ai-card-icon">
                  <Sparkles size={22} />
                </div>

                <span>
                  AI ASSISTANT
                </span>

              </div>

              <h2>
                Your intelligent
                <br />
                workspace assistant.
              </h2>

              <p>
                Summarize conversations,
                generate ideas, create
                tasks and get answers
                from your workspace.
              </p>

              <button
                type="button"
                className="ai-action-button"
                onClick={() =>
                  handleNavigation(
                    "AI Assistant",
                  )
                }
              >
                <Bot size={17} />

                Open AI Assistant
              </button>

              <div className="ai-suggestions">

                <button
                  type="button"
                  onClick={() =>
                    console.log(
                      "Summarize messages",
                    )
                  }
                >
                  Summarize today's
                  messages
                </button>

                <button
                  type="button"
                  onClick={() =>
                    console.log(
                      "Create project tasks",
                    )
                  }
                >
                  Create project tasks
                </button>

              </div>

            </article>

          </section>

          {/* ==================================================
              PROJECTS
          =================================================== */}

          <section className="dashboard-card projects-card">

            <div className="card-header">

              <div>

                <h2>
                  Active projects
                </h2>

                <p>
                  Track what's currently
                  being built.
                </p>

              </div>

              <button
                type="button"
                className="card-link"
                onClick={() =>
                  console.log(
                    "View projects clicked",
                  )
                }
              >
                View projects
              </button>

            </div>

            <div className="project-list">

              {/* Project 1 */}

              <div className="project-row">

                <div className="project-info">

                  <div className="project-icon">
                    A
                  </div>

                  <div>

                    <strong>
                      AkaSphere Platform
                    </strong>

                    <span>
                      Product development
                    </span>

                  </div>

                </div>

                <div className="project-progress">

                  <div className="progress-label">

                    <span>
                      Progress
                    </span>

                    <strong>
                      78%
                    </strong>

                  </div>

                  <div className="progress-bar">
                    <span
                      style={{
                        width: "78%",
                      }}
                    />
                  </div>

                </div>

                <span className="project-status">
                  On track
                </span>

              </div>

              {/* Project 2 */}

              <div className="project-row">

                <div className="project-info">

                  <div className="project-icon project-icon-ai">
                    <Sparkles
                      size={17}
                    />
                  </div>

                  <div>

                    <strong>
                      AI Assistant
                    </strong>

                    <span>
                      Intelligence features
                    </span>

                  </div>

                </div>

                <div className="project-progress">

                  <div className="progress-label">

                    <span>
                      Progress
                    </span>

                    <strong>
                      54%
                    </strong>

                  </div>

                  <div className="progress-bar">
                    <span
                      style={{
                        width: "54%",
                      }}
                    />
                  </div>

                </div>

                <span className="project-status">
                  In progress
                </span>

              </div>

              {/* Project 3 */}

              <div className="project-row">

                <div className="project-info">

                  <div className="project-icon project-icon-blue">
                    D
                  </div>

                  <div>

                    <strong>
                      Dashboard Redesign
                    </strong>

                    <span>
                      UX & engineering
                    </span>

                  </div>

                </div>

                <div className="project-progress">

                  <div className="progress-label">

                    <span>
                      Progress
                    </span>

                    <strong>
                      91%
                    </strong>

                  </div>

                  <div className="progress-bar">
                    <span
                      style={{
                        width: "91%",
                      }}
                    />
                  </div>

                </div>

                <span className="project-status">
                  Almost done
                </span>

              </div>

            </div>

          </section>

        </main>

      </div>

    </div>
  );
}

export default Dashboard;