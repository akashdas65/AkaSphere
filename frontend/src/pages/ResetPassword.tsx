import { useState, type FormEvent } from "react";
import {
  ArrowRight,
  Eye,
  EyeOff,
  Lock,
  Sparkles,
} from "lucide-react";
import {
  Link,
  useLocation,
  useNavigate,
} from "react-router-dom";
import api from "../services/api";

type ResetPasswordState = {
  email?: string;
  otp?: string;
};

function ResetPassword() {
  const navigate = useNavigate();
  const location = useLocation();

  const state =
    (location.state as ResetPasswordState | null) ||
    {};

  const email = state.email || "";
  const otp = state.otp || "";

  const [password, setPassword] =
    useState("");

  const [confirmPassword, setConfirmPassword] =
    useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const [
    showConfirmPassword,
    setShowConfirmPassword,
  ] = useState(false);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    setError("");

    if (!email || !otp) {
      navigate(
        "/forgot-password",
        { replace: true },
      );
      return;
    }

    if (password.length < 8) {
      setError(
        "Password must be at least 8 characters.",
      );
      return;
    }

    if (password !== confirmPassword) {
      setError(
        "Passwords do not match.",
      );
      return;
    }

    try {
      setLoading(true);

      await api.post(
        "/auth/reset-password",
        {
          email,
          otp,
          new_password: password,
        },
      );

      navigate("/login", {
        replace: true,
        state: {
          passwordReset: true,
          email,
        },
      });
    } catch (err: any) {
      console.error(
        "Password reset failed:",
        err,
      );

      setError(
        err?.response?.data?.detail ||
          "Unable to reset your password. Please try again.",
      );
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
          to="/login"
          className="auth-back-home"
        >
          ← Back to sign in
        </Link>
      </header>

      <main className="auth-main">
        <section className="auth-card">
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

          <div className="auth-heading">
            <h1>Reset your password</h1>

            <p>
              Create a new secure password
              for your AkaSphere account.
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
            <label htmlFor="new-password">
              New password
            </label>

            <div className="auth-input-wrapper">
              <Lock size={18} />

              <input
                id="new-password"
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                value={password}
                onChange={(event) =>
                  setPassword(
                    event.target.value,
                  )
                }
                placeholder="Create a new password"
                autoComplete="new-password"
                minLength={8}
                maxLength={128}
                disabled={loading}
                required
              />

              <button
                type="button"
                className="password-toggle"
                onClick={() =>
                  setShowPassword(
                    (previous) =>
                      !previous,
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

            <label htmlFor="confirm-password">
              Confirm password
            </label>

            <div className="auth-input-wrapper">
              <Lock size={18} />

              <input
                id="confirm-password"
                type={
                  showConfirmPassword
                    ? "text"
                    : "password"
                }
                value={confirmPassword}
                onChange={(event) =>
                  setConfirmPassword(
                    event.target.value,
                  )
                }
                placeholder="Confirm your password"
                autoComplete="new-password"
                minLength={8}
                maxLength={128}
                disabled={loading}
                required
              />

              <button
                type="button"
                className="password-toggle"
                onClick={() =>
                  setShowConfirmPassword(
                    (previous) =>
                      !previous,
                  )
                }
                aria-label={
                  showConfirmPassword
                    ? "Hide password"
                    : "Show password"
                }
              >
                {showConfirmPassword ? (
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
                  Resetting password...
                </>
              ) : (
                <>
                  Reset password
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
        </section>
      </main>
    </div>
  );
}

export default ResetPassword;