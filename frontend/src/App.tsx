import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import News from "./pages/News";
import Weather from "./pages/Weather";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen">
        <Navbar />

        <main className="mx-auto w-full max-w-7xl px-4 pb-12 pt-8 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/news" element={<News />} />
            <Route path="/weather" element={<Weather />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
