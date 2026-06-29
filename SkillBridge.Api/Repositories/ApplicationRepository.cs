using Microsoft.EntityFrameworkCore;
using SkillBridge.Api.Entities;
using SkillBridge.Api.IRepositories;
using SkillBridge.Api.Models;

namespace SkillBridge.Api.Repositories
{
    /// <summary>
    /// ApplicationRepository implements IApplicationRepository — demonstrates OOP Polymorphism
    /// through interface-based implementation.
    /// All database access goes through Entity Framework Core (no raw SQL).
    /// </summary>
    public class ApplicationRepository : IApplicationRepository
    {
        private readonly SkillBridgeDbContext _context;
        private readonly ICurrentUserHelper _currentUserHelper;
        private readonly IFileUploadHelper _fileUploadHelper;

        public ApplicationRepository(
            SkillBridgeDbContext context,
            ICurrentUserHelper currentUserHelper,
            IFileUploadHelper fileUploadHelper)
        {
            _context = context;
            _currentUserHelper = currentUserHelper;
            _fileUploadHelper = fileUploadHelper;
        }

        /// <summary>
        /// Submits a new job application. Prevents duplicate applications.
        /// </summary>
        public async Task<ApplicationResponseDto> SubmitApplicationAsync(SubmitApplicationRequestDto request)
        {
            var userId = _currentUserHelper.userID;

            // Prevent duplicate applications
            var existing = await _context.JobApplications
                .FirstOrDefaultAsync(a => a.ApplicantId == userId && a.AppliedJobId == request.JobId && a.IsActive);
            if (existing != null)
            {
                throw new InvalidOperationException("You have already applied for this job.");
            }

            string? resumePath = null;
            if (request.Resume != null && request.Resume.Length > 0)
            {
                resumePath = await _fileUploadHelper.UploadFileAsync(request.Resume);
            }

            var application = new JobApplication
            {
                AppliedJobId = request.JobId,
                ApplicantId = userId,
                CoverLetter = request.CoverLetter,
                ResumePath = resumePath,
                TailoredResumePath = resumePath,
                Status = "Applied",
                AppliedAt = DateTime.UtcNow,
                IsActive = true
            };

            _context.JobApplications.Add(application);
            await _context.SaveChangesAsync();

            return await MapToDto(application);
        }

        /// <summary>
        /// Returns all applications submitted by a specific candidate.
        /// </summary>
        public async Task<IEnumerable<ApplicationResponseDto>> GetApplicationsByUserAsync(int userId)
        {
            var apps = await _context.JobApplications
                .Include(a => a.AppliedJob)
                .Include(a => a.Applicant)
                .Where(a => a.ApplicantId == userId && a.IsActive)
                .OrderByDescending(a => a.AppliedAt)
                .ToListAsync();

            return apps.Select(a => new ApplicationResponseDto
            {
                Id = a.Id,
                JobId = a.AppliedJobId,
                JobTitle = a.AppliedJob?.Title,
                Company = a.AppliedJob?.Company,
                ApplicantId = a.ApplicantId,
                ApplicantName = a.Applicant?.FullName,
                ApplicantEmail = a.Applicant?.Email,
                Status = a.Status,
                AppliedAt = a.AppliedAt,
                CoverLetter = a.CoverLetter,
                ResumePath = a.ResumePath,
                IsActive = a.IsActive
            });
        }

        /// <summary>
        /// Returns all applications (Admin use). Supports filtering by job, status, and date range.
        /// </summary>
        public async Task<IEnumerable<ApplicationResponseDto>> GetAllApplicationsAsync(
            int? jobId,
            string? status,
            DateTime? fromDate,
            DateTime? toDate)
        {
            var query = _context.JobApplications
                .Include(a => a.AppliedJob)
                .Include(a => a.Applicant)
                .Where(a => a.IsActive)
                .AsQueryable();

            if (jobId.HasValue)
                query = query.Where(a => a.AppliedJobId == jobId.Value);

            if (!string.IsNullOrWhiteSpace(status))
                query = query.Where(a => a.Status == status);

            if (fromDate.HasValue)
                query = query.Where(a => a.AppliedAt >= fromDate.Value);

            if (toDate.HasValue)
                query = query.Where(a => a.AppliedAt <= toDate.Value);

            var apps = await query.OrderByDescending(a => a.AppliedAt).ToListAsync();

            return apps.Select(a => new ApplicationResponseDto
            {
                Id = a.Id,
                JobId = a.AppliedJobId,
                JobTitle = a.AppliedJob?.Title,
                Company = a.AppliedJob?.Company,
                ApplicantId = a.ApplicantId,
                ApplicantName = a.Applicant?.FullName,
                ApplicantEmail = a.Applicant?.Email,
                Status = a.Status,
                AppliedAt = a.AppliedAt,
                CoverLetter = a.CoverLetter,
                ResumePath = a.ResumePath,
                IsActive = a.IsActive
            });
        }

