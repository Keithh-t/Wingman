import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import NotFound from "./pages/NotFound";
import QuestionDetailPage from "./components/QuestionDetailPage";
import QuestionList from "./components/QuestionList";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,            // layout/shell
    children: [
      { index: true, element: <Home /> },
      { path: "dashboard", element: <Dashboard /> },
      { path: "questions", element: <QuestionList /> },
      { path: "questions/:id", element: <QuestionDetailPage /> },
      { path: "*", element: <NotFound /> },
    ],
  },
]);
