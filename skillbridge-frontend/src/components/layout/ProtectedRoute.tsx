import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

type Props = {
  children: React.ReactNode;
  requiredRole?: 'Admin' | 'Candidate';
};

export const ProtectedRoute: React.FC<Props> = ({ children, requiredRole }) => {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRole && user?.type !== requiredRole) {
    // Redirect Admin to admin dashboard, Candidate to candidate dashboard
    if (user?.type === 'Admin') return <Navigate to="/admin/dashboard" replace />;
    return <Navigate to="/candidate/dashboard" replace />;
  }

  return <>{children}</>;
};