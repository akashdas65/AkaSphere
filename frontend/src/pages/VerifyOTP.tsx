import { useEffect, useState, type FormEvent } from "react";
import { ArrowRight, Mail, Sparkles } from "lucide-react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import api from "../services/api";

function VerifyOTP() {
  const navigate = useNavigate();
  const location = useLocation();

  const email = (location.state as { email?: string } | null)?.email || "";

  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState("");
  const [seconds, setSeconds] = useState(300);

  useEffect(() => {
    if (!email) {
      navigate("/register", { replace: true });
      return;
    }

    const timer = setInterval(() => {
      setSeconds((current) => (current > 0 ? current - 1 : 0));
    }, 1000);

    return () => clearInterval(timer);
  }, [email, navigate]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (otp.length !== 6) {
      setError("Please enter the 6-digit OTP.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      await api.post("/auth/verify-otp", {
        email,
        otp,
      });

      navigate("/login", {
        replace: true,
        state: {
          verified: true,
          email,
        },
      });
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
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
      await api.post("/auth/send-otp", { email });
      setSeconds(300);
      setOtp("");
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          "Unable to resend OTP. Please try again.",
      );
    } finally {
      setResending(false);
    }
  };

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = String(seconds % 60).padStart(2, "0");

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
          <h1>Verify your email</h1>
          <p>
            We sent a 6-digit verification code to{" "}
            <strong>{email}</strong>
          </p>
        </div>

        <div className="input-wrapper">
          <Mail size={18} />

          <input
            type="text"
            inputMode="numeric"
            autoComplete="one-time-code"
            maxLength={6}
            placeholder="Enter 6-digit OTP"
            value={otp}
            onChange={(event) =>
              setOtp(event.target.value.replace(/\D/g, ""))
            }
            disabled={loading}
          />
        </div>

        {error && (
          <div className="auth-error" role="alert">
            {error}
          </div>
        )}

        <p>
          Code expires in{" "}
          <strong>
            {minutes}:{remainingSeconds}
          </strong>
        </p>

        <form onSubmit={handleSubmit}>
          <button
            className="btn btn-primary auth-submit"
            type="submit"
            disabled={loading || otp.length !== 6 || seconds === 0}
          >
            {loading ? "Verifying..." : "Verify email"}
            {!loading && <ArrowRight size={17} />}
          </button>
        </form>

        <button
          type="button"
          className="back-home"
          onClick={resendOTP}
          disabled={resending || seconds > 240}
        >
          {resending
            ? "Sending..."
            : seconds > 240
              ? `Resend available in ${seconds - 240}s`
              : "Resend OTP"}
        </button>

        <Link className="back-home" to="/register">
          Use a different email
        </Link>
      </div>
    </div>
  );
}

export default VerifyOTP;
