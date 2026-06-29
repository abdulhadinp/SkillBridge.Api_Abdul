using SkillBridge.Api.Models;

namespace SkillBridge.Api.IRepositories
{
    /// <summary>
    /// Interface demonstrating OOP Abstraction — hides implementation details
    /// of the application management logic behind a contract.
    /// </summary>
    public interface IApplicationRepository
    {
        Task<ApplicationResponseDto> SubmitApplicationAsync(SubmitApplicationRequestDto request);
        Task<IEnumerable<ApplicationResponseDto>> GetApplicationsByUserAsync(int userId);
        Task<IEnumerable<ApplicationResponseDto>> GetAllApplicationsAsync(int? jobId, string? status, DateTime? fromDate, DateTime? toDate);
        Task<ApplicationResponseDto?> GetApplicationByIdAsync(int id);
        Task<bool> UpdateApplicationStatusAsync(int id, string newStatus);
        Task<bool> HasAppliedAsync(int userId, int jobId);
        Task<IEnumerable<JobRecommendationDto>> GetRecommendedJobsAsync(int userId);
        Task<DashboardStatsDto> GetDashboardStatsAsync();
    }
}
