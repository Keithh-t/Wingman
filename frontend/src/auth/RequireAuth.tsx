import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./AuthContext";
import type { JSX } from "react/jsx-dev-runtime";

// A component that wraps its children and redirects to login if not authenticated
// Ai generated
export default function RequireAuth({ children }: { children: JSX.Element }) {
    const { user, loading } = useAuth();
    const location = useLocation();

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!user) {
        return <Navigate to={"/login"} state={{ from: location }} replace />;
    }
    return children;
}