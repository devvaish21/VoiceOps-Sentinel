import { motion } from "framer-motion";
import {
  ShieldCheck,
  Phone,
  Mail,
  CreditCard,
  BadgeCheck,
  Lock,
} from "lucide-react";

export default function PIICard() {
  return (
    <motion.div
      whileHover={{ y: -6 }}
      transition={{ duration: 0.25 }}
      className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white p-7 shadow-sm hover:shadow-xl"
    >
      {/* Background Glow */}
      <div className="absolute -top-20 -right-20 h-56 w-56 rounded-full bg-red-200/40 blur-3xl"></div>

      <div className="relative z-10">

        {/* Header */}

        <div className="flex items-center justify-between">

          <div className="flex items-center gap-3">

            <div className="rounded-2xl bg-red-100 p-3">

              <ShieldCheck className="text-red-600" />

            </div>

            <div>

              <h2 className="text-2xl font-bold text-slate-800">
                PII Detection
              </h2>

              <p className="text-slate-500">
                Sensitive information automatically masked
              </p>

            </div>

          </div>

          <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-semibold text-green-700">
            Protected
          </span>

        </div>

        {/* Security Score */}

        <div className="mt-8 rounded-3xl bg-gradient-to-r from-indigo-600 to-violet-600 p-6 text-white">

          <div className="flex justify-between items-center">

            <div>

              <p className="text-white/80">
                Security Score
              </p>

              <h2 className="mt-2 text-4xl font-bold">
                98%
              </h2>

            </div>

            <Lock size={48} />

          </div>

        </div>

        {/* Detected Fields */}

        <div className="mt-8 space-y-4">

          <InfoRow
            icon={<Phone size={18} />}
            title="Phone Number"
            value="+91 ********54"
          />

          <InfoRow
            icon={<Mail size={18} />}
            title="Email Address"
            value="tej****@gmail.com"
          />

          <InfoRow
            icon={<CreditCard size={18} />}
            title="Bank Account"
            value="XXXX XXXX XXXX 4521"
          />

        </div>

        {/* Footer */}

        <div className="mt-8 rounded-2xl border border-green-200 bg-green-50 p-5">

          <div className="flex items-center gap-3">

            <BadgeCheck className="text-green-600" />

            <div>

              <h3 className="font-semibold text-green-700">
                AI Protection Enabled
              </h3>

              <p className="mt-1 text-sm text-green-600">
                All detected sensitive information has been masked before
                displaying the transcript.
              </p>

            </div>

          </div>

        </div>

      </div>

    </motion.div>
  );
}

function InfoRow({ icon, title, value }) {
  return (
    <div className="flex items-center justify-between rounded-2xl border border-slate-200 bg-slate-50 p-4">

      <div className="flex items-center gap-3">

        <div className="rounded-xl bg-white p-3 shadow-sm">
          {icon}
        </div>

        <span className="font-medium text-slate-700">
          {title}
        </span>

      </div>

      <span className="font-semibold text-slate-500">
        {value}
      </span>

    </div>
  );
}