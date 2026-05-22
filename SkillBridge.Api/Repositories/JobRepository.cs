using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

public class JobRepository : IJobRepository
{
    private readonly SkillBridgedbcontext _context;
    public JobRepository(SkillBridgedbcontext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<JobDto>> GetJobListAsync()
    {
        var jobList = await _context.Jobs.ToListAsync();

        if (jobList == null || jobList.Count == 0)
        {
            return new List<JobDto>();
        }

        return jobList.Select(job => new JobDto
        {
            Id = job.Id,
            Title = job.Title,
            Description = job.Description,
            Company = job.Company,
            Location = job.Location,
            JobType = job.JobType,
            MaximumSalary = job.MaximumSalary,
            MinimumSalary = job.MinimumSalary,
            PostedDate = job.PostedDate,
            DeadLineDate = job.DeadLineDate,
            isActive = job.IsActive
        }).ToList();
    }

    public async Task<JobDto> GetJobByIdAsync(int id)
    {
        var job = await _context.Jobs.FirstOrDefaultAsync(j => j.Id == id);

        if (job == null)
        {
            return null;
        }

        return new JobDto
        {
            Id = job.Id,
            Title = job.Title,
            Description = job.Description,
            Company = job.Company,
            Location = job.Location,
            JobType = job.JobType,
            MaximumSalary = job.MaximumSalary,
            MinimumSalary = job.MinimumSalary,
            PostedDate = job.PostedDate,
            DeadLineDate = job.DeadLineDate,
            isActive = job.IsActive
        };
    }
}