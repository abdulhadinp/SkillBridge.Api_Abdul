import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import api from "../../lib/axios";

interface Profile {
  fullName: string;
  email: string;
  phoneNumber: string;
  experience: string;
  skills: string;
  education: string;
  summary: string;
  linkedInProfile: string;
  gitHubProfile: string;
  resumePath: string;
}

export default function CandidateProfile() {
  const { user } = useAuth();
  const [profile, setProfile] = useState<Partial<Profile>>({});
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess(false);

    try {
      const formData = new FormData();
      Object.entries(profile).forEach(([k, v]) => { if (v) formData.append(k, v); });
      if (resumeFile) formData.append("resume", resumeFile);

      await api.post("/user/profile/create", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSuccess(true);
    } catch {
      setError("Failed to save profile. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const completionFields = ["fullName", "skills", "experience", "education", "summary", "resumePath"];
  const filled = completionFields.filter(f => profile[f as keyof Profile]);
  const completion = Math.round((filled.length / completionFields.length) * 100);

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-blue-600">SkillBridge</Link>
          <div className="flex items-center gap-6">
            <Link to="/" className="text-gray-600 hover:text-blue-600">Find Jobs</Link>
            <Link to="/candidate/dashboard" className="text-gray-600 hover:text-blue-600">Dashboard</Link>
            <Link to="/candidate/applications" className="text-gray-600 hover:text-blue-600">My Applications</Link>
          </div>
        </div>
      </nav>

      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
          <div className="text-right">
            <div className="text-sm text-gray-500 mb-1">Profile Completion</div>
            <div className="flex items-center gap-2">
              <div className="w-32 h-2 bg-gray-200 rounded-full">
                <div
                  className="h-2 bg-blue-500 rounded-full transition-all"
                  style={{ width: `${completion}%` }}
                />
              </div>
              <span className="text-sm font-semibold text-blue-600">{completion}%</span>
            </div>
          </div>
        </div>

        {success && (
          <div className="mb-4 p-4 bg-green-50 border border-green-200 text-green-700 rounded-xl">
            ✅ Profile saved successfully!
          </div>
        )}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-6 border-b border-gray-100 bg-gradient-to-r from-blue-50 to-indigo-50">
            <h2 className="text-lg font-semibold text-gray-800">Personal Information</h2>
          </div>
          <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
            {[
              { name: "fullName", label: "Full Name", type: "text", placeholder: "Your full name" },
              { name: "email", label: "Email Address", type: "email", placeholder: "your@email.com" },
              { name: "phoneNumber", label: "Phone Number", type: "tel", placeholder: "+977 98XXXXXXXX" },
            ].map(field => (
              <div key={field.name}>
                <label className="block text-sm font-medium text-gray-700 mb-1">{field.label}</label>
                <input
                  type={field.type}
                  name={field.name}
                  value={profile[field.name as keyof Profile] || ""}
                  onChange={handleChange}
                  placeholder={field.placeholder}
                  className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                />
              </div>
            ))}

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Skills <span className="text-gray-400 text-xs">(comma-separated, e.g., C#, React, SQL)</span>
              </label>
              <input
                type="text"
                name="skills"
                value={profile.skills || ""}
                onChange={handleChange}
                placeholder="C#, ASP.NET, React, SQL Server"
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">Experience Summary</label>
              <textarea
                name="experience"
                value={profile.experience || ""}
                onChange={handleChange}
                rows={3}
                placeholder="Describe your professional experience..."
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all resize-none"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">Education</label>
              <textarea
                name="education"
                value={profile.education || ""}
                onChange={handleChange}
                rows={2}
                placeholder="e.g., BSc Computer Science, ISMT College, 2024"
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all resize-none"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">Professional Summary</label>
              <textarea
                name="summary"
                value={profile.summary || ""}
                onChange={handleChange}
                rows={3}
                placeholder="A brief summary of your professional background..."
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all resize-none"
              />
            </div>

            {[
              { name: "linkedInProfile", label: "LinkedIn Profile URL", placeholder: "https://linkedin.com/in/..." },
              { name: "gitHubProfile", label: "GitHub Profile URL", placeholder: "https://github.com/..." },
            ].map(field => (
              <div key={field.name}>
                <label className="block text-sm font-medium text-gray-700 mb-1">{field.label}</label>
                <input
                  type="url"
                  name={field.name}
                  value={profile[field.name as keyof Profile] || ""}
                  onChange={handleChange}
                  placeholder={field.placeholder}
                  className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                />
              </div>
            ))}

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">CV / Resume (PDF only)</label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={e => setResumeFile(e.target.files?.[0] || null)}
                  className="hidden"
                  id="resume-upload"
                />
                <label htmlFor="resume-upload" className="cursor-pointer">
                  <div className="text-3xl mb-2">📄</div>
                  {resumeFile ? (
                    <p className="text-blue-600 font-medium">{resumeFile.name}</p>
                  ) : (
                    <>
                      <p className="text-gray-600 font-medium">Click to upload your CV/Resume</p>
                      <p className="text-gray-400 text-sm">PDF format only, max 5MB</p>
                    </>
                  )}
                </label>
              </div>
            </div>
          </div>

          <div className="p-6 border-t border-gray-100 bg-gray-50">
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 disabled:opacity-50 transition-all"
            >
              {loading ? "Saving..." : "Save Profile"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
