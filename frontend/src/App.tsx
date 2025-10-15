import { Link, Outlet } from "react-router-dom";

export default function App() {
  return (
    <div>
      <nav style={{ padding: 12, display: "flex", gap: 12 }}>
        <Link to="/">Home</Link>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/login">Login</Link>
      </nav>
      <main style={{ padding: 12 }}>
        <Outlet />
      </main>
    </div>
  );
}
