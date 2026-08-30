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
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    setError("");

    const normalizedEmail = email.trim().toLowerCase();
    const normalizedUsername = username.trim().toLowerCase();

    if (!normalizedEmail || !normalizedUsername || !password) {
      setError("Please complete all required fields.");
      return;
    }

    setLoading(true);

    try {
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
        <Link to="/" className="auth-logo">
          <div className="logo-mark">
            <Sparkles size={19} strokeWidth={2.5} />
          </div>
          <span>AkaSphere</span>
        </Link>

        <div className="auth-heading">
          <h1>Create your account</h1>
          <p>Start building smarter with your team.</p>
        </div>

        {error && (
          <div className="auth-error" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <label htmlFor="full-name">Full name</label>

          <div className="input-wrapper">
            <User size={18} />

            <input
              id="full-name"
              type="text"
              placeholder="Akash Das"
              value={fullName}
              onChange={(event) => setFullName(event.target.value)}
              autoComplete="name"
              disabled={loading}
            />
          </div>

          <label htmlFor="username">Username</label>

          <div className="input-wrapper">
            <User size={18} />

            <input
              id="username"
              type="text"
              placeholder="akashdas"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              autoComplete="username"
              minLength={3}
              maxLength={50}
              pattern="[a-zA-Z0-9_]+"
              required
              disabled={loading}
            />
          </div>

          <label htmlFor="email">Email</label>

          <div className="input-wrapper">
            <Mail size={18} />

            <input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              autoComplete="email"
              required
              disabled={loading}
            />
          </div>

          <label htmlFor="password">Password</label>

          <div className="input-wrapper">
            <LockKeyhole size={18} />

            <input
              id="password"
              type="password"
              placeholder="Create a password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              autoComplete="new-password"
              minLength={8}
              maxLength={128}
              required
              disabled={loading}
            />
          </div>

          <button
            className="btn btn-primary auth-submit"
            type="submit"
            disabled={loading}
          >
            {loading ? (
              "Creating account..."
            ) : (
              <>
                Continue
                <ArrowRight size={17} />
              </>
            )}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account?{" "}
          <Link to="/login">Sign in</Link>
        </p>

        <Link className="back-home" to="/">
          Back to home
        </Link>
      </div>
    </div>
  );
}

export default Register;
