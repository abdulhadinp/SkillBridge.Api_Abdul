using SkillBridge.Api.Models;

public interface IJobRepository
{
    Task<IEnumerable<JobDto>> GetJobsListAsync(string? keyword = null, string? jobType = null, string? location = null, int page = 1, int pageSize = 10);
    Task<JobDto> GetJobByIdAsync(int id);
    Task<int> CreateJobAsync(CreateJobRequestDto request);
    Task<bool> UpdateJobAsync(int id, CreateJobRequestDto request);
    Task<bool> DeleteJobAsync(int id);
    Task<int> GetTotalJobsCountAsync(string? keyword = null, string? jobType = null, string? location = null);
}