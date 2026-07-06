import { motion } from "framer-motion";
import {
  Search,
  MoreVertical,
  PhoneCall,
} from "lucide-react";

const calls = [
  {
    id: 1,
    customer: "John Smith",
    company: "Acme Inc.",
    duration: "04:12",
    sentiment: "Positive",
    status: "Completed",
    avatar: "JS",
  },
  {
    id: 2,
    customer: "Sarah Lee",
    company: "Amazon",
    duration: "08:25",
    sentiment: "Neutral",
    status: "Processing",
    avatar: "SL",
  },
  {
    id: 3,
    customer: "Michael Brown",
    company: "Google",
    duration: "06:41",
    sentiment: "Negative",
    status: "Completed",
    avatar: "MB",
  },
  {
    id: 4,
    customer: "Emma Wilson",
    company: "Netflix",
    duration: "05:38",
    sentiment: "Positive",
    status: "Completed",
    avatar: "EW",
  },
];

export default function RecentCalls() {
  return (
    <motion.div
      whileHover={{ y: -6 }}
      className="rounded-3xl border border-slate-200 bg-white p-7 shadow-sm hover:shadow-xl"
    >
      {/* Header */}

      <div className="flex items-center justify-between mb-6">

        <div>

          <h2 className="text-2xl font-bold text-slate-800">
            Recent Calls
          </h2>

          <p className="text-slate-500">
            Latest analyzed conversations
          </p>

        </div>

        <div className="relative">

          <Search
            size={18}
            className="absolute left-3 top-3 text-slate-400"
          />

          <input
            placeholder="Search..."
            className="rounded-xl border border-slate-200 bg-slate-50 py-2 pl-10 pr-4 outline-none focus:ring-2 focus:ring-indigo-200"
          />

        </div>

      </div>

      {/* Table */}

      <div className="overflow-x-auto">

        <table className="w-full">

          <thead>

            <tr className="border-b border-slate-200 text-left text-slate-500">

              <th className="pb-4 font-medium">
                Customer
              </th>

              <th className="pb-4 font-medium">
                Duration
              </th>

              <th className="pb-4 font-medium">
                Sentiment
              </th>

              <th className="pb-4 font-medium">
                Status
              </th>

              <th className="pb-4"></th>

            </tr>

          </thead>

          <tbody>

            {calls.map((call) => (

              <tr
                key={call.id}
                className="border-b border-slate-100 transition hover:bg-slate-50"
              >

                {/* Customer */}

                <td className="py-5">

                  <div className="flex items-center gap-4">

                    <div className="flex h-11 w-11 items-center justify-center rounded-full bg-gradient-to-r from-indigo-600 to-violet-600 font-semibold text-white">

                      {call.avatar}

                    </div>

                    <div>

                      <h4 className="font-semibold text-slate-800">
                        {call.customer}
                      </h4>

                      <p className="text-sm text-slate-500">
                        {call.company}
                      </p>

                    </div>

                  </div>

                </td>

                {/* Duration */}

                <td>

                  <div className="flex items-center gap-2">

                    <PhoneCall
                      size={16}
                      className="text-slate-400"
                    />

                    {call.duration}

                  </div>

                </td>

                {/* Sentiment */}

                <td>

                  <span
                    className={`rounded-full px-3 py-1 text-sm font-semibold ${
                      call.sentiment === "Positive"
                        ? "bg-green-100 text-green-700"
                        : call.sentiment === "Neutral"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-red-100 text-red-700"
                    }`}
                  >
                    {call.sentiment}
                  </span>

                </td>

                {/* Status */}

                <td>

                  <span
                    className={`rounded-full px-3 py-1 text-sm font-semibold ${
                      call.status === "Completed"
                        ? "bg-indigo-100 text-indigo-700"
                        : "bg-orange-100 text-orange-700"
                    }`}
                  >
                    {call.status}
                  </span>

                </td>

                {/* Menu */}

                <td className="text-right">

                  <button className="rounded-lg p-2 hover:bg-slate-100">

                    <MoreVertical size={18} />

                  </button>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </motion.div>
  );
}