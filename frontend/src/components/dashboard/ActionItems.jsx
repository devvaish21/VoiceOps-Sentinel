import { motion } from "framer-motion";
import {
  CheckCircle2,
  Clock3,
  AlertCircle,
  CalendarDays,
} from "lucide-react";

const tasks = [
  {
    title: "Send refund confirmation email",
    priority: "High",
    due: "Today",
    status: "Completed",
  },
  {
    title: "Verify payment gateway logs",
    priority: "Medium",
    due: "Tomorrow",
    status: "Pending",
  },
  {
    title: "Schedule follow-up call",
    priority: "Low",
    due: "Friday",
    status: "Pending",
  },
  {
    title: "Close support ticket",
    priority: "High",
    due: "Today",
    status: "Completed",
  },
];

export default function ActionItems() {
  return (
    <motion.div
      whileHover={{ y: -6 }}
      className="rounded-3xl border border-slate-200 bg-white p-7 shadow-sm hover:shadow-xl"
    >
      {/* Header */}

      <div className="flex items-center justify-between mb-8">

        <div>

          <h2 className="text-2xl font-bold text-slate-800">
            Action Items
          </h2>

          <p className="text-slate-500">
            AI-generated follow-up tasks
          </p>

        </div>

        <div className="rounded-full bg-indigo-100 px-4 py-2 text-sm font-semibold text-indigo-700">
          4 Tasks
        </div>

      </div>

      {/* Timeline */}

      <div className="space-y-6">

        {tasks.map((task, index) => (

          <div
            key={index}
            className="flex gap-5"
          >

            {/* Timeline */}

            <div className="flex flex-col items-center">

              <div
                className={`flex h-10 w-10 items-center justify-center rounded-full ${
                  task.status === "Completed"
                    ? "bg-green-100"
                    : "bg-orange-100"
                }`}
              >

                {task.status === "Completed" ? (
                  <CheckCircle2 className="text-green-600" size={20} />
                ) : (
                  <Clock3 className="text-orange-600" size={20} />
                )}

              </div>

              {index !== tasks.length - 1 && (
                <div className="mt-2 h-12 w-[2px] bg-slate-200"></div>
              )}

            </div>

            {/* Content */}

            <div className="flex-1 rounded-2xl border border-slate-200 bg-slate-50 p-5">

              <div className="flex items-center justify-between">

                <h3 className="font-semibold text-slate-800">
                  {task.title}
                </h3>

                <span
                  className={`rounded-full px-3 py-1 text-xs font-semibold ${
                    task.priority === "High"
                      ? "bg-red-100 text-red-700"
                      : task.priority === "Medium"
                      ? "bg-yellow-100 text-yellow-700"
                      : "bg-green-100 text-green-700"
                  }`}
                >
                  {task.priority}
                </span>

              </div>

              <div className="mt-4 flex items-center justify-between">

                <div className="flex items-center gap-2 text-sm text-slate-500">

                  <CalendarDays size={16} />

                  Due {task.due}

                </div>

                <div
                  className={`flex items-center gap-2 rounded-full px-3 py-1 text-sm ${
                    task.status === "Completed"
                      ? "bg-green-100 text-green-700"
                      : "bg-orange-100 text-orange-700"
                  }`}
                >

                  <AlertCircle size={15} />

                  {task.status}

                </div>

              </div>

            </div>

          </div>

        ))}

      </div>

      {/* Bottom */}

      <div className="mt-8 rounded-2xl bg-gradient-to-r from-indigo-600 to-violet-600 p-5 text-white">

        <h3 className="font-semibold">
          AI Recommendation
        </h3>

        <p className="mt-2 text-white/90 leading-7">
          Prioritize the payment gateway investigation since multiple
          customers reported similar issues in the last 24 hours.
        </p>

      </div>

    </motion.div>
  );
}