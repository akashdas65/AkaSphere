import {
  Bell,
  Bot,
  ChevronDown,
  FolderKanban,
  Hash,
  Home,
  LogOut,
  MessageSquare,
  Plus,
  Search,
  Settings,
  Sparkles,
  Users,
  X,
} from "lucide-react";

import {
  useEffect,
  useMemo,
  useState,
  type FormEvent,
} from "react";

import {
  useLocation,
  useNavigate,
} from "react-router-dom";

import api from "../services/api";

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

const channels: Channel[] = [
  { name: "general", unread: 0 },
  { name: "engineering", unread: 4 },
  { name: "design", unread: 2 },
  { name: "projects", unread: 0 },
];

function Dashboard() {
  const navigate = useNavigate();
  const location = useLocation();

  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const [searchQuery, setSearchQuery] = useState("");

  const [notificationsOpen, setNotificationsOpen] =
    useState(false);

  const [profileOpen, setProfileOpen] =
    useState(false);

  const [mobileSidebarOpen, setMobileSidebarOpen] =
    useState(false);

  const [toast, setToast] =
    useState<string | null>(null);

  const showToast = (message: string) => {
    setToast(message);

    window.setTimeout(() => {
      setToast(null);
    }, 2500);
  };

  /*
   * =========================================================
   * LOAD CURRENT USER
   * =========================================================
   */

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
        const response =
          await api.get("/auth/me");

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

  /*
   * =========================================================
   * LOGOUT
   * =========================================================
   */

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
        "Logout failed:",
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

  /*
   * =========================================================
   * USER INFORMATION
   * =========================================================
   */

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

  /*
   * =========================================================
   * ACTIVE PAGE
   * =========================================================
   */

  const activePage = useMemo(() => {
    const path = location.pathname;

    if (path.includes("/messages")) {
      return "Messages";
    }

    if (path.includes("/team")) {
      return "Team";
    }

    if (path.includes("/ai")) {
      return "AI Assistant";
    }

    if (path.includes("/projects")) {
      return "Projects";
    }

    if (path.includes("/settings")) {
      return "Settings";
    }

    if (path.includes("/channels/")) {
      return "Channel";
    }

    return "Overview";
  }, [location.pathname]);

  /*
   * =========================================================
   * NAVIGATION
   * =========================================================
   */

  const navigateTo = (path: string) => {
    setNotificationsOpen(false);
    setProfileOpen(false);
    setMobileSidebarOpen(false);

    navigate(path);
  };

  /*
   * =========================================================
   * SEARCH
   * =========================================================
   */

  const handleSearch = (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    const query =
      searchQuery.trim();

    if (!query) {
      showToast(
        "Type something to search.",
      );
      return;
    }

    showToast(
      `Searching for "${query}"`,
    );
  };

  /*
   * =========================================================
   * CHANNEL
   * =========================================================
   */

  const handleChannelClick = (
    channelName: string,
  ) => {
    navigateTo(
      `/dashboard/channels/${channelName}`,
    );
  };

  /*
   * =========================================================
   * LOADING
   * =========================================================
   */

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

  /*
   * =========================================================
   * DASHBOARD
   * =========================================================
   */

  return (
    <div className="dashboard-page">

      {/* TOAST */}

      {toast && (
        <div className="dashboard-toast">
          <span>{toast}</span>

          <button
            type="button"
            onClick={() =>
              setToast(null)
            }
            aria-label="Close notification"
          >
            <X size={15} />
          </button>
        </div>
      )}

      {/* MOBILE OVERLAY */}

      {mobileSidebarOpen && (
        <button
          type="button"
          className="sidebar-overlay"
          aria-label="Close sidebar"
          onClick={() =>
            setMobileSidebarOpen(false)
          }
        />
      )}

      {/* =====================================================
          SIDEBAR
      ====================================================== */}

      <aside
        className={`dashboard-sidebar ${
          mobileSidebarOpen
            ? "mobile-open"
            : ""
        }`}
      >

        {/* BRAND */}

        <div className="dashboard-brand">
          <div className="dashboard-brand-icon">
            <Sparkles size={19} />
          </div>

          <div>
            <strong>AkaSphere</strong>

            <span>Workspace</span>
          </div>
        </div>

        {/* WORKSPACE */}

        <button
          type="button"
          className="workspace-selector"
          onClick={() =>
            navigateTo("/dashboard")
          }
        >
          <div className="workspace-selector-icon">
            A
          </div>

          <div className="workspace-selector-info">
            <strong>AkaSphere</strong>

            <span>
              Personal workspace
            </span>
          </div>

          <ChevronDown size={16} />
        </button>

        {/* WORKSPACE NAVIGATION */}

        <div className="sidebar-group">

          <span className="sidebar-heading">
            WORKSPACE
          </span>

          {/* OVERVIEW */}

          <button
            type="button"
            className={`sidebar-nav ${
              activePage === "Overview"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigateTo("/dashboard")
            }
          >
            <Home size={18} />

            <span>Overview</span>
          </button>

          {/* MESSAGES */}

          <button
            type="button"
            className={`sidebar-nav ${
              activePage === "Messages"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigateTo(
                "/dashboard/messages",
              )
            }
          >
            <MessageSquare size={18} />

            <span>Messages</span>

            <span className="nav-count">
              6
            </span>
          </button>

          {/* TEAM */}

          <button
            type="button"
            className={`sidebar-nav ${
              activePage === "Team"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigateTo(
                "/dashboard/team",
              )
            }
          >
            <Users size={18} />

            <span>Team</span>
          </button>

          {/* PROJECTS */}

          <button
            type="button"
            className={`sidebar-nav ${
              activePage === "Projects"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigateTo(
                "/dashboard/projects",
              )
            }
          >
            <FolderKanban size={18} />

            <span>Projects</span>
          </button>

          {/* AI */}

          <button
            type="button"
            className={`sidebar-nav ${
              activePage === "AI Assistant"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigateTo(
                "/dashboard/ai",
              )
            }
          >
            <Bot size={18} />

            <span>AI Assistant</span>

            <span className="ai-badge">
              AI
            </span>
          </button>
        </div>

        {/* CHANNELS */}

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
                showToast(
                  "Create channel feature coming next.",
                )
              }
            >
              <Plus size={15} />
            </button>
          </div>

          {channels.map((channel) => (
            <button
              key={channel.name}
              type="button"
              className={`sidebar-channel ${
                location.pathname.includes(
                  `/channels/${channel.name}`,
                )
                  ? "active"
                  : ""
              }`}
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
          ))}
        </div>

        {/* SIDEBAR BOTTOM */}

        <div className="sidebar-bottom">

          {/* SETTINGS */}

          <button
            type="button"
            className={`sidebar-nav ${
              activePage === "Settings"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigateTo(
                "/dashboard/settings",
              )
            }
          >
            <Settings size={18} />

            <span>Settings</span>
          </button>

          {/* LOGOUT */}

          <button
            type="button"
            className="sidebar-nav logout-nav"
            onClick={logout}
          >
            <LogOut size={18} />

            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* =====================================================
          MAIN
      ====================================================== */}

      <div className="dashboard-main">

        {/* TOPBAR */}

        <header className="dashboard-topbar">

          {/* MOBILE MENU */}

          <button
            type="button"
            className="mobile-menu-button"
            onClick={() =>
              setMobileSidebarOpen(true)
            }
            aria-label="Open menu"
          >
            <span />
            <span />
            <span />
          </button>

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

            <kbd>Ctrl K</kbd>
          </form>

          {/* TOPBAR ACTIONS */}

          <div className="topbar-actions">

            {/* NOTIFICATIONS */}

            <div className="topbar-menu">

              <button
                type="button"
                className="topbar-icon"
                aria-label="Notifications"
                onClick={() => {
                  setNotificationsOpen(
                    (previous) =>
                      !previous,
                  );

                  setProfileOpen(false);
                }}
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

            {/* PROFILE */}

            <div className="topbar-menu">

              <button
                type="button"
                className="profile-button"
                onClick={() => {
                  setProfileOpen(
                    (previous) =>
                      !previous,
                  );

                  setNotificationsOpen(false);
                }}
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
                      navigateTo(
                        "/dashboard/settings",
                      )
                    }
                  >
                    <Settings size={16} />
                    Settings
                  </button>

                  <button
                    type="button"
                    onClick={logout}
                  >
                    <LogOut size={16} />
                    Logout
                  </button>

                </div>
              )}
            </div>
          </div>
        </header>

        {/* =====================================================
            CONTENT
        ====================================================== */}

        <main className="dashboard-content">

          {/* OVERVIEW */}

          {activePage === "Overview" && (
            <>

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
                    navigateTo(
                      "/dashboard/projects",
                    )
                  }
                >
                  <Plus size={18} />

                  New project
                </button>

              </section>

              {/* STATS */}

              <section className="stats-grid">

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

                <article className="stat-card">

                  <div className="stat-card-top">

                    <div className="stat-icon">
                      <FolderKanban
                        size={20}
                      />
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

                <article className="stat-card">

                  <div className="stat-card-top">

                    <div className="stat-icon ai-stat-icon">
                      <Sparkles size={20} />
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

              {/* MAIN CARDS */}

              <section className="dashboard-grid">

                {/* CONVERSATIONS */}

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
                        navigateTo(
                          "/dashboard/messages",
                        )
                      }
                    >
                      View all
                    </button>

                  </div>

                  <div className="conversation-list">

                    <button
                      type="button"
                      className="conversation-item"
                      onClick={() =>
                        handleChannelClick(
                          "general",
                        )
                      }
                    >

                      <div className="conversation-avatar avatar-purple">
                        R
                      </div>

                      <div className="conversation-content">

                        <div className="conversation-title">
                          <strong>Rahul</strong>

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

                    </button>

                    <button
                      type="button"
                      className="conversation-item"
                      onClick={() =>
                        handleChannelClick(
                          "design",
                        )
                      }
                    >

                      <div className="conversation-avatar avatar-blue">
                        P
                      </div>

                      <div className="conversation-content">

                        <div className="conversation-title">
                          <strong>Priya</strong>

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

                    </button>

                    <button
                      type="button"
                      className="conversation-item"
                      onClick={() =>
                        handleChannelClick(
                          "engineering",
                        )
                      }
                    >

                      <div className="conversation-avatar avatar-green">
                        A
                      </div>

                      <div className="conversation-content">

                        <div className="conversation-title">
                          <strong>Ankit</strong>

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

                    </button>

                  </div>
                </article>

                {/* AI CARD */}

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
                      navigateTo(
                        "/dashboard/ai",
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
                        showToast(
                          "AI summarization is ready to connect.",
                        )
                      }
                    >
                      Summarize today's
                      messages
                    </button>

                    <button
                      type="button"
                      onClick={() =>
                        showToast(
                          "AI task generation is ready to connect.",
                        )
                      }
                    >
                      Create project tasks
                    </button>

                  </div>
                </article>

              </section>

              {/* PROJECTS */}

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
                      navigateTo(
                        "/dashboard/projects",
                      )
                    }
                  >
                    View projects
                  </button>

                </div>

                <div className="project-list">

                  <button
                    type="button"
                    className="project-row"
                    onClick={() =>
                      navigateTo(
                        "/dashboard/projects",
                      )
                    }
                  >

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

                  </button>

                  <button
                    type="button"
                    className="project-row"
                    onClick={() =>
                      navigateTo(
                        "/dashboard/ai",
                      )
                    }
                  >

                    <div className="project-info">

                      <div className="project-icon project-icon-ai">
                        <Sparkles size={17} />
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

                  </button>

                  <button
                    type="button"
                    className="project-row"
                    onClick={() =>
                      navigateTo(
                        "/dashboard/projects",
                      )
                    }
                  >

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

                  </button>

                </div>
              </section>

            </>
          )}

          {/* OTHER PAGES */}

          {activePage !== "Overview" &&
            activePage !== "Channel" && (
              <section className="simple-dashboard-page">

                <span className="dashboard-eyebrow">
                  AKASPHERE
                </span>

                <h1>
                  {activePage}
                </h1>

                <p>
                  {activePage === "Messages" &&
                    "Your team conversations will appear here."}

                  {activePage === "Team" &&
                    "Manage your AkaSphere team members here."}

                  {activePage === "Projects" &&
                    "Create and manage your projects here."}

                  {activePage === "AI Assistant" &&
                    "Your AI-powered workspace assistant will live here."}

                  {activePage === "Settings" &&
                    "Manage your workspace and account settings here."}
                </p>

                <button
                  type="button"
                  className="dashboard-primary-button"
                  onClick={() =>
                    navigateTo("/dashboard")
                  }
                >
                  <Home size={18} />

                  Back to Overview
                </button>

              </section>
            )}

          {/* CHANNEL PAGE */}

          {activePage === "Channel" && (
            <section className="simple-dashboard-page">

              <span className="dashboard-eyebrow">
                CHANNEL
              </span>

              <h1>
                #
                {
                  location.pathname.split(
                    "/channels/",
                  )[1]
                }
              </h1>

              <p>
                Channel messages will appear
                here. The channel navigation
                is working correctly.
              </p>

              <button
                type="button"
                className="dashboard-primary-button"
                onClick={() =>
                  navigateTo(
                    "/dashboard/messages",
                  )
                }
              >
                <MessageSquare size={18} />

                Open Messages
              </button>

            </section>
          )}

        </main>
      </div>
    </div>
  );
}

export default Dashboard;