        public async Task<ApplicationResponseDto?> GetApplicationByIdAsync(int id)
        {
            var a = await _context.JobApplications
                .Include(x => x.AppliedJob)
                .Include(x => x.Applicant)
                .FirstOrDefaultAsync(x => x.Id == id);

            if (a == null) return null;

            return new ApplicationResponseDto
            {
                Id = a.Id,
                JobId = a.AppliedJobId,
                JobTitle = a.AppliedJob?.Title,
                Company = a.AppliedJob?.Company,
                ApplicantId = a.ApplicantId,
                ApplicantName = a.Applicant?.FullName,
                ApplicantEmail = a.Applicant?.Email,
                Status = a.Status,
                AppliedAt = a.AppliedAt,
                CoverLetter = a.CoverLetter,
                ResumePath = a.ResumePath,
                IsActive = a.IsActive
            };
        }

        /// <summary>
        /// Updates application status through the defined workflow:
        /// Applied → Under Review → Shortlisted → Interview → Hired / Rejected
        /// </summary>
        public async Task<bool> UpdateApplicationStatusAsync(int id, string newStatus)
        {
            var validStatuses = new[] { "Applied", "Under Review", "Shortlisted", "Interview", "Hired", "Rejected" };
            if (!validStatuses.Contains(newStatus))
                return false;

            var app = await _context.JobApplications.FindAsync(id);
            if (app == null) return false;

            app.Status = newStatus;
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<bool> HasAppliedAsync(int userId, int jobId)
        {
            return await _context.JobApplications
                .AnyAsync(a => a.ApplicantId == userId && a.AppliedJobId == jobId && a.IsActive);
        }

        /// <summary>
        /// AI Job Recommendation — keyword matching between candidate skills and job descriptions.
        /// Jobs are recommended when any skill keyword appears in the job title or description.
        /// </summary>
        public async Task<IEnumerable<JobRecommendationDto>> GetRecommendedJobsAsync(int userId)
        {
            var profile = await _context.CandidateProfiles
                .FirstOrDefaultAsync(p => p.UserId == userId);

            if (profile == null || string.IsNullOrWhiteSpace(profile.Skills))
                return Enumerable.Empty<JobRecommendationDto>();

            var skills = profile.Skills
                .Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
                .Select(s => s.ToLower())
                .ToList();

            var activeJobs = await _context.Jobs
                .Where(j => j.IsActive && j.DeadLineDate >= DateTime.UtcNow)
                .ToListAsync();

            var recommendations = new List<JobRecommendationDto>();
            foreach (var job in activeJobs)
            {
                var matchedSkill = skills.FirstOrDefault(skill =>
                    (job.Title?.ToLower().Contains(skill) ?? false) ||
                    (job.Description?.ToLower().Contains(skill) ?? false) ||
                    (job.JobType?.ToLower().Contains(skill) ?? false));

                if (matchedSkill != null)
                {
                    recommendations.Add(new JobRecommendationDto
                    {
                        Id = job.Id,
                        Title = job.Title,
                        Company = job.Company,
                        Location = job.Location,
                        JobType = job.JobType,
                        MinSalary = job.MinSalary,
                        MaxSalary = job.MaxSalary,
                        DeadLineDate = job.DeadLineDate,
                        MatchedSkill = matchedSkill
                    });
                }
            }

            return recommendations.Take(5);
        }

        public async Task<DashboardStatsDto> GetDashboardStatsAsync()
        {
            return new DashboardStatsDto
            {
                TotalJobs = await _context.Jobs.CountAsync(),
                ActiveJobs = await _context.Jobs.CountAsync(j => j.IsActive),
                TotalApplications = await _context.JobApplications.CountAsync(a => a.IsActive),
                PendingApplications = await _context.JobApplications
                    .CountAsync(a => a.IsActive && (a.Status == "Applied" || a.Status == "Under Review")),
                TotalCandidates = await _context.Users
                    .CountAsync(u => u.IsActive && (u.Role == "Candidate" || u.Type == "Candidate"))
            };
        }

        private Task<ApplicationResponseDto> MapToDto(JobApplication a)
        {
            return Task.FromResult(new ApplicationResponseDto
            {
                Id = a.Id,
                JobId = a.AppliedJobId,
                ApplicantId = a.ApplicantId,
                Status = a.Status,
                AppliedAt = a.AppliedAt,
                CoverLetter = a.CoverLetter,
                ResumePath = a.ResumePath,
                IsActive = a.IsActive
            });
        }
    }
}
