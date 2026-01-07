// client/src/pages/ErrorPage.js
import React from "react";
import { useRouteError, Link } from "react-router-dom";

function ErrorPage() {
  const err = useRouteError();
  const message = err?.statusText || err?.message || "Unknown error";

  return (
    <div className="text-center py-5">
      <h1 className="h4 mb-3">Something went wrong</h1>
      <p className="text-muted">{message}</p>
      <Link className="btn btn-outline-primary btn-sm" to="/">
        Go Home
      </Link>
    </div>
  );
}

export default ErrorPage;