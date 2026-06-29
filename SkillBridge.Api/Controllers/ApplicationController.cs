using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SkillBridge.Api.IRepositories;
using SkillBridge.Api.Models;

namespace SkillBridge.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ApplicationController : ControllerBase
    {
        private readonly IApplicationRepository _applicationRepository;
        private readonly ICurrentUserHelper _currentUserHelper;

        public ApplicationController(IApplicationRepository applicationRepository, ICurrentUserHelper currentUserHelper)
        {
            _applicationRepository = applicationRepository;
            _currentUserHelper = currentUserHelper;
        }

        /// <summary>
        /// Candidate submits a job application (FR-06).
        /// Requires authentication. Prevents duplicate submissions.
        /// </summary>
        [HttpPost("apply")]
        [Authorize]
        [Consumes("multipart/form-data")]
        public async Task<IActionResult> Apply([FromForm] SubmitApplicationRequestDto request)
        {
            try
            {
                var result = await _applicationRepository.SubmitApplicationAsync(request);
                return Ok(new { success = true, application = result, message = "Application submitted successfully!" });
            }
            catch (InvalidOperationException ex)
            {
                return Conflict(new { success = false, message = ex.Message });
            }
            catch (Exception ex)
            {
                return BadRequest(new { success = false, message = ex.Message });
            }
        }

        /// <summary>
        /// Candidate checks if they have already applied for a job (FR-06).
        /// </summary>
        [HttpGet("check/{jobId}")]
        [Authorize]
        public async Task<IActionResult> CheckApplied(int jobId)
        {
            var userId = _currentUserHelper.userID;
            var hasApplied = await _applicationRepository.HasAppliedAsync(userId, jobId);
            return Ok(new { hasApplied });
        }

        /// <summary>
        /// Candidate views their own applications with status tracking (FR-07).
        /// </summary>
        [HttpGet("my")]
        [Authorize]
        public async Task<IActionResult> GetMyApplications()
        {
            var userId = _currentUserHelper.userID;
            var apps = await _applicationRepository.GetApplicationsByUserAsync(userId);
            return Ok(apps);
        }

        /// <summary>
        /// Admin views all applications with optional filters (FR-03).
        /// </summary>
        [HttpGet("all")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> GetAllApplications(
            [FromQuery] int? jobId,
            [FromQuery] string? status,
            [FromQuery] DateTime? fromDate,
            [FromQuery] DateTime? toDate)
        {
            var apps = await _applicationRepository.GetAllApplicationsAsync(jobId, status, fromDate, toDate);
            return Ok(apps);
        }

        /// <summary>
        /// Gets a single application by ID (Admin use).
        /// </summary>
        [HttpGet("{id}")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> GetById(int id)
        {
            var app = await _applicationRepository.GetApplicationByIdAsync(id);
            if (app == null) return NotFound();
            return Ok(app);
        }

        /// <summary>
        /// Admin updates application status through the defined workflow (FR-03).
        /// Valid statuses: Applied, Under Review, Shortlisted, Interview, Hired, Rejected
        /// </summary>
        [HttpPut("{id}/status")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> UpdateStatus(int id, [FromBody] UpdateApplicationStatusDto dto)
        {
            var success = await _applicationRepository.UpdateApplicationStatusAsync(id, dto.Status);
            if (!success) return BadRequest(new { message = "Invalid status or application not found." });
            return Ok(new { message = $"Application status updated to '{dto.Status}'." });
        }

        /// <summary>
        /// AI-Powered Job Recommendations for the authenticated candidate (FR-07 bonus).
        /// Matches job titles/descriptions against the candidate's skill keywords.
        /// </summary>
        [HttpGet("recommendations")]
        [Authorize]
        public async Task<IActionResult> GetRecommendations()
        {
            var userId = _currentUserHelper.userID;
            var recs = await _applicationRepository.GetRecommendedJobsAsync(userId);
            return Ok(recs);
        }
    }
}
