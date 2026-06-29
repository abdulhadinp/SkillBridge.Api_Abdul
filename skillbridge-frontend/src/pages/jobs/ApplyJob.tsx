import { useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import api from "../../lib/axios";

export default function ApplyJob() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [coverLetter, setCoverLetter] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("jobId", id!);
      formData.append("coverLetter", coverLetter);
      if (resumeFile) formData.append("resume", resumeFile);

      await api.post("/application/apply", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSuccess(true);
    } catch (err: any) {
      setError(err.response?.data?.message || "Failed to submit application. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-lg p-8 text-center">
          <div className="text-6xl mb-4">🎉</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Application Submitted!</h2>
          <p className="text-gray-500 mb-6">Your application has been successfully submitted. The employer will review it and update your status.</p>
          <div className="flex gap-3 justify-center">
            <Link to="/candidate/applications" className="bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold hover:bg-blue-700 transition-all">
              Track Application
            </Link>
            <Link to="/" className="border border-gray-300 text-gray-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-50 transition-all">
              Find More Jobs
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-blue-600">SkillBridge</Link>
        </div>
      </nav>

      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Link to={`/jobs/${id}`} className="text-blue-600 hover:underline text-sm mb-4 inline-block">← Back to job detail</Link>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
            <h1 className="text-2xl font-bold">Submit Your Application</h1>
            <p className="text-blue-100 mt-1">Complete the form below to apply for this position.</p>
          </div>

          <form onSubmit={handleSubmit} className="p-6 space-y-6">
            {error && (
              <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl text-sm">
                {error}
              </div>
            )}

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Cover Letter <span className="text-red-500">*</span>
              </label>
              <textarea
                required
                value={coverLetter}
                onChange={e => setCoverLetter(e.target.value)}
                rows={8}
                placeholder="Write a compelling cover letter explaining why you are the ideal candidate for this position. Mention your relevant experience, skills, and what motivates you to apply..."
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all resize-none text-sm"
              />
              <div className="text-xs text-gray-400 mt-1 text-right">{coverLetter.length} characters</div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Tailored Resume (Optional) <span className="text-gray-400 text-xs font-normal">PDF only</span>
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-blue-400 transition-colors">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={e => setResumeFile(e.target.files?.[0] || null)}
                  className="hidden"
                  id="tailored-resume"
                />
                <label htmlFor="tailored-resume" className="cursor-pointer">
                  <div className="text-3xl mb-2">📄</div>
                  {resumeFile ? (
                    <p className="text-blue-600 font-medium">{resumeFile.name}</p>
                  ) : (
                    <>
                      <p className="text-gray-600 font-medium">Upload a tailored resume</p>
                      <p className="text-gray-400 text-sm">If you have a resume tailored to this role</p>
                    </>
                  )}
                </label>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading || !coverLetter.trim()}
              className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md"
            >
              {loading ? "Submitting..." : "Submit Application →"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
