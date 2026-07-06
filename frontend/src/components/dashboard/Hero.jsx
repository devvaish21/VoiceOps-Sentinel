import { motion } from "framer-motion";
import {
  Upload,
  BarChart3,
  Mic,
  Brain,
  ShieldCheck,
  Smile,
} from "lucide-react";

export default function Hero() {
  return (
    <motion.section
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="relative overflow-hidden rounded-[32px] bg-gradient-to-br from-indigo-600 via-violet-600 to-purple-700 p-8 lg:p-10 text-white shadow-xl"
    >
      {/* Background Blur */}
      <div className="absolute -top-24 -right-24 h-72 w-72 rounded-full bg-white/20 blur-3xl" />
      <div className="absolute bottom-0 left-1/3 h-48 w-48 rounded-full bg-pink-400/20 blur-3xl" />

      <div className="relative z-10 grid lg:grid-cols-2 gap-10 items-center">

        {/* Left Content */}
        <div>

          <span className="inline-flex items-center rounded-full border border-white/30 bg-white/10 px-4 py-1 text-sm backdrop-blur">
            👋 Welcome Back
          </span>

          <h1 className="mt-5 text-4xl md:text-5xl font-extrabold leading-tight">
            VoiceOps
            <br />
            Sentinel
          </h1>

          <p className="mt-5 text-white/90 text-lg max-w-xl">
            AI-powered platform to transcribe conversations, detect speakers,
            analyze sentiment, generate summaries and protect sensitive
            information.
          </p>

          {/* Feature Pills */}

          <div className="mt-8 flex flex-wrap gap-3">

            <Feature icon={<Mic size={16} />} text="Speech to Text" />

            <Feature icon={<Brain size={16} />} text="AI Summary" />

            <Feature icon={<Smile size={16} />} text="Sentiment" />

            <Feature
              icon={<ShieldCheck size={16} />}
              text="PII Detection"
            />

          </div>

          {/* Buttons */}

          <div className="mt-10 flex flex-wrap gap-4">

            <button className="flex items-center gap-2 rounded-xl bg-white px-6 py-3 font-semibold text-indigo-700 shadow-lg transition hover:scale-105">

              <Upload size={18} />

              Upload Audio

            </button>

            <button className="flex items-center gap-2 rounded-xl border border-white/30 bg-white/10 px-6 py-3 font-semibold backdrop-blur transition hover:bg-white/20">

              <BarChart3 size={18} />

              View Analytics

            </button>

          </div>

        </div>

        {/* Right Content */}

        <motion.div
          initial={{ opacity: 0, scale: 0.85 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="flex justify-center lg:justify-end"
        >

          <div className="w-full max-w-sm rounded-3xl border border-white/20 bg-white/10 p-6 backdrop-blur-xl">

            <h3 className="text-lg font-semibold">
              Live AI Analysis
            </h3>

            <p className="mt-1 text-sm text-white/80">
              Customer Call.mp3
            </p>

            {/* Fake Waveform */}

            <div className="mt-8 flex items-end justify-between h-24">

              {[30, 55, 70, 40, 85, 60, 95, 45, 80, 55, 70, 35].map(
                (height, index) => (
                  <motion.div
                    key={index}
                    animate={{
                      height: [height, height + 15, height],
                    }}
                    transition={{
                      repeat: Infinity,
                      duration: 1.2,
                      delay: index * 0.08,
                    }}
                    className="w-2 rounded-full bg-white"
                    style={{
                      height,
                    }}
                  />
                )
              )}

            </div>

            {/* Metrics */}

            <div className="mt-8 grid grid-cols-2 gap-4">

              <Metric title="Accuracy" value="98%" />

              <Metric title="Sentiment" value="Positive" />

              <Metric title="Duration" value="08:45" />

              <Metric title="Speakers" value="2" />

            </div>

          </div>

        </motion.div>

      </div>

    </motion.section>
  );
}

function Feature({ icon, text }) {
  return (
    <div className="flex items-center gap-2 rounded-full bg-white/15 px-4 py-2 text-sm backdrop-blur">
      {icon}
      {text}
    </div>
  );
}

function Metric({ title, value }) {
  return (
    <div className="rounded-2xl bg-white/10 p-4 backdrop-blur">
      <p className="text-xs text-white/70">{title}</p>

      <h4 className="mt-1 text-lg font-bold">
        {value}
      </h4>
    </div>
  );
}