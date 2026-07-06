import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";

export default function Settings() {
  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />

      <div className="flex-1">
        <Navbar />

        <main className="p-8">
          <h1 className="text-4xl font-bold">Settings</h1>

          <p className="text-slate-500 mt-2">
            Configure your VoiceOps Sentinel workspace.
          </p>
        </main>
      </div>
    </div>
  );
}