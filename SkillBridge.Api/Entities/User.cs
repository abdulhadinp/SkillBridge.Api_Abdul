using System.ComponentModel.DataAnnotations;

namespace SkillBridge.Api.Entities
{
    public class User
    {
    [Required,Key]
    public int ID {get; set;}
    [Required]
    public string Name {get; set;}
    [Required, EmailAddress]
    public string Email {get; set;}
    [Required]
    public string PasswordHash {get; set;}
    [Required]
    public string Type {get; set;}
    [Required]
    public DateTime CreatedAt {get; set;}
    public bool IsActive {get; set;}
    }
}
