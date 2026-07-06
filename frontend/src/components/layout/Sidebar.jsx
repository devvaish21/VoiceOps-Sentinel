import {
  LayoutDashboard,
  Upload,
  History,
  BarChart3,
  Settings,
  PhoneCall,
  ChevronRight,
  Sparkles,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const menu = [
  {
    title: "Dashboard",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    title: "Upload Audio",
    path: "/upload",
    icon: Upload,
  },
  {
    title: "Call History",
    path: "/history",
    icon: History,
  },
  {
    title: "Analytics",
    path: "/analytics",
    icon: BarChart3,
  },
  {
    title: "Settings",
    path: "/settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  return (
    <aside className="flex h-screen w-72 flex-col border-r border-slate-200 bg-white">

      {/* Logo */}

      <div className="border-b border-slate-100 p-6">

        <div className="flex items-center gap-4">

          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-600 via-violet-600 to-purple-700 shadow-lg">

            <PhoneCall className="text-white" />

          </div>

          <div>

            <h1 className="text-xl font-bold text-slate-800">
              VoiceOps
            </h1>

            <p className="text-sm text-slate-500">
              Sentinel AI
            </p>

          </div>

        </div>

      </div>

      {/* Workspace */}

      <div className="mx-5 mt-6 rounded-3xl bg-gradient-to-r from-indigo-600 to-violet-600 p-5 text-white shadow-lg">

        <div className="flex items-center justify-between">

          <div>

            <p className="text-sm text-white/80">
              Workspace
            </p>

            <h3 className="mt-1 text-lg font-bold">
              Voice Intelligence
            </h3>

          </div>

          <Sparkles />

        </div>

      </div>

      {/* Navigation */}

      <nav className="mt-8 flex-1 px-5">

        <p className="mb-3 px-4 text-xs font-semibold uppercase tracking-wider text-slate-400">
          Navigation
        </p>

        <div className="space-y-2">

          {menu.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.title}
                to={item.path}
                className={({ isActive }) =>
                  `group flex items-center justify-between rounded-2xl px-4 py-4 transition-all duration-300 ${
                    isActive
                      ? "bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-lg"
                      : "text-slate-600 hover:bg-slate-100"
                  }`
                }
              >
                <div className="flex items-center gap-3">

                  <Icon size={20} />

                  <span className="font-medium">
                    {item.title}
                  </span>

                </div>

                <ChevronRight
                  size={18}
                  className="opacity-0 transition group-hover:opacity-100"
                />

              </NavLink>
            );
          })}

        </div>

      </nav>

      {/* Bottom Card */}

      <div className="p-5">

        <div className="rounded-3xl border border-indigo-100 bg-indigo-50 p-5">

          <div className="flex items-center gap-4">

            <img
              src="https://i.pravatar.cc/100?img=12"
              alt="profile"
              className="h-12 w-12 rounded-full"
            />

            <div>

              <h3 className="font-semibold text-slate-800">
                Tejas Pagar
              </h3>

              <p className="text-sm text-slate-500">
                AI Engineer
              </p>

            </div>

          </div>

          <div className="mt-5 rounded-xl bg-white p-4">

            <div className="flex justify-between text-sm">

              <span className="text-slate-500">
                AI Credits
              </span>

              <span className="font-semibold">
                820 / 1000
              </span>

            </div>

            <div className="mt-3 h-2 rounded-full bg-slate-200">

              <div className="h-2 w-[82%] rounded-full bg-gradient-to-r from-indigo-600 to-violet-600"></div>

            </div>

          </div>

        </div>

      </div>

    </aside>
  );
}