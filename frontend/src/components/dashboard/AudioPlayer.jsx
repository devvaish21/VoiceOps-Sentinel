import { motion } from "framer-motion";
import {
  Play,
  SkipBack,
  SkipForward,
  Volume2,
  Mic2,
  Download,
  MoreHorizontal,
} from "lucide-react";

export default function AudioPlayer() {
  const waveform = [
    22, 45, 70, 40, 85, 60, 95, 55, 80, 50, 75, 35,
    65, 90, 55, 75, 45, 82, 60, 92, 48, 70, 40, 58,
  ];

  return (
    <motion.div
      whileHover={{ y: -6 }}
      transition={{ duration: 0.25 }}
      className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white p-8 shadow-sm hover:shadow-xl"
    >
      {/* Glow */}
      <div className="absolute -bottom-20 -right-20 h-56 w-56 rounded-full bg-cyan-200/40 blur-3xl"></div>

      <div className="relative z-10">

        {/* Header */}

        <div className="flex items-center justify-between">

          <div className="flex items-center gap-4">

            <div className="rounded-2xl bg-indigo-100 p-4">
              <Mic2 className="text-indigo-600" size={28} />
            </div>

            <div>

              <h2 className="text-2xl font-bold text-slate-800">
                Audio Player
              </h2>

              <p className="text-slate-500">
                customer_call.mp3
              </p>

            </div>

          </div>

          <div className="flex gap-2">

            <button className="rounded-xl p-3 hover:bg-slate-100">
              <Download size={18} />
            </button>

            <button className="rounded-xl p-3 hover:bg-slate-100">
              <MoreHorizontal size={18} />
            </button>

          </div>

        </div>

        {/* Waveform */}

        <div className="mt-10 flex h-28 items-end justify-between">

          {waveform.map((bar, index) => (
            <motion.div
              key={index}
              animate={{
                height: [bar, bar + 12, bar],
              }}
              transition={{
                repeat: Infinity,
                duration: 1.4,
                delay: index * 0.05,
              }}
              className="w-2 rounded-full bg-gradient-to-t from-indigo-600 to-cyan-400"
              style={{
                height: `${bar}px`,
              }}
            />
          ))}

        </div>

        {/* Timeline */}

        <div className="mt-8">

          <div className="h-2 rounded-full bg-slate-200">

            <motion.div
              initial={{ width: 0 }}
              animate={{ width: "42%" }}
              transition={{ duration: 2 }}
              className="h-2 rounded-full bg-gradient-to-r from-indigo-600 to-cyan-500"
            />

          </div>

          <div className="mt-2 flex justify-between text-sm text-slate-500">

            <span>01:18</span>

            <span>03:42</span>

          </div>

        </div>

        {/* Controls */}

        <div className="mt-10 flex items-center justify-between">

          <div className="flex items-center gap-4">

            <button className="rounded-full bg-slate-100 p-3 hover:bg-slate-200">
              <SkipBack />
            </button>

            <button className="rounded-full bg-gradient-to-r from-indigo-600 to-violet-600 p-5 text-white shadow-lg hover:scale-105 transition">
              <Play fill="white" />
            </button>

            <button className="rounded-full bg-slate-100 p-3 hover:bg-slate-200">
              <SkipForward />
            </button>

          </div>

          <div className="flex items-center gap-3">

            <Volume2 className="text-slate-500" />

            <div className="h-2 w-28 rounded-full bg-slate-200">

              <div className="h-2 w-3/4 rounded-full bg-indigo-600"></div>

            </div>

          </div>

        </div>

      </div>

    </motion.div>
  );
}