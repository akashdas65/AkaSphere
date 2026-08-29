import { useState } from "react";
import {
  ArrowRight,
  CheckCircle2,
  Code2,
  Menu,
  MessageSquare,
  ShieldCheck,
  Sparkles,
  Users,
  X,
  Zap,
} from "lucide-react";
import "./App.css";

function App() {
  const [menuOpen, setMenuOpen] = useState(false);

  const features = [
    {
      icon: MessageSquare,
      title: "Real-time Collaboration",
      description:
        "Communicate with your team instantly through channels, messaging and live collaboration.",
    },
    {
      icon: Sparkles,
      title: "AI-Powered Workspace",
      description:
        "Use intelligent AI assistance to summarize conversations, generate ideas and improve productivity.",
    },
    {
      icon: ShieldCheck,
      title: "Secure by Design",
      description:
        "JWT authentication, protected APIs and production-ready security architecture.",
    },
    {
      icon: Users,
      title: "Team Management",
      description:
        "Create teams, manage members and organize your workspace from one place.",
    },
    {
      icon: Zap,
      title: "Fast & Scalable",
      description:
        "Built with FastAPI, PostgreSQL, Redis and Docker for reliable performance.",
    },
    {
      icon: Code2,
      title: "Developer Friendly",
      description:
        "Modern APIs, clean architecture, Docker support and an extensible codebase.",
    },
  ];

  const closeMenu = () => {
    setMenuOpen(false);
  };

  return (
    <div className="app">
      {/* ==================== NAVBAR ==================== */}

      <header className="navbar">
        <div className="nav-container">
          <a href="#home" className="logo" onClick={closeMenu}>
            <div className="logo-mark">
              <Sparkles size={19} strokeWidth={2.5} />
            </div>

            <span>AkaSphere</span>
          </a>

          <nav className={`nav-links ${menuOpen ? "open" : ""}`}>
            <a href="#home" onClick={closeMenu}>
              Home
            </a>

            <a href="#features" onClick={closeMenu}>
              Features
            </a>

            <a href="#about" onClick={closeMenu}>
              About
            </a>

            <a href="#contact" onClick={closeMenu}>
              Contact
            </a>

            <div className="mobile-actions">
              <button className="btn btn-secondary" type="button">
                Log in
              </button>

              <button className="btn btn-primary" type="button">
                Get Started
              </button>
            </div>
          </nav>

          <div className="desktop-actions">
            <button className="btn btn-secondary" type="button">
              Log in
            </button>

            <button className="btn btn-primary" type="button">
              Get Started
              <ArrowRight size={16} />
            </button>
          </div>

          <button
            className="menu-button"
            type="button"
            onClick={() => setMenuOpen((open) => !open)}
            aria-label="Toggle navigation menu"
            aria-expanded={menuOpen}
          >
            {menuOpen ? <X size={25} /> : <Menu size={25} />}
          </button>
        </div>
      </header>

      <main>
        {/* ==================== HERO ==================== */}

        <section id="home" className="hero-section">
          <div className="hero-background" />

          <div className="hero-container">
            <div className="hero-badge">
              <span className="badge-dot" />
              AI-powered collaboration platform
            </div>

            <h1>
              Work together.
              <br />
              <span>Build smarter.</span>
            </h1>

            <p className="hero-description">
              AkaSphere brings communication, collaboration and AI-powered
              productivity into one modern workspace built for ambitious teams.
            </p>

            <div className="hero-actions">
              <button className="btn btn-primary btn-large" type="button">
                Start Building
                <ArrowRight size={19} />
              </button>

              <button className="btn btn-outline btn-large" type="button">
                <Code2 size={18} />
                Explore Platform
              </button>
            </div>

            <div className="hero-trust">
              <div className="trust-item">
                <CheckCircle2 size={17} />
                Production-ready architecture
              </div>

              <div className="trust-item">
                <CheckCircle2 size={17} />
                Secure authentication
              </div>

              <div className="trust-item">
                <CheckCircle2 size={17} />
                Dockerized infrastructure
              </div>
            </div>

            {/* ==================== DASHBOARD PREVIEW ==================== */}

            <div className="dashboard-wrapper">
              <div className="dashboard-glow" />

              <div className="dashboard">
                <div className="dashboard-topbar">
                  <div className="window-controls">
                    <span />
                    <span />
                    <span />
                  </div>

                  <div className="dashboard-title">
                    AkaSphere Workspace
                  </div>

                  <div className="status-indicator">
                    <span />
                    Live
                  </div>
                </div>

                <div className="dashboard-content">
                  {/* Sidebar */}

                  <aside className="dashboard-sidebar">
                    <div className="workspace-name">
                      <div className="workspace-icon">A</div>

                      <div>
                        <strong>AkaSphere</strong>
                        <small>Workspace</small>
                      </div>
                    </div>

                    <div className="sidebar-section">
                      <span className="sidebar-label">WORKSPACE</span>

                      <div className="sidebar-item active">
                        <MessageSquare size={15} />
                        General
                      </div>

                      <div className="sidebar-item">
                        <Users size={15} />
                        Team
                      </div>

                      <div className="sidebar-item">
                        <Sparkles size={15} />
                        AI Assistant
                      </div>
                    </div>

                    <div className="sidebar-section">
                      <span className="sidebar-label">CHANNELS</span>

                      <div className="sidebar-item">
                        # engineering
                      </div>

                      <div className="sidebar-item">
                        # design
                      </div>

                      <div className="sidebar-item">
                        # projects
                      </div>
                    </div>
                  </aside>

                  {/* Main Chat */}

                  <div className="dashboard-main">
                    <div className="chat-header">
                      <div>
                        <h3># General</h3>
                        <p>Team communication</p>
                      </div>

                      <div className="online-users">
                        <span />
                        8 online
                      </div>
                    </div>

                    <div className="messages">
                      <div className="message">
                        <div className="avatar avatar-purple">A</div>

                        <div className="message-body">
                          <div className="message-meta">
                            <strong>Akash</strong>
                            <span>10:42 AM</span>
                          </div>

                          <p>
                            Welcome to the AkaSphere workspace! 🚀
                          </p>
                        </div>
                      </div>

                      <div className="message">
                        <div className="avatar avatar-blue">R</div>

                        <div className="message-body">
                          <div className="message-meta">
                            <strong>Rahul</strong>
                            <span>10:43 AM</span>
                          </div>

                          <p>
                            The new collaboration dashboard looks amazing.
                          </p>
                        </div>
                      </div>

                      <div className="ai-message">
                        <div className="ai-icon">
                          <Sparkles size={15} />
                        </div>

                        <div>
                          <div className="ai-title">
                            AI Assistant
                          </div>

                          <p>
                            I can summarize your conversation, create tasks
                            and help your team move faster.
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="chat-input">
                      <span>Message #general...</span>

                      <button type="button" aria-label="Send message">
                        <ArrowRight size={17} />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ==================== FEATURES ==================== */}

        <section id="features" className="features-section">
          <div className="section-container">
            <div className="section-heading">
              <div className="section-badge">
                <Sparkles size={15} />
                Powerful by default
              </div>

              <h2>
                Everything your team needs
                <br />
                <span>in one workspace.</span>
              </h2>

              <p>
                A modern collaboration platform designed with scalable
                engineering principles from the ground up.
              </p>
            </div>

            <div className="features-grid">
              {features.map((feature) => {
                const Icon = feature.icon;

                return (
                  <article
                    className="feature-card"
                    key={feature.title}
                  >
                    <div className="feature-icon">
                      <Icon size={22} />
                    </div>

                    <h3>{feature.title}</h3>

                    <p>{feature.description}</p>

                    <a href="#about">
                      Learn more
                      <ArrowRight size={15} />
                    </a>
                  </article>
                );
              })}
            </div>
          </div>
        </section>

        {/* ==================== ABOUT ==================== */}

        <section id="about" className="about-section">
          <div className="section-container">
            <div className="about-card">
              <div className="about-content">
                <div className="section-badge">
                  <Code2 size={15} />
                  Built for developers
                </div>

                <h2>
                  Engineering-first.
                  <br />
                  <span>Built to scale.</span>
                </h2>

                <p>
                  AkaSphere combines a modern React frontend with a FastAPI
                  backend, PostgreSQL database, Redis and Docker-based
                  infrastructure.
                </p>

                <div className="tech-list">
                  <div>
                    <CheckCircle2 size={17} />
                    FastAPI REST APIs
                  </div>

                  <div>
                    <CheckCircle2 size={17} />
                    PostgreSQL + SQLAlchemy
                  </div>

                  <div>
                    <CheckCircle2 size={17} />
                    Redis-powered services
                  </div>

                  <div>
                    <CheckCircle2 size={17} />
                    Docker & Nginx
                  </div>
                </div>
              </div>

              <div className="architecture">
                <div className="architecture-card">
                  <span>CLIENT</span>
                  <strong>React + TypeScript</strong>
                </div>

                <ArrowRight
                  className="architecture-arrow"
                  size={20}
                />

                <div className="architecture-card highlight">
                  <span>API</span>
                  <strong>FastAPI</strong>
                </div>

                <ArrowRight
                  className="architecture-arrow"
                  size={20}
                />

                <div className="architecture-card">
                  <span>DATA</span>
                  <strong>PostgreSQL</strong>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ==================== CTA ==================== */}

        <section id="contact" className="cta-section">
          <div className="cta-container">
            <div className="cta-icon">
              <Sparkles size={25} />
            </div>

            <h2>
              Ready to build something
              <br />
              <span>extraordinary?</span>
            </h2>

            <p>
              Start your journey with AkaSphere and bring your team,
              technology and ideas together.
            </p>

            <button className="btn btn-primary btn-large" type="button">
              Get Started
              <ArrowRight size={19} />
            </button>
          </div>
        </section>
      </main>

      {/* ==================== FOOTER ==================== */}

      <footer className="footer">
        <div className="footer-container">
          <div className="footer-brand">
            <div className="logo">
              <div className="logo-mark">
                <Sparkles size={17} />
              </div>

              <span>AkaSphere</span>
            </div>

            <p>
              Intelligent collaboration for modern teams.
            </p>
          </div>

          <div className="footer-links">
            <a href="#home">Home</a>
            <a href="#features">Features</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
          </div>

          <div className="footer-bottom">
            <span>© 2026 AkaSphere. All rights reserved.</span>

            <span className="built-with">
              Built with <Zap size={13} /> modern technology
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;