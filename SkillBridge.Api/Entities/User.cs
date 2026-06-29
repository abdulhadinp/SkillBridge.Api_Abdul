using System.ComponentModel.DataAnnotations;

namespace SkillBridge.Api.Entities
{
    /// <summary>
    /// User entity — demonstrates Encapsulation through property access modifiers.
    /// Inherits Id, CreatedAt, IsActive from BaseEntity (demonstrates Inheritance).
    /// </summary>
    public class User : BaseEntity
    {
        [Required, MaxLength(250)]
        public string? FullName { get; set; }

        // Alias kept for backward compatibility with existing repository code
        public string? Name
        {
            get => FullName;
            set => FullName = value;
        }

        [Required, EmailAddress]
        public string? Email { get; set; }

        [Required]
        public string? PasswordHash { get; set; }

        /// <summary>
        /// Role: "Admin" or "Candidate". Kept as 'Type' in DB for backward compat.
        /// </summary>
        [MaxLength(50)]
        public string? Role { get; set; } = "Candidate";

        // Alias for backward compatibility
        public string? Type
        {
            get => Role;
            set => Role = value;
        }

        // Navigation properties
        public CandidateProfile? CandidateProfile { get; set; }
        public ICollection<Job> PostedJobs { get; set; } = new List<Job>();
        public ICollection<JobApplication> Applications { get; set; } = new List<JobApplication>();
    }
}