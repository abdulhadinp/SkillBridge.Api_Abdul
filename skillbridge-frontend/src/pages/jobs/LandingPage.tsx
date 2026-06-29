import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Search, MapPin, Briefcase, Loader2 } from "lucide-react";
import { publicApi } from "@/lib/axios";
import JobDetailModal from "@/components/jobs/JobDetailModal";
import { useAuth } from "@/context/AuthContext";

type Job = {
  id: number;
  title: string;
  company: string;
  location: string;
  jobType: string;
  minSalary: number;
  maxSalary: number;
  deadLineDate: string;
  description?: string;
};

export default function LandingPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { isAuthenticated, user, logout, isAdmin } = useAuth();

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        setLoading(true);
        const response = await publicApi.get<Job[]>("/api/Job");
        setJobs(response.data);
      } catch (error) {
        console.error("Error fetching jobs:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchJobs();
  }, []);

  const filteredJobs = jobs.filter(
    (job) =>
      job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      job.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
      job.location.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  const openJobDetails = (job: Job) => {
    setSelectedJob(job);
    setIsModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white shadow-sm border-b sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold text-blue-600">
            SkillBridge
          </Link>
          <div className="flex items-center gap-3">
            {isAuthenticated ? (
              <>
                <span className="text-sm text-gray-600">
                  Hi, {user?.fullName}
                </span>
                {isAdmin && (
                  <>
                    <Link to="/admin/dashboard">
                      <Button variant="outline" size="sm">
                        Dashboard
                      </Button>
                    </Link>
                    <Link to="/admin/jobs/create">
                      <Button variant="outline" size="sm">
                        Post Job
                      </Button>
                    </Link>
                  </>
                )}
                <Button variant="outline" size="sm" onClick={logout}>
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="outline" size="sm">
                    Login
                  </Button>
                </Link>
                <Link to="/register">
                  <Button size="sm">Register</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-20">
        <div className="max-w-6xl mx-auto text-center px-4">
          <h1 className="text-5xl font-bold mb-4">Find Your Dream Job</h1>
          <p className="text-xl mb-8">
            Discover opportunities that match your skills
          </p>

          <div className="max-w-md mx-auto relative">
            <Search className="absolute left-4 top-3.5 text-gray-400" />
            <Input
              placeholder="Search jobs, companies, or locations..."
              className="pl-12 py-6 text-lg bg-white text-gray-900"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
      </div>

      {/* Jobs Section */}
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-3xl font-semibold">
            {searchTerm ? "Search Results" : "Featured Jobs"}
          </h2>
          <span className="text-gray-500">{filteredJobs.length} jobs found</span>
        </div>

        {loading && (
          <div className="flex justify-center py-12">
            <Loader2 className="animate-spin w-8 h-8 text-blue-600" />
          </div>
        )}

        {!loading && filteredJobs.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <Briefcase className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p className="text-lg">No jobs found</p>
            <p className="text-sm">Try a different search or check back later</p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredJobs.map((job) => (
            <Card key={job.id} className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => openJobDetails(job)}>
              <CardHeader>
                <CardTitle className="text-lg">{job.title}</CardTitle>
                <CardDescription className="flex items-center gap-2">
                  <Briefcase className="w-4 h-4" /> {job.company}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <MapPin className="w-4 h-4" /> {job.location}
                  </div>

                  <div className="flex gap-2 flex-wrap">
                    <Badge variant="secondary">{job.jobType}</Badge>
                    <Badge variant="outline">
                      NPR {job.minSalary.toLocaleString()} -{" "}
                      {job.maxSalary.toLocaleString()}
                    </Badge>
                  </div>

                  <p className="text-sm text-gray-500">
                    Deadline: {new Date(job.deadLineDate).toLocaleDateString()}
                  </p>

                  <Button className="w-full mt-4">View Details</Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      <JobDetailModal
        job={selectedJob}
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
}
