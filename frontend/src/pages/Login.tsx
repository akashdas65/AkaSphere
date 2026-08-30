import { useState, type FormEvent } from "react";
import {
  ArrowLeft,
  ArrowRight,
  LockKeyhole,
  Mail,
  Sparkles,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    setError("");

    const normalizedEmail = email.trim().toLowerCase();

    if (!normalizedEmail || !password) {
      setError("Please enter your email and password.");
      return;
    }

    setLoading(true);

    try {
      const response = await api.post("/auth/login", {
        email: normalizedEmail,
        password,
      });

      const {
        access_token,
        refresh_token,
      } = response.data;

      if (!access_token || !refresh_token) {
        throw new Error("Invalid authentication response.");
      }

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
    } catch (error: unknown) {
      if (
        typeof error === "object" &&
        error !== null &&
        "response" in error
      ) {
        const axiosError = error as {
          response?: {
            data?: {
              detail?: string;
            };
          };
        };

        setError(
          axiosError.response?.data?.detail ||
            "Invalid email or password.",
        );
      } else {
        setError(
          "Unable to connect to the server. Please try again.",
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">

        {/* Logo */}
        <Link
          to="/"
          className="auth-logo"
        >
          <div className="logo-mark">
            <Sparkles
              size={19}
              strokeWidth={2.5}
            />
          </div>

          <span>AkaSphere</span>
        </Link>

        {/* Heading */}
        <div className="auth-heading">
          <h1>Welcome back</h1>

          <p>
            Sign in to continue to your workspace.
          </p>
        </div>

        {/* Error */}
        {error && (
          <div
            className="auth-error"
            role="alert"
          >
            {error}
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit}>

          {/* Email */}
          <label htmlFor="email">
            Email
          </label>

          <div className="input-wrapper">
            <Mail size={18} />

            <input
              id="email"
              name="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              autoComplete="email"
              disabled={loading}
              required
            />
          </div>

          {/* Password */}
          <label htmlFor="password">
            Password
          </label>

          <div className="input-wrapper">
            <LockKeyhole size={18} />

            <input
              id="password"
              name="password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              autoComplete="current-password"
              disabled={loading}
              required
            />
          </div>

          {/* Submit */}
          <button
            className="btn btn-primary auth-submit"
            type="submit"
            disabled={loading}
          >
            {loading ? (
              "Signing in..."
            ) : (
              <>
                Sign in
                <ArrowRight size={17} />
              </>
            )}
          </button>
        </form>

        {/* Register */}
        <p className="auth-footer">
          Don't have an account?{" "}
          <Link to="/register">
            Create one
          </Link>
        </p>

        {/* Back */}
        <Link
          className="back-home"
          to="/"
        >
          <ArrowLeft size={15} />
          Back to home
        </Link>

      </div>
    </div>
  );
}

export default Login;