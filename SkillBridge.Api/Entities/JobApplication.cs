using System.ComponentModel.DataAnnotations;
using SkillBridge.Api.Entities;

/// <summary>
/// JobApplication entity — inherits from BaseEntity (OOP Inheritance).
/// </summary>
public class JobApplication : BaseEntity
{
    public Job? AppliedJob { get; set; }
    public int AppliedJobId { get; set; }

    public User? Applicant { get; set; }
    public int ApplicantId { get; set; }

    public DateTime AppliedAt { get; set; } = DateTime.UtcNow;

    [MaxLength(100)]
    public string? Status { get; set; } = "Applied";

    /// <summary>
    /// Cover letter text submitted with the application.
    /// </summary>
    public string? CoverLetter { get; set; }

    /// <summary>
    /// Path to the optional tailored resume PDF uploaded with the application.
    /// </summary>
    [MaxLength(500)]
    public string? ResumePath { get; set; }

    /// <summary>
    /// Optional separate tailored resume path.
    /// </summary>
    [MaxLength(500)]
    public string? TailoredResumePath { get; set; }

    // Backward compat alias
    public string? CoverLetterPath
    {
        get => CoverLetter;
        set => CoverLetter = value;
    }
}