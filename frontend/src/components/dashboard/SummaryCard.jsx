import { motion } from "framer-motion";
import {
  Sparkles,
  CircleAlert,
  BadgeCheck,
  ClipboardList,
  Smile,
  Brain,
} from "lucide-react";

export default function SummaryCard() {
  return (
    <motion.div
      whileHover={{ y: -6 }}
      transition={{ duration: 0.25 }}
      className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white p-7 shadow-sm hover:shadow-xl"
    >
      {/* Background Glow */}
      <div className="absolute -right-20 -top-20 h-60 w-60 rounded-full bg-violet-200/40 blur-3xl"></div>

      <div className="relative z-10">

        {/* Header */}

        <div className="flex items-center justify-between">

          <div className="flex items-center gap-3">

            <div className="rounded-2xl bg-gradient-to-r from-indigo-600 to-violet-600 p-3 shadow">

              <Brain className="text-white" />

            </div>

            <div>

              <h2 className="text-2xl font-bold text-slate-800">
                AI Summary
              </h2>

              <p className="text-slate-500">
                Generated using VoiceOps AI
              </p>

            </div>

          </div>

          <span className="rounded-full bg-indigo-100 px-3 py-1 text-xs font-semibold text-indigo-700">
            AI Powered
          </span>

        </div>

        {/* Summary */}

        <Card
          color="bg-indigo-50"
          icon={<Sparkles className="text-indigo-600" size={18} />}
          title="Conversation Summary"
        >
          Customer contacted support regarding a failed online payment.
          The support representative verified the transaction and initiated
          the refund process successfully.
        </Card>

        {/* Issue */}

        <Card
          color="bg-red-50"
          icon={<CircleAlert className="text-red-500" size={18} />}
          title="Customer Issue"
        >
          Payment amount was deducted but order was not confirmed.
        </Card>

        {/* Resolution */}

        <Card
          color="bg-green-50"
          icon={<BadgeCheck className="text-green-600" size={18} />}
          title="Resolution"
        >
          Refund request created and customer informed about the processing
          timeline.
        </Card>

        {/* Action */}

        <Card
          color="bg-amber-50"
          icon={<ClipboardList className="text-amber-600" size={18} />}
          title="Recommended Next Action"
        >
          Send confirmation email and monitor payment gateway logs.
        </Card>

        {/* Bottom Metrics */}

        <div className="mt-8 grid grid-cols-3 gap-4">

          <Metric
            icon={<Smile className="text-green-600" />}
            label="Sentiment"
            value="Positive"
          />

          <Metric
            icon={<Brain className="text-indigo-600" />}
            label="Confidence"
            value="98%"
          />

          <Metric
            icon={<Sparkles className="text-violet-600" />}
            label="Keywords"
            value="12"
          />

        </div>

      </div>

    </motion.div>
  );
}

function Card({ icon, title, children, color }) {
  return (
    <div className={`${color} mt-6 rounded-2xl p-5`}>

      <div className="flex items-center gap-2">

        {icon}

        <h3 className="font-semibold text-slate-800">
          {title}
        </h3>

      </div>

      <p className="mt-3 text-slate-600 leading-7">
        {children}
      </p>

    </div>
  );
}

function Metric({ icon, label, value }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-center">

      <div className="flex justify-center">

        {icon}

      </div>

      <p className="mt-3 text-sm text-slate-500">
        {label}
      </p>

      <h3 className="mt-1 text-lg font-bold text-slate-800">
        {value}
      </h3>

    </div>
  );
}