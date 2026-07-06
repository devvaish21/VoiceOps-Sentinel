import { motion } from "framer-motion";
import {
  PhoneCall,
  Smile,
  CheckCircle2,
  Clock3,
  TrendingUp,
} from "lucide-react";

const stats = [
  {
    title: "Total Calls",
    value: "1,248",
    change: "+18%",
    subtitle: "vs last week",
    color: "from-indigo-500 to-violet-500",
    icon: PhoneCall,
  },
  {
    title: "Avg Sentiment",
    value: "89%",
    change: "+6%",
    subtitle: "Customer Satisfaction",
    color: "from-green-500 to-emerald-500",
    icon: Smile,
  },
  {
    title: "Action Items",
    value: "218",
    change: "+12",
    subtitle: "Pending Tasks",
    color: "from-orange-500 to-amber-500",
    icon: CheckCircle2,
  },
  {
    title: "Avg Duration",
    value: "08:45",
    change: "-4%",
    subtitle: "Average Call",
    color: "from-cyan-500 to-sky-500",
    icon: Clock3,
  },
];

export default function StatsCards() {
  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 xl:grid-cols-4">
      {stats.map((item, index) => {
        const Icon = item.icon;

        return (
          <motion.div
            key={item.title}
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{
              y: -8,
              transition: { duration: 0.2 },
            }}
            className="group relative overflow-hidden rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition-all duration-300 hover:shadow-xl"
          >
            {/* Background Gradient */}
            <div
              className={`absolute top-0 right-0 h-32 w-32 rounded-full bg-gradient-to-br ${item.color} opacity-10 blur-3xl`}
            />

            <div className="relative z-10">
              {/* Top */}

              <div className="flex items-center justify-between">

                <div
                  className={`flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br ${item.color} shadow-lg`}
                >
                  <Icon className="text-white" size={26} />
                </div>

                <div className="flex items-center gap-1 rounded-full bg-green-50 px-3 py-1 text-sm font-semibold text-green-600">
                  <TrendingUp size={15} />
                  {item.change}
                </div>

              </div>

              {/* Value */}

              <h2 className="mt-8 text-4xl font-bold text-slate-800">
                {item.value}
              </h2>

              {/* Title */}

              <p className="mt-2 text-lg font-semibold text-slate-700">
                {item.title}
              </p>

              {/* Footer */}

              <p className="mt-1 text-sm text-slate-500">
                {item.subtitle}
              </p>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}