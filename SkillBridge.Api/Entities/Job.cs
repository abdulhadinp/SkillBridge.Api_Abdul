using System.ComponentModel.DataAnnotations;

namespace SkillBridge.Api.Entities
{
    /// <summary>
    /// Job entity — inherits from BaseEntity (OOP Inheritance).
    /// </summary>
    public class Job : BaseEntity
    {
        [Required, MaxLength(600)]
        public string? Title { get; set; }

        public string? Description { get; set; }

        public string? Company { get; set; }

        public string? Location { get; set; }

        public string? JobType { get; set; }

        public decimal MinSalary { get; set; }

        public decimal MaxSalary { get; set; }

        public DateTime PostedDate { get; set; } = DateTime.UtcNow;

        public DateTime DeadLineDate { get; set; }

        // Foreign key
        public int PostedById { get; set; }

        // Navigation properties
        public User? PostedBy { get; set; }
        public ICollection<JobApplication> Applications { get; set; } = new List<JobApplication>();
    }
}