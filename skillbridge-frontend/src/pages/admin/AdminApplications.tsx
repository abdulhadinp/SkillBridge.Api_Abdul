import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../../lib/axios";

interface Application {
  id: number;
  jobId: number;
  jobTitle: string;
  company: string;
  applicantId: number;
  applicantName: string;
  applicantEmail: string;
  status: string;
  appliedAt: string;
  coverLetter?: string;
}

const ALL_STATUSES = ["Applied", "Under Review", "Shortlisted", "Interview", "Hired", "Rejected"];

const statusColours: Record<string, string> = {
  Applied: "bg-blue-100 text-blue-800",
  "Under Review": "bg-yellow-100 text-yellow-800",
  Shortlisted: "bg-purple-100 text-purple-800",
  Interview: "bg-orange-100 text-orange-800",
  Hired: "bg-green-100 text-green-800",
  Rejected: "bg-red-100 text-red-800",
};

export default function AdminApplications() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState("");
  const [updatingId, setUpdatingId] = useState<number | null>(null);
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const fetchApplications = async () => {
    try {
      const params = filterStatus ? `?status=${filterStatus}` : "";
      const res = await api.get(`/application/all${params}`);
      setApplications(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, [filterStatus]);

  const updateStatus = async (id: number, newStatus: string) => {
    setUpdatingId(id);
    try {
      await api.put(`/application/${id}/status`, { status: newStatus });
      setApplications(apps => apps.map(a => a.id === id ? { ...a, status: newStatus } : a));
    } catch (err) {
      console.error(err);
    } finally {
      setUpdatingId(null);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-blue-600">SkillBridge</Link>
          <div className="flex items-center gap-6">
            <Link to="/admin/dashboard" className="text-gray-600 hover:text-blue-600">Dashboard</Link>
            <Link to="/admin/jobs/create" className="text-gray-600 hover:text-blue-600">Post Job</Link>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">All Applications</h1>
            <p className="text-gray-500 mt-1">{applications.length} applications found</p>
          </div>
          <select
            value={filterStatus}
            onChange={e => setFilterStatus(e.target.value)}
            className="px-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none bg-white"
          >
            <option value="">All Statuses</option>
            {ALL_STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>

        {loading ? (
          <div className="text-center py-16 text-gray-400">Loading applications...</div>
        ) : applications.length === 0 ? (
          <div className="bg-white rounded-xl p-12 text-center shadow-sm">
            <div className="text-5xl mb-4">📭</div>
            <h2 className="text-xl font-semibold text-gray-700">No applications found</h2>
          </div>
        ) : (
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200">
                  <th className="text-left p-4 text-xs font-semibold text-gray-500 uppercase tracking-wide">Candidate</th>
                  <th className="text-left p-4 text-xs font-semibold text-gray-500 uppercase tracking-wide">Job</th>
                  <th className="text-left p-4 text-xs font-semibold text-gray-500 uppercase tracking-wide">Applied</th>
                  <th className="text-left p-4 text-xs font-semibold text-gray-500 uppercase tracking-wide">Status</th>
                  <th className="text-left p-4 text-xs font-semibold text-gray-500 uppercase tracking-wide">Update Status</th>
                  <th className="text-left p-4 text-xs font-semibold text-gray-500 uppercase tracking-wide">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {applications.map(app => (
                  <>
                    <tr key={app.id} className="hover:bg-gray-50 transition-colors">
                      <td className="p-4">
                        <div className="font-medium text-gray-800">{app.applicantName}</div>
                        <div className="text-sm text-gray-400">{app.applicantEmail}</div>
                      </td>
                      <td className="p-4">
                        <div className="font-medium text-gray-800">{app.jobTitle}</div>
                        <div className="text-sm text-gray-400">{app.company}</div>
                      </td>
                      <td className="p-4 text-sm text-gray-500">
                        {new Date(app.appliedAt).toLocaleDateString("en-GB")}
                      </td>
                      <td className="p-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColours[app.status] || "bg-gray-100 text-gray-600"}`}>
                          {app.status}
                        </span>
                      </td>
                      <td className="p-4">
                        <select
                          value={app.status}
                          onChange={e => updateStatus(app.id, e.target.value)}
                          disabled={updatingId === app.id}
                          className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none disabled:opacity-50"
                        >
                          {ALL_STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
                        </select>
                      </td>
                      <td className="p-4">
                        <button
                          onClick={() => setExpandedId(expandedId === app.id ? null : app.id)}
                          className="text-blue-600 text-sm hover:underline"
                        >
                          {expandedId === app.id ? "Hide" : "Cover Letter"}
                        </button>
                      </td>
                    </tr>
                    {expandedId === app.id && app.coverLetter && (
                      <tr key={`${app.id}-expanded`}>
                        <td colSpan={6} className="px-4 pb-4">
                          <div className="bg-blue-50 border border-blue-100 rounded-xl p-4 text-sm text-gray-700 leading-relaxed">
                            <div className="font-semibold text-blue-700 mb-2">Cover Letter:</div>
                            {app.coverLetter}
                          </div>
                        </td>
                      </tr>
                    )}
                  </>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
