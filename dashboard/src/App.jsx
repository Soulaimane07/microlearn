import { Routes, Route, Navigate } from "react-router-dom";
import Overview from "./pages/overview/Overview";
import Pipelines from "./pages/pipelines/Pipelines";
import PipelineDetailsPage from "./pages/pipelines/PipelineDetailsPage";
import Datasets from "./pages/datasets/Datasets";
import DatasetDetailsPage from "./pages/datasets/DatasetDetailsPage";
import Login from "./pages/auth/login/Login";
import { useSelector } from "react-redux";

export default function App() {
  const user = useSelector((state) => state.auth.user);

  // Protect private routes
  const PrivateRoute = ({ children }) => {
    return user ? children : <Navigate to="/login" />;
  };

  console.log(user);
  

  return (
    <Routes>
      {/* Public Route */}
      <Route path="/login" element={<Login />} />

      {/* Private Routes */}
      <Route
        path="/"
        element={
          <PrivateRoute>
            <Overview />
          </PrivateRoute>
        }
      />
      <Route
        path="/pipelines"
        element={
          <PrivateRoute>
            <Pipelines />
          </PrivateRoute>
        }
      />
      <Route
        path="/pipelines/:id"
        element={
          <PrivateRoute>
            <PipelineDetailsPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/datasets"
        element={
          <PrivateRoute>
            <Datasets />
          </PrivateRoute>
        }
      />
      <Route
        path="/datasets/:id"
        element={
          <PrivateRoute>
            <DatasetDetailsPage />
          </PrivateRoute>
        }
      />

      {/* Catch-all: redirect unknown routes to login or dashboard */}
      <Route path="*" element={<Navigate to={user ? "/" : "/login"} />} />
    </Routes>
  );
}
