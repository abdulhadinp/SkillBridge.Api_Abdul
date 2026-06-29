import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import api from "../../lib/axios";

interface Job {
  id: number;
  title: string;
  description: string;
  company: string;
  location: string;
  jobType: string;
  minSalary: number;
  maxSalary: number;
  deadLineDate: string;
  postedDate: string;
}

export default function JobDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [job, setJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);
  const [hasApplied, setHasApplied] = useState(false);

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const res = await api.get(`/job/${id}`);
        setJob(res.data);
        if (isAuthenticated) {
          const checkRes = await api.get(`/application/check/${id}`);
          setHasApplied(checkRes.data.hasApplied);
        }
      } catch {
        navigate("/");
      } finally {
        setLoading(false);
      }
    };
    fetchJob();
  }, [id, isAuthenticated]);

  if (loading) return <div className="min-h-screen flex items-center justify-center text-gray-400">Loading...</div>;
  if (!job) return null;

  const deadline = new Date(job.deadLineDate);
  const isExpired = deadline < new Date();

  const jobTypeColours: Record<string, string> = {
    IT: "bg-blue-100 text-blue-700",
    Accounting: "bg-green-100 text-green-700",
    Teaching: "bg-purple-100 text-purple-700",
    Management: "bg-orange-100 text-orange-700",
    Other: "bg-gray-100 text-gray-700",
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-blue-600">SkillBridge</Link>
          <div className="flex items-center gap-4">
            {isAuthenticated ? (
              <Link to="/candidate/dashboard" className="text-gray-600 hover:text-blue-600">Dashboard</Link>
            ) : (
              <>
                <Link to="/login" className="text-gray-600 hover:text-blue-600">Login</Link>
                <Link to="/register" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">Register</Link>
              </>
            )}
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Link to="/" className="text-blue-600 hover:underline text-sm mb-4 inline-block">← Back to jobs</Link>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          {/* Header */}
          <div className="p-8 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-3 mb-3">
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold bg-white/20 text-white`}>
                    {job.jobType}
                  </span>
                  {isExpired && <span className="px-3 py-1 rounded-full text-xs font-semibold bg-red-400/30 text-white">Closed</span>}
                </div>
                <h1 className="text-3xl font-bold mb-2">{job.title}</h1>
                <p className="text-blue-100 text-lg">{job.company}</p>
                <p className="text-blue-200 mt-1">📍 {job.location}</p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold">NPR {job.minSalary.toLocaleString()}</div>
                <div className="text-blue-100">– {job.maxSalary.toLocaleString()}</div>
                <div className="text-blue-200 text-sm mt-2">per month</div>
              </div>
            </div>
          </div>

          {/* Details */}
          <div className="p-8">
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8 p-4 bg-gray-50 rounded-xl">
              <div>
                <div className="text-xs text-gray-400 uppercase tracking-wide">Job Type</div>
                <div className="font-semibold text-gray-800 mt-1">{job.jobType}</div>
              </div>
              <div>
                <div className="text-xs text-gray-400 uppercase tracking-wide">Location</div>
                <div className="font-semibold text-gray-800 mt-1">{job.location}</div>
              </div>
              <div>
                <div className="text-xs text-gray-400 uppercase tracking-wide">Deadline</div>
                <div className={`font-semibold mt-1 ${isExpired ? "text-red-600" : "text-gray-800"}`}>
                  {deadline.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
                </div>
              </div>
            </div>

            <h2 className="text-xl font-bold text-gray-800 mb-4">Job Description</h2>
            <div className="text-gray-600 leading-relaxed whitespace-pre-wrap">{job.description}</div>

            {/* Apply Section */}
            <div className="mt-8 p-6 border border-gray-200 rounded-xl bg-blue-50">
              <h3 className="text-lg font-bold text-gray-800 mb-2">Ready to apply?</h3>
              {isExpired ? (
                <p className="text-red-500 font-medium">This job posting has expired.</p>
              ) : hasApplied ? (
                <div className="flex items-center gap-2 text-green-600 font-medium">
                  <span className="text-2xl">✅</span>
                  <span>You have already applied for this position.</span>
                </div>
              ) : isAuthenticated ? (
                <Link
                  to={`/jobs/${job.id}/apply`}
                  className="inline-block bg-blue-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-blue-700 transition-all shadow-md hover:shadow-lg"
                >
                  Apply Now →
                </Link>
              ) : (
                <div>
                  <p className="text-gray-600 mb-3">You must be logged in to apply for this job.</p>
                  <Link
                    to="/login"
                    className="inline-block bg-blue-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-blue-700 transition-all"
                  >
                    Login to Apply
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
