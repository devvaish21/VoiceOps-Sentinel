import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";
import Hero from "../components/dashboard/Hero";
import StatsCards from "../components/dashboard/StatsCards";
import UploadCard from "../components/dashboard/UploadCard";
import AudioPlayer from "../components/dashboard/AudioPlayer";
import Transcript from "../components/dashboard/Transcript";
import SummaryCard from "../components/dashboard/SummaryCard";
import SentimentCard from "../components/dashboard/SentimentCard";
import ActionItems from "../components/dashboard/ActionItems";
import PIICard from "../components/dashboard/PIICard";
import RecentCalls from "../components/dashboard/RecentCalls";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-slate-50 flex">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <main className="p-8 space-y-8">

  <Hero />

  <StatsCards />

  <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
    <UploadCard />
    <AudioPlayer />
  </div>

  <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
    <Transcript />
    <SummaryCard />
  </div>

  <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
    <SentimentCard />
    <ActionItems />
  </div>

  <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
    <PIICard />
    <RecentCalls />
  </div>

</main>

      </div>

    </div>
  );
}