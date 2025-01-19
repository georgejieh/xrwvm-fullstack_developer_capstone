import React, { useState } from "react";
import "./Login.css";
import Header from "../Header/Header";
import { useNavigate } from "react-router-dom";

const Login = ({ onClose }) => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(true);

  const navigate = useNavigate();
  let login_url = window.location.origin + "/djangoapp/login";

  const login = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch(login_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userName: userName,
          password: password,
        }),
      });

      const json = await res.json();
      if (json.status && json.status === "Authenticated") {
        sessionStorage.setItem("username", json.userName);
        setOpen(false);
      } else {
        alert("The user could not be authenticated.");
      }
    } catch (error) {
      console.error("Error during login:", error);
      alert("An error occurred. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    sessionStorage.removeItem("username");
    setOpen(false);
  };

  if (!open) {
    navigate("/");
  }

  return (
    <div>
      <Header />
      <div onClick={onClose}>
        <div
          onClick={(e) => {
            e.stopPropagation();
          }}
          className="modalContainer"
        >
          <form className="login_panel" onSubmit={login}>
            <div>
              <span className="input_field">Username </span>
              <input
                type="text"
                name="username"
                placeholder="Username"
                className="input_field"
                onChange={(e) => setUserName(e.target.value)}
              />
            </div>
            <div>
              <span className="input_field">Password </span>
              <input
                name="psw"
                type="password"
                placeholder="Password"
                className="input_field"
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div>
              <input
                className="action_button"
                type="submit"
                value={loading ? "Logging in..." : "Login"}
                disabled={loading}
              />
              <input
                className="action_button"
                type="button"
                value="Cancel"
                onClick={handleCancel}
              />
            </div>
            <a className="loginlink" href="/register">
              Register Now
            </a>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;