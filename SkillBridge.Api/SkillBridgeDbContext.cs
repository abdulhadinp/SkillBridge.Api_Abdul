using Microsoft.EntityFrameworkCore;
using SkillBridge.Api.Entities;

public class SkillBridgedbcontext : DbContext
{
    public SkillBridgedbcontext(DbContextOptions<SkillBridgedbcontext> options) : base(options)
    {  
    }

    public DbSet<User> Users {get; set;}
}