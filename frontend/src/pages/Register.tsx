import { useState, type FormEvent } from "react";
import {
  ArrowRight,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  Sparkles,
  User,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

function Register() {
  const navigate = useNavigate();

  const [fullName, setFullName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    setError("");

    const normalizedEmail = email.trim().toLowerCase();
    const normalizedUsername = username.trim().toLowerCase();

    if (
      !normalizedEmail ||
      !normalizedUsername ||
      !password
    ) {
      setError("Please complete all required fields.");
      return;
    }

    try {
      setLoading(true);

      await api.post("/auth/register", {
        full_name: fullName.trim() || null,
        username: normalizedUsername,
        email: normalizedEmail,
        password,
      });

      await api.post("/auth/send-otp", {
        email: normalizedEmail,
      });

      navigate("/verify-otp", {
        replace: true,
        state: {
          email: normalizedEmail,
        },
      });
    } catch (err: any) {
      console.error("Registration failed:", err);

      setError(
        err?.response?.data?.detail ||
          "Unable to create your account. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page register-page">
      <div className="auth-background-glow auth-glow-one" />
      <div className="auth-background-glow auth-glow-two" />

      <div className="auth-orbit auth-orbit-one" />
      <div className="auth-orbit auth-orbit-two" />

      <header className="auth-navbar">
        <Link to="/" className="auth-brand">
          <span className="auth-brand-icon">
            <Sparkles size={20} />
          </span>

          <span>AkaSphere</span>
        </Link>

        <Link
          to="/login"
          className="auth-nav-link"
        >
          Already have an account?
          <span>Sign in</span>
        </Link>
      </header>

      <main className="auth-main">
        <section className="auth-card register-card">
          <div className="auth-card-glow" />

          <div className="auth-logo">
            <div className="logo-mark">
              <Sparkles
                size={19}
                strokeWidth={2.5}
              />
            </div>

            <span>AkaSphere</span>
          </div>

          <div className="auth-heading">
            <div className="auth-eyebrow">
              <span className="auth-eyebrow-dot" />
              CREATE YOUR ACCOUNT
            </div>

            <h1>
              Build something
              <span> extraordinary.</span>
            </h1>

            <p>
              Join AkaSphere and start building
              smarter with your team.
            </p>
          </div>

          {error && (
            <div
              className="auth-error"
              role="alert"
            >
              {error}
            </div>
          )}

          <form
            className="auth-form"
            onSubmit={handleSubmit}
          >
            <div className="auth-field">
              <label htmlFor="register-full-name">
                Full name
              </label>

              <div className="auth-input-wrapper">
                <User size={18} />

                <input
                  id="register-full-name"
                  type="text"
                  placeholder="Akash Das"
                  value={fullName}
                  onChange={(event) =>
                    setFullName(event.target.value)
                  }
                  autoComplete="name"
                  disabled={loading}
                />
              </div>
            </div>

            <div className="auth-field">
              <label htmlFor="register-username">
                Username
              </label>

              <div className="auth-input-wrapper">
                <User size={18} />

                <input
                  id="register-username"
                  type="text"
                  placeholder="akashdas"
                  value={username}
                  onChange={(event) =>
                    setUsername(event.target.value)
                  }
                  autoComplete="username"
                  minLength={3}
                  maxLength={50}
                  pattern="[a-zA-Z0-9_]+"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            <div className="auth-field">
              <label htmlFor="register-email">
                Email address
              </label>

              <div className="auth-input-wrapper">
                <Mail size={18} />

                <input
                  id="register-email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(event) =>
                    setEmail(event.target.value)
                  }
                  autoComplete="email"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            <div className="auth-field">
              <label htmlFor="register-password">
                Password
              </label>

              <div className="auth-input-wrapper">
                <LockKeyhole size={18} />

                <input
                  id="register-password"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Create a password"
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  autoComplete="new-password"
                  minLength={8}
                  maxLength={128}
                  required
                  disabled={loading}
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(
                      (previous) => !previous,
                    )
                  }
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                >
                  {showPassword ? (
                    <EyeOff size={18} />
                  ) : (
                    <Eye size={18} />
                  )}
                </button>
              </div>
            </div>

            <button
              className="auth-submit"
              type="submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="auth-spinner" />
                  Creating account...
                </>
              ) : (
                <>
                  Create account
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          <p className="auth-register">
            Already have an account?{" "}
            <Link to="/login">
              Sign in
            </Link>
          </p>

          <Link
            className="back-home"
            to="/"
          >
            Back to home
          </Link>
        </section>
      </main>
    </div>
  );
}

export default Register;