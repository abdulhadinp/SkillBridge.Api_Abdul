using System.ComponentModel.DataAnnotations;
using SkillBridge.Api.Entities;

public class CreateUserProfileRequestDto
{
    public int Id { get; set; }
    public string? FullName { get; set; }
    public string? Email { get; set; }
    public string? PhoneNumber { get; set; }
    public string? Education { get; set; }
    public string? LinkedInProfile { get; set; }
    public string? ResumePath { get; set; }
    public string? GitHubProfile { get; set; }
    public string? Summary { get; set; }
    public IFormFile? Resume { get; set; }
}

public class CreateUserProfileResponseDto
{
    public bool Success { get; set; }
    public int ProfileId { get; set; }
}

public class UserProfileDto
{
    public int Id { get; set; }
    public string? FullName { get; set; }
    public string? Email { get; set; }
    public string? PhoneNumber { get; set; }
    public string? Education { get; set; }
    public string? LinkedInProfile { get; set; }
    public string? ResumePath { get; set; }
    public string? GitHubProfile { get; set; }
    public string? Summary { get; set; }
}
