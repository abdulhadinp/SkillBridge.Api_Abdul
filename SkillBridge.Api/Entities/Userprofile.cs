using System.ComponentModel.DataAnnotations;
using SkillBridge.Api.Entities;

/// <summary>
/// CandidateProfile entity — inherits from BaseEntity (OOP Inheritance).
/// Stores professional profile information for job seekers.
/// </summary>
public class CandidateProfile : BaseEntity
{
    [Required]
    public int UserId { get; set; }

    public User? User { get; set; }

    [MaxLength(500)]
    public string? FullName { get; set; }

    [MaxLength(500)]
    public string? Email { get; set; }

    [MaxLength(50)]
    public string? PhoneNumber { get; set; }

    /// <summary>
    /// Professional experience summary.
    /// </summary>
    public string? Experience { get; set; }

    /// <summary>
    /// Comma-separated list of skills (e.g., "C#, ASP.NET, MySQL, React").
    /// Used for AI job recommendations via keyword matching.
    /// </summary>
    public string? Skills { get; set; }

    /// <summary>
    /// Educational background details.
    /// </summary>
    public string? Education { get; set; }

    [MaxLength(500)]
    public string? ResumePath { get; set; }

    public string? LinkedInProfile { get; set; }

    public string? GitHubProfile { get; set; }

    /// <summary>
    /// Professional summary / bio.
    /// </summary>
    public string? Summary { get; set; }

    /// <summary>
    /// Computes the profile completion percentage based on filled fields.
    /// Demonstrates Encapsulation — logic is contained within the entity.
    /// </summary>
    public int GetCompletionPercentage()
    {
        int filled = 0;
        int total = 6;
        if (!string.IsNullOrEmpty(FullName)) filled++;
        if (!string.IsNullOrEmpty(Skills)) filled++;
        if (!string.IsNullOrEmpty(Experience)) filled++;
        if (!string.IsNullOrEmpty(Education)) filled++;
        if (!string.IsNullOrEmpty(ResumePath)) filled++;
        if (!string.IsNullOrEmpty(Summary)) filled++;
        return (int)Math.Round((double)filled / total * 100);
    }
}