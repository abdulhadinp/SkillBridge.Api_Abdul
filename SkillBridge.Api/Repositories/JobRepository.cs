using Microsoft.EntityFrameworkCore;
using SkillBridge.Api.Entities;
using SkillBridge.Api.Models;

public class JobRepository : IJobRepository
{
    private readonly SkillBridgeDbContext _context;
    private readonly ICurrentUserHelper _currentUserHelper;

    public JobRepository(SkillBridgeDbContext context, ICurrentUserHelper currentUserHelper)
    {
        _context = context;
        _currentUserHelper = currentUserHelper;
    }

    /// <summary>
    /// Retrieves jobs with optional keyword, jobType, and location filters plus pagination.
    /// Demonstrates Abstraction — implementation detail hidden behind IJobRepository contract.
    /// </summary>
    public async Task<IEnumerable<JobDto>> GetJobsListAsync(
        string? keyword = null,
        string? jobType = null,
        string? location = null,
        int page = 1,
        int pageSize = 10)
    {
        var query = _context.Jobs.Where(j => j.IsActive).AsQueryable();

        if (!string.IsNullOrWhiteSpace(keyword))
        {
            var kw = keyword.ToLower();
            query = query.Where(j =>
                (j.Title != null && j.Title.ToLower().Contains(kw)) ||
                (j.Description != null && j.Description.ToLower().Contains(kw)) ||
                (j.Company != null && j.Company.ToLower().Contains(kw)));
        }

        if (!string.IsNullOrWhiteSpace(jobType))
            query = query.Where(j => j.JobType == jobType);

        if (!string.IsNullOrWhiteSpace(location))
        {
            var loc = location.ToLower();
            query = query.Where(j => j.Location != null && j.Location.ToLower().Contains(loc));
        }

        var jobs = await query
            .OrderByDescending(j => j.PostedDate)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        return jobs.Select(MapToDto);
    }

    public async Task<int> GetTotalJobsCountAsync(string? keyword = null, string? jobType = null, string? location = null)
    {
        var query = _context.Jobs.Where(j => j.IsActive).AsQueryable();

        if (!string.IsNullOrWhiteSpace(keyword))
        {
            var kw = keyword.ToLower();
            query = query.Where(j =>
                (j.Title != null && j.Title.ToLower().Contains(kw)) ||
                (j.Description != null && j.Description.ToLower().Contains(kw)) ||
                (j.Company != null && j.Company.ToLower().Contains(kw)));
        }

        if (!string.IsNullOrWhiteSpace(jobType))
            query = query.Where(j => j.JobType == jobType);

        if (!string.IsNullOrWhiteSpace(location))
        {
            var loc = location.ToLower();
            query = query.Where(j => j.Location != null && j.Location.ToLower().Contains(loc));
        }

        return await query.CountAsync();
    }

    public async Task<JobDto> GetJobByIdAsync(int id)
    {
        var job = await _context.Jobs.FirstOrDefaultAsync(j => j.Id == id);
        return job != null ? MapToDto(job) : new JobDto();
    }

    public async Task<int> CreateJobAsync(CreateJobRequestDto request)
    {
        var job = new Job
        {
            Title = request.Title,
            Description = request.Description,
            Company = request.Company,
            Location = request.Location,
            MinSalary = request.MinSalary,
            MaxSalary = request.MaxSalary,
            JobType = request.JobType,
            PostedDate = DateTime.UtcNow,
            DeadLineDate = request.DeadLineDate,
            IsActive = true,
            PostedById = _currentUserHelper.userID
        };

        _context.Jobs.Add(job);
        await _context.SaveChangesAsync();
        return job.Id;
    }

    public async Task<bool> UpdateJobAsync(int id, CreateJobRequestDto request)
    {
        var job = await _context.Jobs.FindAsync(id);
        if (job == null) return false;

        job.Title = request.Title;
        job.Description = request.Description;
        job.Company = request.Company;
        job.Location = request.Location;
        job.MinSalary = request.MinSalary;
        job.MaxSalary = request.MaxSalary;
        job.JobType = request.JobType;
        job.DeadLineDate = request.DeadLineDate;
        job.IsActive = request.IsActive;

        await _context.SaveChangesAsync();
        return true;
    }

    /// <summary>
    /// Soft-delete: sets IsActive = false rather than removing from database.
    /// Preserves referential integrity for existing applications.
    /// </summary>
    public async Task<bool> DeleteJobAsync(int id)
    {
        var job = await _context.Jobs.FindAsync(id);
        if (job == null) return false;

        job.IsActive = false;
        await _context.SaveChangesAsync();
        return true;
    }

    private static JobDto MapToDto(Job job) => new JobDto
    {
        Id = job.Id,
        Title = job.Title,
        Description = job.Description,
        Company = job.Company,
        Location = job.Location,
        JobType = job.JobType,
        MinSalary = job.MinSalary,
        MaxSalary = job.MaxSalary,
        PostedDate = job.PostedDate,
        DeadLineDate = job.DeadLineDate,
        IsActive = job.IsActive,
        PostedByUserId = job.PostedById
    };
}