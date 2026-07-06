import { motion } from "framer-motion";
import {
  UploadCloud,
  FileAudio,
  CheckCircle2,
  Music4,
  FileMusic,
} from "lucide-react";

export default function UploadCard() {
  return (
    <motion.div
      whileHover={{ y: -6 }}
      transition={{ duration: 0.25 }}
      className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white p-8 shadow-sm hover:shadow-xl"
    >
      {/* Background Glow */}
      <div className="absolute -right-20 -top-20 h-56 w-56 rounded-full bg-indigo-200/40 blur-3xl"></div>

      <div className="relative z-10">

        <div className="flex items-center justify-between">

          <div>

            <h2 className="text-2xl font-bold text-slate-800">
              Upload Audio
            </h2>

            <p className="mt-2 text-slate-500">
              Drag & drop your customer call recordings
            </p>

          </div>

          <div className="rounded-2xl bg-indigo-100 p-4">
            <UploadCloud className="text-indigo-600" size={28} />
          </div>

        </div>

        {/* Upload Area */}

        <div className="group mt-8 cursor-pointer rounded-3xl border-2 border-dashed border-indigo-300 bg-indigo-50/40 p-10 text-center transition-all hover:border-indigo-500 hover:bg-indigo-50">

          <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-indigo-500 to-violet-600 shadow-lg">

            <UploadCloud size={38} className="text-white" />

          </div>

          <h3 className="mt-6 text-xl font-semibold text-slate-800">
            Drag & Drop Audio Files
          </h3>

          <p className="mt-2 text-slate-500">
            or click below to browse from your device
          </p>

          <button className="mt-6 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 px-6 py-3 font-semibold text-white shadow-lg transition hover:scale-105">
            Browse Files
          </button>

          {/* Supported Formats */}

          <div className="mt-8 flex flex-wrap justify-center gap-3">

            <Chip icon={<Music4 size={16} />} text="MP3" />

            <Chip icon={<FileMusic size={16} />} text="WAV" />

            <Chip icon={<FileAudio size={16} />} text="M4A" />

          </div>

        </div>

        {/* Recent Upload */}

        <div className="mt-8 rounded-2xl border border-slate-200 bg-slate-50 p-5">

          <div className="flex items-center justify-between">

            <div className="flex items-center gap-4">

              <div className="rounded-xl bg-indigo-100 p-3">

                <FileAudio className="text-indigo-600" />

              </div>

              <div>

                <h4 className="font-semibold text-slate-800">
                  customer_call.mp3
                </h4>

                <p className="text-sm text-slate-500">
                  8.2 MB
                </p>

              </div>

            </div>

            <CheckCircle2 className="text-green-500" />

          </div>

          {/* Progress */}

          <div className="mt-6">

            <div className="mb-2 flex justify-between text-sm">

              <span className="text-slate-500">
                Uploading...
              </span>

              <span className="font-semibold text-indigo-600">
                84%
              </span>

            </div>

            <div className="h-3 rounded-full bg-slate-200">

              <motion.div
                initial={{ width: 0 }}
                animate={{ width: "84%" }}
                transition={{ duration: 1 }}
                className="h-3 rounded-full bg-gradient-to-r from-indigo-600 to-violet-600"
              />

            </div>

          </div>

        </div>

      </div>

    </motion.div>
  );
}

function Chip({ icon, text }) {
  return (
    <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium shadow-sm">
      {icon}
      {text}
    </div>
  );
}