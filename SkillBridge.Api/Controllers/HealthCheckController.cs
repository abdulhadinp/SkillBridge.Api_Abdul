using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;


namespace SkillBridge.Api.Controllers;

[Route("api/[controller]")]
[ApiController]
public class HealthCheckController : ControllerBase
{
    private readonly IConfiguration _configuration;

    public HealthCheckController(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    // GET: api/healthcheck
    [HttpGet]
    public async Task<IActionResult> GetHealth()
    {
        try
        {
            var connectionString = _configuration.GetConnectionString("DefaultConnection");

            if (string.IsNullOrEmpty(connectionString))
            {
                return BadRequest(new { status = "Error", message = "Connection string not configured" });
            }

            using var connection = new SqlConnection(connectionString);
            await connection.OpenAsync();

            // Optional: Get SQL Server version
            using var command = connection.CreateCommand();
            command.CommandText = "SELECT @@VERSION";
            var version = await command.ExecuteScalarAsync();

            return Ok(new
            {
                status = "Healthy",
                database = "Connected",
                server = connection.DataSource,
                sqlVersion = version?.ToString()?.Substring(0, 50) + "...",
                timestamp = DateTime.UtcNow
            });
        }
        catch (SqlException sqlEx)
        {
            return StatusCode(503, new
            {
                status = "Unhealthy",
                message = "Database connection failed",
                error = sqlEx.Message,
                errorCode = sqlEx.Number
            });
        }
        catch (Exception ex)
        {
            return StatusCode(500, new
            {
                status = "Unhealthy",
                message = "Unexpected error",
                error = ex.Message
            });
        }
    }
}