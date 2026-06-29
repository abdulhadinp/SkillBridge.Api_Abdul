using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SkillBridge.Api.IRepositories;
using SkillBridge.Api.Models;

namespace SkillBridge.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class JobController : ControllerBase
    {
        private readonly IJobRepository _jobRepository;

        public JobController(IJobRepository jobRepository)
        {
            _jobRepository = jobRepository;
        }

        /// <summary>
        /// Public endpoint — returns all active jobs with optional search/filter/pagination (FR-05).
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> GetJobList(
            [FromQuery] string? keyword,
            [FromQuery] string? jobType,
            [FromQuery] string? location,
            [FromQuery] int page = 1,
            [FromQuery] int pageSize = 10)
        {
            var jobs = await _jobRepository.GetJobsListAsync(keyword, jobType, location, page, pageSize);
            var total = await _jobRepository.GetTotalJobsCountAsync(keyword, jobType, location);
            return Ok(new
            {
                jobs,
                total,
                page,
                pageSize,
                totalPages = (int)Math.Ceiling((double)total / pageSize)
            });
        }

        /// <summary>
        /// Public endpoint — returns a single job by ID (FR-05).
        /// </summary>
        [HttpGet("{id}")]
        public async Task<IActionResult> GetJobById(int id)
        {
            var job = await _jobRepository.GetJobByIdAsync(id);
            if (job == null || job.Id == 0) return NotFound();
            return Ok(job);
        }

        /// <summary>
        /// Admin creates a new job posting (FR-02).
        /// </summary>
        [HttpPost("create")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> CreateJob([FromBody] CreateJobRequestDto request)
        {
            var jobId = await _jobRepository.CreateJobAsync(request);
            return CreatedAtAction(nameof(GetJobById), new { id = jobId }, new { id = jobId });
        }

        /// <summary>
        /// Admin updates an existing job posting (FR-02).
        /// </summary>
        [HttpPut("{id}")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> UpdateJob(int id, [FromBody] CreateJobRequestDto request)
        {
            var success = await _jobRepository.UpdateJobAsync(id, request);
            if (!success) return NotFound(new { message = "Job not found." });
            return Ok(new { message = "Job updated successfully." });
        }

        /// <summary>
        /// Admin soft-deletes a job posting (sets IsActive = false) (FR-02).
        /// </summary>
        [HttpDelete("{id}")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> DeleteJob(int id)
        {
            var success = await _jobRepository.DeleteJobAsync(id);
            if (!success) return NotFound(new { message = "Job not found." });
            return Ok(new { message = "Job deactivated successfully." });
        }
    }
}