using System.ComponentModel.DataAnnotations;

namespace SkillBridge.Api.Entities
{
    /// <summary>
    /// Abstract base entity demonstrating OOP Inheritance.
    /// All domain entities inherit common audit fields from this class.
    /// </summary>
    public abstract class BaseEntity
    {
        [Key]
        public int Id { get; set; }

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public bool IsActive { get; set; } = true;
    }
}
