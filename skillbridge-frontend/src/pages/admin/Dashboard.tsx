import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Loader2, Plus, Briefcase, Users, MapPin } from "lucide-react";
import { publicApi } from "@/lib/axios";
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
  isActive: boolean;
  postedByUserId: number;
};

export default function AdminDashboard() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const { user, logout } = useAuth();

  useEffect(() => {
    const fetchJobs = async () => {
      try {
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

  const myJobs = jobs.filter((j) => j.postedByUserId === user?.id);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white shadow-sm border-b sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold text-blue-600">
            SkillBridge
          </Link>
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-600">Admin: {user?.fullName}</span>
            <Link to="/">
              <Button variant="outline" size="sm">View Jobs</Button>
            </Link>
            <Button variant="outline" size="sm" onClick={logout}>
              Logout
            </Button>
          </div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">Admin Dashboard</h1>
          <Link to="/admin/jobs/create">
            <Button>
              <Plus className="w-4 h-4 mr-2" /> Post New Job
            </Button>
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-blue-100 rounded-lg">
                  <Briefcase className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold">{jobs.length}</p>
                  <p className="text-sm text-gray-500">Total Jobs</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-green-100 rounded-lg">
                  <Users className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold">{myJobs.length}</p>
                  <p className="text-sm text-gray-500">My Posted Jobs</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-purple-100 rounded-lg">
                  <MapPin className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold">{jobs.filter(j => j.isActive).length}</p>
                  <p className="text-sm text-gray-500">Active Listings</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* My Jobs */}
        <h2 className="text-xl font-semibold mb-4">My Posted Jobs</h2>
        {loading && (
          <div className="flex justify-center py-8">
            <Loader2 className="animate-spin w-6 h-6 text-blue-600" />
          </div>
        )}

        {!loading && myJobs.length === 0 && (
          <Card>
            <CardContent className="py-8 text-center text-gray-500">
              <p>You haven't posted any jobs yet.</p>
              <Link to="/admin/jobs/create">
                <Button className="mt-4">Post Your First Job</Button>
              </Link>
            </CardContent>
          </Card>
        )}

        <div className="space-y-4">
          {myJobs.map((job) => (
            <Card key={job.id}>
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">{job.title}</CardTitle>
                  <Badge variant={job.isActive ? "default" : "secondary"}>
                    {job.isActive ? "Active" : "Closed"}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-6 text-sm text-gray-600">
                  <span>{job.company}</span>
                  <span>{job.location}</span>
                  <span>{job.jobType}</span>
                  <span>
                    NPR {job.minSalary.toLocaleString()} - {job.maxSalary.toLocaleString()}
                  </span>
                  <span>Deadline: {new Date(job.deadLineDate).toLocaleDateString()}</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* All Jobs */}
        {jobs.length > myJobs.length && (
          <>
            <h2 className="text-xl font-semibold mt-8 mb-4">All Jobs on Platform</h2>
            <div className="space-y-4">
              {jobs.filter(j => j.postedByUserId !== user?.id).map((job) => (
                <Card key={job.id} className="opacity-75">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-lg">{job.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center gap-6 text-sm text-gray-600">
                      <span>{job.company}</span>
                      <span>{job.location}</span>
                      <span>{job.jobType}</span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
