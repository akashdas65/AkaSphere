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

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    setError("");

    if (!email.trim() || !password) {
      setError("Please enter your email and password.");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post("/auth/login", {
        email: email.trim(),
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
        setError("Please enter a valid email and password.");
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
        <Link
          to="/"
          className="auth-brand"
        >
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
          <div className="auth-card-glow" />

          <div className="auth-icon">
            <Sparkles size={25} />
          </div>

          <div className="auth-heading">
            <span className="auth-eyebrow">
              WELCOME BACK
            </span>

            <h1>Sign in to AkaSphere</h1>

            <p>
              Continue to your workspace and
              collaborate with your team.
            </p>
          </div>

          {error && (
            <div className="auth-error">
              {error}
            </div>
          )}

          <form
            className="auth-form"
            onSubmit={handleSubmit}
          >
            <div className="auth-field">
              <label htmlFor="email">
                Email
              </label>

              <div className="auth-input-wrapper">
                <Mail size={18} />

                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(event) =>
                    setEmail(event.target.value)
                  }
                  placeholder="you@example.com"
                  autoComplete="email"
                />
              </div>
            </div>

            <div className="auth-field">
              <div className="auth-label-row">
                <label htmlFor="password">
                  Password
                </label>

                <button
                  type="button"
                  className="forgot-button"
                  onClick={() =>
                    navigate("/verify-otp")
                  }
                >
                  Forgot password?
                </button>
              </div>

              <div className="auth-input-wrapper">
                <Lock size={18} />

                <input
                  id="password"
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