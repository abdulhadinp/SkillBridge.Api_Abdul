import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import api from "../../lib/axios";

interface Application {
  id: number;
  jobId: number;
  jobTitle: string;
  company: string;
  status: string;
  appliedAt: string;
}

interface RecommendedJob {
  id: number;
  title: string;
  company: string;
  location: string;
  jobType: string;
  minSalary: number;
  maxSalary: number;
  matchedSkill: string;
}

const statusColours: Record<string, string> = {
  Applied: "bg-blue-100 text-blue-800",
  "Under Review": "bg-yellow-100 text-yellow-800",
  Shortlisted: "bg-purple-100 text-purple-800",
  Interview: "bg-orange-100 text-orange-800",
  Hired: "bg-green-100 text-green-800",
  Rejected: "bg-red-100 text-red-800",
};

export default function CandidateDashboard() {
  const { user } = useAuth();
  const [applications, setApplications] = useState<Application[]>([]);
  const [recommendations, setRecommendations] = useState<RecommendedJob[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [appsRes, recsRes] = await Promise.all([
          api.get("/application/my"),
          api.get("/application/recommendations"),
        ]);
        setApplications(appsRes.data);
        setRecommendations(recsRes.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-blue-600">SkillBridge</Link>
          <div className="flex items-center gap-6">
            <Link to="/" className="text-gray-600 hover:text-blue-600 transition-colors">Find Jobs</Link>
            <Link to="/candidate/applications" className="text-gray-600 hover:text-blue-600 transition-colors">My Applications</Link>
            <Link to="/candidate/profile" className="text-gray-600 hover:text-blue-600 transition-colors">Profile</Link>
            <span className="text-sm text-gray-500">Hello, {user?.fullName}</span>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Banner */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-8 text-white mb-8 shadow-lg">
          <h1 className="text-3xl font-bold mb-2">Welcome back, {user?.fullName}! 👋</h1>
          <p className="text-blue-100">Track your applications and discover new opportunities.</p>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 text-center">
            <div className="text-4xl font-bold text-blue-600">{applications.length}</div>
            <div className="text-gray-500 mt-1">Total Applications</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 text-center">
            <div className="text-4xl font-bold text-green-600">
              {applications.filter(a => a.status === "Hired").length}
            </div>
            <div className="text-gray-500 mt-1">Successful Hires</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 text-center">
            <div className="text-4xl font-bold text-orange-500">
              {applications.filter(a => ["Shortlisted", "Interview"].includes(a.status)).length}
            </div>
            <div className="text-gray-500 mt-1">In Progress</div>
          </div>
        </div>

        {/* Recent Applications */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 mb-8">
          <div className="p-6 border-b border-gray-100 flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-800">Recent Applications</h2>
            <Link to="/candidate/applications" className="text-blue-600 text-sm hover:underline">View all →</Link>
          </div>
          {loading ? (
            <div className="p-8 text-center text-gray-400">Loading...</div>
          ) : applications.length === 0 ? (
            <div className="p-8 text-center">
              <p className="text-gray-500 mb-4">You haven't applied for any jobs yet.</p>
              <Link to="/" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors">Browse Jobs</Link>
            </div>
          ) : (
            <div className="divide-y divide-gray-50">
              {applications.slice(0, 5).map(app => (
                <div key={app.id} className="p-6 flex items-center justify-between hover:bg-gray-50 transition-colors">
                  <div>
                    <div className="font-semibold text-gray-800">{app.jobTitle}</div>
                    <div className="text-sm text-gray-500">{app.company}</div>
                    <div className="text-xs text-gray-400 mt-1">Applied {new Date(app.appliedAt).toLocaleDateString("en-GB")}</div>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColours[app.status] || "bg-gray-100 text-gray-600"}`}>
                    {app.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* AI Recommendations */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="p-6 border-b border-gray-100">
            <div className="flex items-center gap-2">
              <span className="text-2xl">🤖</span>
              <h2 className="text-xl font-bold text-gray-800">AI-Powered Job Recommendations</h2>
              <span className="ml-2 px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full font-medium">Beta</span>
            </div>
            <p className="text-sm text-gray-500 mt-1">Matched against your skills profile using keyword analysis.</p>
          </div>
          {recommendations.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              <p>No recommendations yet. <Link to="/candidate/profile" className="text-blue-600 hover:underline">Complete your profile</Link> to get personalised job matches.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6">
              {recommendations.map(job => (
                <Link key={job.id} to={`/jobs/${job.id}`} className="block border border-gray-200 rounded-xl p-4 hover:shadow-md hover:border-blue-300 transition-all">
                  <div className="flex items-start justify-between mb-2">
                    <span className="text-xs px-2 py-0.5 bg-blue-50 text-blue-600 rounded-full font-medium">{job.jobType}</span>
                    <span className="text-xs text-green-600 font-medium">Matched: {job.matchedSkill}</span>
                  </div>
                  <h3 className="font-semibold text-gray-800 mb-1">{job.title}</h3>
                  <p className="text-sm text-gray-500">{job.company}</p>
                  <p className="text-sm text-gray-400">{job.location}</p>
                  <div className="mt-2 text-sm font-medium text-gray-700">
                    NPR {job.minSalary.toLocaleString()} – {job.maxSalary.toLocaleString()}
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
