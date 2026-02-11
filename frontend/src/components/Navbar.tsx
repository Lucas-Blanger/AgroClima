import { Link } from "react-router-dom";

export function Navbar() {
  return (
    <nav className="bg-white shadow-md px-8 py-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold text-green-600">AgroClima</h1>

      <div className="flex gap-6">
        <Link to="/" className="hover:text-green-600">
          Dashboard
        </Link>
        <Link to="/news" className="hover:text-green-600">
          News
        </Link>
        <Link to="/weather" className="hover:text-green-600">
          Weather
        </Link>
      </div>
    </nav>
  );
}
