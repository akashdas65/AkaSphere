import { useState } from "react";
import type { FormEvent } from "react";
import {
  ArrowRight,
  Eye,
  EyeOff,
  Lock,
  Mail,
  Sparkles,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

function Login() {
  const navigate = useNavigate();

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

    if (!email.trim() || !password) {
      setError("Please enter your email and password.");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post("/auth/login", {
        email: email.trim().toLowerCase(),
        password,
      });

      const {
        access_token,
        refresh_token,
      } = response.data;

      localStorage.setItem(
        "access_token",
        access_token,
      );

      localStorage.setItem(
        "refresh_token",
        refresh_token,
      );

      navigate("/dashboard", {
        replace: true,
      });
    } catch (error: any) {
      console.error("Login failed:", error);

      const status = error?.response?.status;

      if (status === 401) {
        setError("Invalid email or password.");
      } else if (status === 422) {
        setError(
          "Please enter a valid email and password.",
        );
      } else {
        setError(
          "Unable to sign in. Please try again.",
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-background-glow auth-glow-one" />
      <div className="auth-background-glow auth-glow-two" />

      <header className="auth-navbar">
        <Link to="/" className="auth-brand">
          <span className="auth-brand-icon">
            <Sparkles size={20} />
          </span>

          <span>AkaSphere</span>
        </Link>

        <Link
          to="/"
          className="auth-back-home"
        >
          ← Back to home
        </Link>
      </header>

      <main className="auth-main">
        <section className="auth-card">
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
            <h1>Welcome back</h1>

            <p>
              Sign in to continue to your workspace.
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

          <form onSubmit={handleSubmit}>
            <label htmlFor="login-email">
              Email
            </label>

            <div className="auth-input-wrapper">
              <Mail size={18} />

              <input
                id="login-email"
                type="email"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                placeholder="you@example.com"
                autoComplete="email"
                disabled={loading}
                required
              />
            </div>

            <div className="auth-password-label">
              <label htmlFor="login-password">
                Password
              </label>

              <Link to="/forgot-password">
                Forgot password?
              </Link>
            </div>

            <div className="auth-input-wrapper">
              <Lock size={18} />

              <input
                id="login-password"
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                value={password}
                onChange={(event) =>
                  setPassword(event.target.value)
                }
                placeholder="Enter your password"
                autoComplete="current-password"
                disabled={loading}
                required
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

            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="auth-spinner" />
                  Signing in...
                </>
              ) : (
                <>
                  Sign in
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          <div className="auth-divider">
            <span />
            <p>OR</p>
            <span />
          </div>

          <p className="auth-register">
            Don't have an account?{" "}
            <Link to="/register">
              Create one
            </Link>
          </p>
        </section>
      </main>
    </div>
  );
}

export default Login;