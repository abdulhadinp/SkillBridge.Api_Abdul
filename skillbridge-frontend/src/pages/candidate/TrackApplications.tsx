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
  coverLetter?: string;
}

const statusColours: Record<string, string> = {
  Applied: "bg-blue-100 text-blue-800",
  "Under Review": "bg-yellow-100 text-yellow-800",
  Shortlisted: "bg-purple-100 text-purple-800",
  Interview: "bg-orange-100 text-orange-800",
  Hired: "bg-green-100 text-green-800",
  Rejected: "bg-red-100 text-red-800",
};

const statusOrder = ["Applied", "Under Review", "Shortlisted", "Interview", "Hired"];

export default function TrackApplications() {
  const { user } = useAuth();
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/application/my")
      .then(res => setApplications(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-blue-600">SkillBridge</Link>
          <div className="flex items-center gap-6">
            <Link to="/" className="text-gray-600 hover:text-blue-600">Find Jobs</Link>
            <Link to="/candidate/dashboard" className="text-gray-600 hover:text-blue-600">Dashboard</Link>
            <Link to="/candidate/profile" className="text-gray-600 hover:text-blue-600">Profile</Link>
          </div>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Applications</h1>
          <p className="text-gray-500 mt-1">Track the status of all your job applications.</p>
        </div>

        {loading ? (
          <div className="text-center py-16 text-gray-400">Loading your applications...</div>
        ) : applications.length === 0 ? (
          <div className="bg-white rounded-xl p-12 text-center shadow-sm">
            <div className="text-5xl mb-4">📋</div>
            <h2 className="text-xl font-semibold text-gray-700 mb-2">No applications yet</h2>
            <p className="text-gray-500 mb-6">Start applying for jobs to track your progress here.</p>
            <Link to="/" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">Browse Jobs</Link>
          </div>
        ) : (
          <div className="space-y-4">
            {applications.map(app => {
              const isRejected = app.status === "Rejected";
              return (
                <div key={app.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h3 className="text-lg font-bold text-gray-800">{app.jobTitle}</h3>
                        <p className="text-gray-500 text-sm">{app.company}</p>
                        <p className="text-gray-400 text-xs mt-1">Applied on {new Date(app.appliedAt).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}</p>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColours[app.status] || "bg-gray-100 text-gray-600"}`}>
                        {app.status}
                      </span>
                    </div>

                    {/* Progress Bar */}
                    {!isRejected && (
                      <div className="mt-4">
                        <div className="flex items-center gap-1">
                          {statusOrder.map((s, i) => {
                            const currentIdx = statusOrder.indexOf(app.status);
                            const isActive = i <= currentIdx;
                            return (
                              <div key={s} className="flex items-center flex-1">
                                <div className={`w-full h-2 rounded-full transition-all ${isActive ? "bg-blue-500" : "bg-gray-200"}`} />
                              </div>
                            );
                          })}
                        </div>
                        <div className="flex justify-between mt-1">
                          {statusOrder.map(s => (
                            <span key={s} className={`text-xs ${app.status === s ? "text-blue-600 font-semibold" : "text-gray-400"}`} style={{ flex: 1, textAlign: "center" }}>{s}</span>
                          ))}
                        </div>
                      </div>
                    )}
                    {isRejected && (
                      <div className="mt-3 p-3 bg-red-50 border border-red-100 rounded-lg text-sm text-red-600">
                        ❌ This application was not selected. Keep applying — the right opportunity is out there!
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
