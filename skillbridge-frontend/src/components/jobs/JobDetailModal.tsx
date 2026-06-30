import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/context/AuthContext";
import { useNavigate } from "react-router-dom";

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

type JobDetailModalProps = {
  job: Job | null;
  open: boolean;
  onClose: () => void;
};

export default function JobDetailModal({
  job,
  open,
  onClose,
}: JobDetailModalProps) {
  const { isAuthenticated, isJobSeeker } = useAuth();
  const navigate = useNavigate();

  const handleApply = () => {
    if (!isAuthenticated) {
      alert("Please login to apply for this job.");
      navigate("/login");
      onClose();
      return;
    }

    if (!isJobSeeker) {
      alert("Only Job Seekers can apply for jobs.");
      return;
    }

    navigate(`/jobs/${job?.id}/apply`);
    onClose();
  };

  if (!job) return null;

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl">{job.title}</DialogTitle>
          <DialogDescription className="text-lg font-medium text-gray-700">
            {job.company} - {job.location}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          <div className="flex gap-3">
            <Badge variant="secondary">{job.jobType}</Badge>
            <Badge variant="outline">
              NPR {job.minSalary.toLocaleString()} -{" "}
              {job.maxSalary.toLocaleString()}
            </Badge>
          </div>

          <div>
            <h3 className="font-semibold mb-2">Job Description</h3>
            <p className="text-gray-600 leading-relaxed">
              {job.description || "No detailed description available."}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <strong>Location:</strong> {job.location}
            </div>
            <div>
              <strong>Deadline:</strong>{" "}
              {new Date(job.deadLineDate).toLocaleDateString()}
            </div>
          </div>
        </div>

        <div className="flex gap-3 pt-4 border-t">
          <Button variant="outline" className="flex-1" onClick={onClose}>
            Close
          </Button>
          <Button className="flex-1" onClick={handleApply}>
            Apply Now
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
