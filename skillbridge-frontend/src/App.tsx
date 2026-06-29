import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import LoginPage from "./pages/auth/LoginPage";
import Register from "./pages/auth/Register";
import LandingPage from "./pages/jobs/LandingPage";
import JobDetail from "./pages/jobs/JobDetail";
import ApplyJob from "./pages/jobs/ApplyJob";
import CreateJob from "./pages/admin/CreateJob";
import AdminDashboard from "./pages/admin/Dashboard";
import AdminApplications from "./pages/admin/AdminApplications";
import CandidateDashboard from "./pages/candidate/CandidateDashboard";
import CandidateProfile from "./pages/candidate/CandidateProfile";
import TrackApplications from "./pages/candidate/TrackApplications";
import { ProtectedRoute } from "./components/layout/ProtectedRoute";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<Register />} />
          <Route path="/jobs/:id" element={<JobDetail />} />

          {/* Admin Routes */}
          <Route
            path="/admin/dashboard"
            element={
              <ProtectedRoute requiredRole="Admin">
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/jobs/create"
            element={
              <ProtectedRoute requiredRole="Admin">
                <CreateJob />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/applications"
            element={
              <ProtectedRoute requiredRole="Admin">
                <AdminApplications />
              </ProtectedRoute>
            }
          />

          {/* Candidate Routes */}
          <Route
            path="/candidate/dashboard"
            element={
              <ProtectedRoute requiredRole="Candidate">
                <CandidateDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/candidate/profile"
            element={
              <ProtectedRoute requiredRole="Candidate">
                <CandidateProfile />
              </ProtectedRoute>
            }
          />
          <Route
            path="/candidate/applications"
            element={
              <ProtectedRoute requiredRole="Candidate">
                <TrackApplications />
              </ProtectedRoute>
            }
          />
          <Route
            path="/jobs/:id/apply"
            element={
              <ProtectedRoute>
                <ApplyJob />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
