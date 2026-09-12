import { useState, type FormEvent } from "react";
import {
  ArrowRight,
  Mail,
  Sparkles,
} from "lucide-react";
import {
  Link,
  useNavigate,
} from "react-router-dom";
import api from "../services/api";

function ForgotPassword() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    setError("");

    const normalizedEmail =
      email.trim().toLowerCase();

    if (!normalizedEmail) {
      setError("Please enter your email address.");
      return;
    }

    try {
      setLoading(true);

      await api.post(
        "/auth/forgot-password",
        {
          email: normalizedEmail,
        },
      );

      navigate("/verify-otp", {
        replace: true,
        state: {
          email: normalizedEmail,
          purpose: "password-reset",
        },
      });
    } catch (err: any) {
      console.error(
        "Forgot password failed:",
        err,
      );

      setError(
        err?.response?.data?.detail ||
          "Unable to process your request. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page forgot-password-page">
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
          to="/login"
          className="auth-back-home"
        >
          ← Back to sign in
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
            <h1>Forgot your password?</h1>

            <p>
              Enter your email and we'll send you
              a verification code.
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
            <label htmlFor="forgot-email">
              Email
            </label>

            <div className="auth-input-wrapper">
              <Mail size={18} />

              <input
                id="forgot-email"
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

            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="auth-spinner" />
                  Sending code...
                </>
              ) : (
                <>
                  Send verification code
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          <p className="auth-register">
            Remember your password?{" "}
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

export default ForgotPassword;