import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { loginSuccess, loginFailure } from "../../../redux/slices/authSlice";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    setTimeout(() => {
      setLoading(false);
      dispatch(loginSuccess({ email, name: email }));
      navigate("/");

      // if (email === "admin@example.com" && password === "123456") {
      //   dispatch(loginSuccess({ email, name: "Admin" }));
      //   navigate("/");
      // } else {
      //   dispatch(loginFailure("Invalid credentials"));
      //   alert("Invalid email or password");
      // }
    }, 1000);
  };

  return (
    <div className="min-h-screen flex">
      <div
        className="flex-1 flex items-center justify-center relative"
        style={{ backgroundImage: "url('./login.jpg')", backgroundSize: "cover", backgroundPosition: "center",}}
      >
        <div className="absolute inset-0 bg-black/40"></div>

        <div className="relative bg-white p-10 rounded-2xl shadow-lg w-full max-w-md z-10">
          <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">
            Welcome Back
          </h2>
          <p className="text-center text-gray-500 mb-8">
            Please login to your account
          </p>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block mb-1 font-medium text-gray-700">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="Enter your email"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500"
              />
            </div>
            <div>
              <label className="block mb-1 font-medium text-gray-700">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Enter your password"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500"
              />
            </div>
            <div className="flex justify-end">
              <a href="#" className="text-sm text-yellow-600 hover:underline">
                Forgot password?
              </a>
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-yellow-600 text-white py-2 rounded-lg hover:bg-yellow-700 transition"
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
