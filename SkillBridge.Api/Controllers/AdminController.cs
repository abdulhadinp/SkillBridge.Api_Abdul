using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SkillBridge.Api.IRepositories;

namespace SkillBridge.Api.Controllers
{
    /// <summary>
    /// AdminController — provides dashboard statistics for the Admin role (FR-03).
    /// All endpoints require the "Admin" role.
    /// </summary>
    [ApiController]
    [Route("api/[controller]")]
    [Authorize(Roles = "Admin")]
    public class AdminController : ControllerBase
    {
        private readonly IApplicationRepository _applicationRepository;

        public AdminController(IApplicationRepository applicationRepository)
        {
            _applicationRepository = applicationRepository;
        }

        /// <summary>
        /// Returns aggregate statistics for the admin dashboard:
        /// total jobs, active jobs, total applications, pending applications, total candidates.
        /// </summary>
        [HttpGet("dashboard/stats")]
        public async Task<IActionResult> GetDashboardStats()
        {
            var stats = await _applicationRepository.GetDashboardStatsAsync();
            return Ok(stats);
        }
    }
}
