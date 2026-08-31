import {
  ArrowRight,
  Bot,
  CheckCircle2,
  Code2,
  MessageSquare,
  Sparkles,
  Users,
  Zap,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      {/* =====================================================
          NAVBAR
      ====================================================== */}

      <header className="landing-navbar">
        <button
          type="button"
          className="landing-logo"
          onClick={() => navigate("/")}
        >
          <span className="landing-logo-icon">
            <Sparkles size={21} />
          </span>

          <span>AkaSphere</span>
        </button>

        <nav className="landing-nav-links">
          <a href="#home">Home</a>
          <a href="#features">Features</a>
          <a href="#about">About</a>
          <a href="#contact">Contact</a>
        </nav>

        <div className="landing-nav-actions">
          <button
            type="button"
            className="landing-login-button"
            onClick={() => navigate("/login")}
          >
            Log in
          </button>

          <button
            type="button"
            className="landing-primary-button"
            onClick={() => navigate("/register")}
          >
            Get Started
            <ArrowRight size={17} />
          </button>
        </div>
      </header>

      {/* =====================================================
          HERO
      ====================================================== */}

      <main>
        <section
          id="home"
          className="landing-hero"
        >
          <div className="hero-glow hero-glow-one" />
          <div className="hero-glow hero-glow-two" />

          <div className="hero-content">
            <div className="hero-badge">
              <span className="hero-badge-dot" />
              AI-powered collaboration platform
            </div>

            <h1>
              Work together.
              <br />
              <span>Build smarter.</span>
            </h1>

            <p>
              AkaSphere brings communication,
              collaboration and AI-powered productivity
              into one modern workspace built for
              ambitious teams.
            </p>

            <div className="hero-actions">
              <button
                type="button"
                className="hero-primary-button"
                onClick={() => navigate("/register")}
              >
                Start Building
                <ArrowRight size={18} />
              </button>

              <button
                type="button"
                className="hero-secondary-button"
                onClick={() => {
                  document
                    .getElementById("features")
                    ?.scrollIntoView({
                      behavior: "smooth",
                    });
                }}
              >
                <Code2 size={17} />
                Explore Platform
              </button>
            </div>

            <div className="hero-trust">
              <span>
                <CheckCircle2 size={16} />
                Production-ready architecture
              </span>

              <span>
                <CheckCircle2 size={16} />
                Secure authentication
              </span>

              <span>
                <CheckCircle2 size={16} />
                Dockerized infrastructure
              </span>
            </div>
          </div>

          {/* =================================================
              PRODUCT PREVIEW
          ================================================= */}

          <div className="hero-preview">
            <div className="preview-top">
              <div className="preview-dots">
                <span />
                <span />
                <span />
              </div>

              <span className="preview-title">
                AkaSphere Workspace
              </span>

              <span className="preview-live">
                <span />
                Live
              </span>
            </div>

            <div className="preview-body">
              <aside className="preview-sidebar">
                <div className="preview-brand">
                  <div className="preview-brand-icon">
                    A
                  </div>

                  <div>
                    <strong>AkaSphere</strong>
                    <span>Workspace</span>
                  </div>
                </div>

                <div className="preview-section-title">
                  WORKSPACE
                </div>

                <div className="preview-menu active">
                  <MessageSquare size={15} />
                  General
                </div>

                <div className="preview-menu">
                  <Users size={15} />
                  Team
                </div>

                <div className="preview-menu">
                  <Bot size={15} />
                  AI Assistant
                </div>

                <div className="preview-section-title">
                  CHANNELS
                </div>

                <div className="preview-channel">
                  # engineering
                </div>

                <div className="preview-channel">
                  # design
                </div>

                <div className="preview-channel">
                  # projects
                </div>
              </aside>

              <div className="preview-main">
                <div className="preview-main-heading">
                  <div>
                    <span>YOUR WORKSPACE</span>

                    <h3>
                      Good morning, Akash 👋
                    </h3>

                    <p>
                      Here's what's happening
                      across your workspace.
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={() =>
                      navigate("/register")
                    }
                  >
                    <Zap size={15} />
                    New project
                  </button>
                </div>

                <div className="preview-stats">
                  <div>
                    <MessageSquare size={17} />
                    <strong>128</strong>
                    <span>Messages</span>
                  </div>

                  <div>
                    <Users size={17} />
                    <strong>24</strong>
                    <span>Team members</span>
                  </div>

                  <div>
                    <Zap size={17} />
                    <strong>12</strong>
                    <span>Projects</span>
                  </div>

                  <div>
                    <Sparkles size={17} />
                    <strong>94%</strong>
                    <span>AI productivity</span>
                  </div>
                </div>

                <div className="preview-cards">
                  <div className="preview-card">
                    <span>RECENT CONVERSATIONS</span>

                    <div className="preview-message">
                      <div>R</div>
                      <p>
                        The new collaboration
                        dashboard looks amazing.
                      </p>
                    </div>

                    <div className="preview-message">
                      <div>P</div>
                      <p>
                        I've uploaded the latest
                        design files.
                      </p>
                    </div>
                  </div>

                  <div className="preview-ai">
                    <Sparkles size={22} />

                    <span>AI ASSISTANT</span>

                    <h4>
                      Your intelligent
                      workspace assistant.
                    </h4>

                    <p>
                      Summarize conversations,
                      generate ideas and get
                      answers from your workspace.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* =====================================================
            FEATURES
        ====================================================== */}

        <section
          id="features"
          className="landing-section"
        >
          <div className="section-heading">
            <span>FEATURES</span>

            <h2>
              Everything your team
              <br />
              needs to move faster.
            </h2>

            <p>
              A unified workspace designed for
              communication, productivity and
              intelligent collaboration.
            </p>
          </div>

          <div className="feature-grid">
            <article className="feature-card">
              <div className="feature-icon">
                <MessageSquare size={22} />
              </div>

              <h3>Team Communication</h3>

              <p>
                Organize conversations into channels
                and keep your team aligned.
              </p>
            </article>

            <article className="feature-card">
              <div className="feature-icon">
                <Bot size={22} />
              </div>

              <h3>AI Assistant</h3>

              <p>
                Turn conversations into summaries,
                ideas, tasks and useful answers.
              </p>
            </article>

            <article className="feature-card">
              <div className="feature-icon">
                <Users size={22} />
              </div>

              <h3>Team Collaboration</h3>

              <p>
                Manage your workspace, members,
                projects and permissions.
              </p>
            </article>

            <article className="feature-card">
              <div className="feature-icon">
                <Zap size={22} />
              </div>

              <h3>Production Ready</h3>

              <p>
                Built with modern backend,
                frontend, database and Docker
                infrastructure.
              </p>
            </article>
          </div>
        </section>

        {/* =====================================================
            ABOUT
        ====================================================== */}

        <section
          id="about"
          className="landing-about"
        >
          <div>
            <span>ABOUT AKASPHERE</span>

            <h2>
              One workspace.
              <br />
              Infinite possibilities.
            </h2>
          </div>

          <p>
            AkaSphere is designed as a modern
            collaboration platform where teams can
            communicate, manage projects and use AI
            without switching between multiple tools.
          </p>
        </section>

        {/* =====================================================
            CTA
        ====================================================== */}

        <section
          id="contact"
          className="landing-cta"
        >
          <div>
            <span>
              <Sparkles size={17} />
              READY TO BUILD?
            </span>

            <h2>
              Build your workspace
              <br />
              with AkaSphere.
            </h2>

            <p>
              Create your account and start
              collaborating.
            </p>

            <button
              type="button"
              onClick={() => navigate("/register")}
            >
              Get Started
              <ArrowRight size={18} />
            </button>
          </div>
        </section>
      </main>

      {/* =====================================================
          FOOTER
      ====================================================== */}

      <footer className="landing-footer">
        <div>
          <strong>AkaSphere</strong>

          <span>
            AI-powered collaboration platform.
          </span>
        </div>

        <span>
          © {new Date().getFullYear()} AkaSphere
        </span>
      </footer>
    </div>
  );
}

export default LandingPage;