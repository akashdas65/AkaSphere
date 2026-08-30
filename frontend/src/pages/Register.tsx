import { useState, type FormEvent } from "react";
import {
  ArrowRight,
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
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await api.post("/auth/register", {
        full_name: fullName,
        email,
        password,
      });

      navigate("/login");
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          "Unable to create your account. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">
          <div className="logo-mark">
            <Sparkles size={19} />
          </div>

          <span>AkaSphere</span>
        </div>

        <div className="auth-heading">
          <h1>Create your account</h1>

          <p>
            Start building smarter with your team.
          </p>
        </div>

        {error && (
          <div className="auth-error">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <label htmlFor="full-name">
            Full name
          </label>

          <div className="input-wrapper">
            <User size={18} />

            <input
              id="full-name"
              type="text"
              placeholder="Akash Das"
              value={fullName}
              onChange={(event) =>
                setFullName(event.target.value)
              }
              required
            />
          </div>

          <label htmlFor="email">
            Email
          </label>

          <div className="input-wrapper">
            <Mail size={18} />

            <input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              required
            />
          </div>

          <label htmlFor="password">
            Password
          </label>

          <div className="input-wrapper">
            <LockKeyhole size={18} />

            <input
              id="password"
              type="password"
              placeholder="Create a password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
              minLength={8}
            />
          </div>

          <button
            className="btn btn-primary auth-submit"
            type="submit"
            disabled={loading}
          >
            {loading ? "Creating account..." : "Create account"}

            {!loading && <ArrowRight size={17} />}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account?{" "}
          <Link to="/login">
            Sign in
          </Link>
        </p>

        <Link className="back-home" to="/">
          ← Back to home
        </Link>
      </div>
    </div>
  );
}

export default Register;