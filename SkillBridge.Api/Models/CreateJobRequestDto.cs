namespace SkillBridge.Api.Models
{
    public class CreateJobRequestDto
    {
        public string? Title { get; set; }
        public string? Description { get; set; }
        public string? Company { get; set; }
        public string? Location { get; set; }
        public string? JobType { get; set; }
        public decimal MinSalary { get; set; }
        public decimal MaxSalary { get; set; }
        public DateTime DeadLineDate { get; set; }
        public bool IsActive { get; set; } = true;
    }
}