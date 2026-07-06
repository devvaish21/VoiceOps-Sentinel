import {
  Bell,
  Moon,
  Search,
  Sun,
  ChevronDown,
} from "lucide-react";
import { useState } from "react";

export default function Navbar() {
  const [dark, setDark] = useState(false);

  return (
    <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-slate-200">

      <div className="flex items-center justify-between px-8 py-5">

        {/* Left */}

        <div>

          <h2 className="text-2xl font-bold text-slate-800">
            Dashboard
          </h2>

          <p className="text-sm text-slate-500 mt-1">
            Monitor AI call intelligence in real time
          </p>

        </div>

        {/* Right */}

        <div className="flex items-center gap-5">

          {/* Search */}

          <div className="relative hidden md:block">

            <Search
              size={18}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
            />

            <input
              placeholder="Search calls..."
              className="w-80 rounded-2xl border border-slate-200 bg-slate-50 py-3 pl-11 pr-5 outline-none transition focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-100"
            />

          </div>

          {/* Theme */}

          <button
            onClick={() => setDark(!dark)}
            className="rounded-xl border border-slate-200 bg-white p-3 transition hover:bg-indigo-50 hover:border-indigo-300"
          >
            {dark ? (
              <Sun className="text-amber-500" size={20} />
            ) : (
              <Moon className="text-slate-600" size={20} />
            )}
          </button>

          {/* Notifications */}

          <button className="relative rounded-xl border border-slate-200 bg-white p-3 transition hover:bg-indigo-50 hover:border-indigo-300">

            <Bell size={20} />

            <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-xs text-white">
              3
            </span>

          </button>

          {/* User */}

          <button className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white px-3 py-2 transition hover:shadow-md">

            <img
              src="https://i.pravatar.cc/150?img=8"
              alt="profile"
              className="h-11 w-11 rounded-full"
            />

            <div className="hidden text-left lg:block">

              <h4 className="font-semibold text-slate-800">
                Tejas
              </h4>

              <p className="text-xs text-slate-500">
                Administrator
              </p>

            </div>

            <ChevronDown
              size={18}
              className="text-slate-500"
            />

          </button>

        </div>

      </div>

    </header>
  );
}