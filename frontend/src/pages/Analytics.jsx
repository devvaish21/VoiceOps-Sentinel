import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";

export default function Analytics() {
  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />

      <div className="flex-1">
        <Navbar />

        <main className="p-8">
          <h1 className="text-4xl font-bold">Analytics</h1>

          <p className="text-slate-500 mt-2">
            AI insights and performance metrics.
          </p>
        </main>
      </div>
    </div>
  );
}