import { useEffect, useState, type FormEvent } from "react";
import {
  ArrowRight,
  Mail,
  Sparkles,
} from "lucide-react";
import {
  Link,
  useLocation,
  useNavigate,
} from "react-router-dom";
import api from "../services/api";

type VerifyOTPState = {
  email?: string;
  purpose?: "registration" | "password-reset";
};

function VerifyOTP() {
  const navigate = useNavigate();
  const location = useLocation();

  const state =
    (location.state as VerifyOTPState | null) || {};

  const email = state.email || "";
  const purpose =
    state.purpose || "registration";

  const isPasswordReset =
    purpose === "password-reset";

  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState("");
  const [seconds, setSeconds] = useState(300);

  useEffect(() => {
    if (!email) {
      navigate(
        isPasswordReset
          ? "/forgot-password"
          : "/register",
        { replace: true },
      );

      return;
    }

    const timer = setInterval(() => {
      setSeconds((current) =>
        current > 0 ? current - 1 : 0,
      );
    }, 1000);

    return () => clearInterval(timer);
  }, [
    email,
    isPasswordReset,
    navigate,
  ]);

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    if (otp.length !== 6) {
      setError(
        "Please enter the 6-digit OTP.",
      );
      return;
    }

    setError("");
    setLoading(true);

    try {
      await api.post("/auth/verify-otp", {
        email,
        otp,
        purpose,
      });

      if (isPasswordReset) {
        navigate("/reset-password", {
          replace: true,
          state: {
            email,
            otp,
          },
        });

        return;
      }

      navigate("/login", {
        replace: true,
        state: {
          verified: true,
          email,
        },
      });
    } catch (err: any) {
      console.error(
        "OTP verification failed:",
        err,
      );

      setError(
        err?.response?.data?.detail ||
          "Invalid or expired OTP. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  const resendOTP = async () => {
    setError("");
    setResending(true);

    try {
      await api.post(
        "/auth/send-otp",
        {
          email,
        },
      );

      setSeconds(300);
      setOtp("");
    } catch (err: any) {
      console.error(
        "OTP resend failed:",
        err,
      );

      setError(
        err?.response?.data?.detail ||
          "Unable to resend OTP. Please try again.",
      );
    } finally {
      setResending(false);
    }
  };

  const minutes = Math.floor(
    seconds / 60,
  );

  const remainingSeconds =
    String(seconds % 60).padStart(2, "0");

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
          to={
            isPasswordReset
              ? "/forgot-password"
              : "/register"
          }
          className="auth-back-home"
        >
          ← Back
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
            <h1>
              {isPasswordReset
                ? "Verify your identity"
                : "Verify your email"}
            </h1>

            <p>
              We sent a 6-digit verification
              code to{" "}
              <strong>{email}</strong>
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
            <label htmlFor="otp">
              Verification code
            </label>

            <div className="auth-input-wrapper">
              <Mail size={18} />

              <input
                id="otp"
                type="text"
                inputMode="numeric"
                autoComplete="one-time-code"
                maxLength={6}
                placeholder="Enter 6-digit OTP"
                value={otp}
                onChange={(event) =>
                  setOtp(
                    event.target.value.replace(
                      /\D/g,
                      "",
                    ),
                  )
                }
                disabled={loading}
              />
            </div>

            <p>
              Code expires in{" "}
              <strong>
                {minutes}:{remainingSeconds}
              </strong>
            </p>

            <button
              className="btn btn-primary auth-submit"
              type="submit"
              disabled={
                loading ||
                otp.length !== 6 ||
                seconds === 0
              }
            >
              {loading
                ? "Verifying..."
                : isPasswordReset
                  ? "Verify & continue"
                  : "Verify email"}

              {!loading && (
                <ArrowRight size={17} />
              )}
            </button>
          </form>

          <button
            type="button"
            className="back-home"
            onClick={resendOTP}
            disabled={
              resending ||
              seconds > 240
            }
          >
            {resending
              ? "Sending..."
              : seconds > 240
                ? `Resend available in ${
                    seconds - 240
                  }s`
                : "Resend OTP"}
          </button>

          <Link
            className="back-home"
            to={
              isPasswordReset
                ? "/forgot-password"
                : "/register"
            }
          >
            Use a different email
          </Link>
        </section>
      </main>
    </div>
  );
}

export default VerifyOTP;