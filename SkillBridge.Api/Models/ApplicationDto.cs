namespace SkillBridge.Api.Models
{
    public class SubmitApplicationRequestDto
    {
        public int JobId { get; set; }
        public string? CoverLetter { get; set; }
        public IFormFile? Resume { get; set; }
    }

    public class ApplicationResponseDto
    {
        public int Id { get; set; }
        public int JobId { get; set; }
        public string? JobTitle { get; set; }
        public string? Company { get; set; }
        public int ApplicantId { get; set; }
        public string? ApplicantName { get; set; }
        public string? ApplicantEmail { get; set; }
        public string? Status { get; set; }
        public DateTime AppliedAt { get; set; }
        public string? CoverLetter { get; set; }
        public string? ResumePath { get; set; }
        public bool IsActive { get; set; }
    }

    public class UpdateApplicationStatusDto
    {
        public string Status { get; set; } = string.Empty;
    }

    public class JobRecommendationDto
    {
        public int Id { get; set; }
        public string? Title { get; set; }
        public string? Company { get; set; }
        public string? Location { get; set; }
        public string? JobType { get; set; }
        public decimal MinSalary { get; set; }
        public decimal MaxSalary { get; set; }
        public DateTime DeadLineDate { get; set; }
        public string? MatchedSkill { get; set; }
    }

    public class DashboardStatsDto
    {
        public int TotalJobs { get; set; }
        public int ActiveJobs { get; set; }
        public int TotalApplications { get; set; }
        public int PendingApplications { get; set; }
        public int TotalCandidates { get; set; }
    }
}
