import { motion } from "framer-motion";
import {
  Smile,
  TrendingUp,
  TrendingDown,
} from "lucide-react";

const sentiment = [
  {
    label: "Positive",
    value: 72,
    color: "bg-green-500",
  },
  {
    label: "Neutral",
    value: 20,
    color: "bg-yellow-400",
  },
  {
    label: "Negative",
    value: 8,
    color: "bg-red-500",
  },
];

export default function SentimentCard() {
  return (
    <motion.div
      whileHover={{ y: -6 }}
      transition={{ duration: 0.25 }}
      className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white p-7 shadow-sm hover:shadow-xl"
    >
      {/* Glow */}

      <div className="absolute -top-16 -right-16 h-48 w-48 rounded-full bg-green-200/40 blur-3xl"></div>

      <div className="relative z-10">

        {/* Header */}

        <div className="flex items-center justify-between">

          <div className="flex items-center gap-3">

            <div className="rounded-2xl bg-green-100 p-3">
              <Smile className="text-green-600" />
            </div>

            <div>

              <h2 className="text-2xl font-bold text-slate-800">
                Sentiment Analysis
              </h2>

              <p className="text-slate-500">
                Overall customer emotion
              </p>

            </div>

          </div>

          <div className="rounded-full bg-green-100 px-3 py-1 text-sm font-semibold text-green-700">
            +6%
          </div>

        </div>

        {/* Score */}

        <div className="mt-8 flex items-center justify-center">

          <div className="relative">

            <div className="flex h-44 w-44 items-center justify-center rounded-full border-[14px] border-green-500">

              <div className="text-center">

                <h2 className="text-5xl font-bold text-slate-800">
                  89%
                </h2>

                <p className="mt-2 text-slate-500">
                  Positive
                </p>

              </div>

            </div>

          </div>

        </div>

        {/* Progress */}

        <div className="mt-10 space-y-6">

          {sentiment.map((item) => (

            <div key={item.label}>

              <div className="mb-2 flex justify-between">

                <span className="font-medium text-slate-700">
                  {item.label}
                </span>

                <span className="font-semibold">
                  {item.value}%
                </span>

              </div>

              <div className="h-3 rounded-full bg-slate-200">

                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${item.value}%` }}
                  transition={{ duration: 1 }}
                  className={`${item.color} h-3 rounded-full`}
                />

              </div>

            </div>

          ))}

        </div>

        {/* Bottom Stats */}

        <div className="mt-8 grid grid-cols-2 gap-4">

          <div className="rounded-2xl bg-slate-50 p-5">

            <div className="flex items-center gap-2">

              <TrendingUp className="text-green-600" />

              <span className="font-semibold">
                Improved
              </span>

            </div>

            <h3 className="mt-3 text-2xl font-bold">
              +14%
            </h3>

            <p className="text-sm text-slate-500">
              Compared to last week
            </p>

          </div>

          <div className="rounded-2xl bg-slate-50 p-5">

            <div className="flex items-center gap-2">

              <TrendingDown className="text-red-500" />

              <span className="font-semibold">
                Negative
              </span>

            </div>

            <h3 className="mt-3 text-2xl font-bold">
              8%
            </h3>

            <p className="text-sm text-slate-500">
              Only few calls affected
            </p>

          </div>

        </div>

      </div>

    </motion.div>
  );
}