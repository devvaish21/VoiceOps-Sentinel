import { motion } from "framer-motion";
import { Search, Clock3, Sparkles } from "lucide-react";

const transcript = [
  {
    speaker: "Agent",
    avatar: "A",
    color: "bg-indigo-600",
    time: "00:15",
    message:
      "Hello, thank you for calling VoiceOps Support. My name is Alex. How may I help you today?",
  },
  {
    speaker: "Customer",
    avatar: "C",
    color: "bg-emerald-500",
    time: "00:32",
    message:
      "Hi, my online payment failed but the amount has already been deducted from my account.",
  },
  {
    speaker: "Agent",
    avatar: "A",
    color: "bg-indigo-600",
    time: "01:04",
    message:
      "I understand your concern. Let me verify your transaction details and help you with the refund process.",
  },
  {
    speaker: "AI Insight",
    avatar: "AI",
    color: "bg-violet-600",
    time: "01:20",
    message:
      "Possible payment gateway issue detected. Customer sentiment slightly negative.",
  },
];

export default function Transcript() {
  return (
    <motion.div
      whileHover={{ y: -6 }}
      className="rounded-3xl border border-slate-200 bg-white p-7 shadow-sm hover:shadow-xl transition"
    >
      {/* Header */}

      <div className="flex items-center justify-between">

        <div>

          <h2 className="text-2xl font-bold text-slate-800">
            Live Transcript
          </h2>

          <p className="text-slate-500 mt-1">
            AI-generated conversation transcript
          </p>

        </div>

        <div className="relative">

          <Search
            size={18}
            className="absolute left-4 top-3 text-slate-400"
          />

          <input
            placeholder="Search transcript..."
            className="rounded-xl border border-slate-200 bg-slate-50 py-2 pl-11 pr-4 outline-none focus:ring-2 focus:ring-indigo-200"
          />

        </div>

      </div>

      {/* Messages */}

      <div className="mt-8 space-y-6 max-h-[430px] overflow-y-auto pr-2">

        {transcript.map((item, index) => (

          <motion.div
            key={index}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.15 }}
            className="flex gap-4"
          >

            {/* Avatar */}

            <div
              className={`h-11 w-11 rounded-full ${item.color} flex items-center justify-center text-white font-bold shadow`}
            >
              {item.avatar}
            </div>

            {/* Bubble */}

            <div className="flex-1 rounded-2xl border border-slate-200 bg-slate-50 p-5">

              <div className="flex items-center justify-between">

                <div className="flex items-center gap-2">

                  <h4 className="font-semibold text-slate-800">
                    {item.speaker}
                  </h4>

                  {item.speaker === "AI Insight" && (
                    <span className="flex items-center gap-1 rounded-full bg-violet-100 px-2 py-1 text-xs text-violet-700">
                      <Sparkles size={12} />
                      AI
                    </span>
                  )}

                </div>

                <span className="flex items-center gap-1 text-xs text-slate-500">
                  <Clock3 size={12} />
                  {item.time}
                </span>

              </div>

              <p className="mt-3 leading-7 text-slate-600">
                {item.message}
              </p>

            </div>

          </motion.div>

        ))}

      </div>
    </motion.div>
  );
}