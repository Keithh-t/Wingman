import { Link, Outlet } from "react-router-dom";
import HealthBadge from "./components/HealthBadge";
import { useAuth } from "./auth/AuthContext";
import "./styles/AppShell.css";


export default function App() {
  const { user, logout, loading } = useAuth();

  return (
    <div className="app">
      <nav className="app-nav">
        <div className="nav-left">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/dashboard" className="nav-link">Dashboard</Link>
          <Link to="/questions" className="nav-link">Questions</Link>
        </div>

        <div className="nav-right">
          {!loading && user ? (
            <>
              <Link to="/progress" className="nav-link">My Progress</Link>
              <span className="nav-user">Hi, {user.username}</span>
              <button className="nav-button" onClick={logout}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link">Login</Link>
              <Link to="/register" className="nav-link">Sign up</Link>
            </>
          )}
          <HealthBadge />
        </div>
      </nav>

      <main className="app-main">
        <Outlet />
      </main>
    </div>
  );
}
