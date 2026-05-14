using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Antiforgery;
using SkillBridge.Api.Entities;

public class JobApplication
{
    [Required, Key]
    public int ID {get; set; }
    public Job AppliedJob {get; set; }
    public int AppliedJobId {get; set; }
    public User AppliedBy {get; set; }
    public int AppliedById {get; set; }
    [Required]
    public DateTime ApplicationDate {get; set; }
    [Required]
    public string Status {get; set; }
    public bool IsActive {get; set; }
    [Required]
    public string CoverLetter {get; set; }
    [Required]
    public string ResumePath {get; set; }

}