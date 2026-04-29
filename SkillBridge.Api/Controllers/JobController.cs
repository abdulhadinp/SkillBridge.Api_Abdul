using Microsoft.AspNetCore.Mvc;
namespace SkillBridge.Api.Controllers;

[ApiController]
[Route("[controller]")]

public class JobController: ControllerBase
{
    public readonly IJobRepository _jobRepository;
    public JobController(IJobRepository jobRepository)
    {
        _jobRepository = jobRepository;
    }
    [HttpGet]

    public IEnumerable<JobDto> GetJobList()
    {
        return _jobRepository.GetJobListAsync().Result;
    }
}