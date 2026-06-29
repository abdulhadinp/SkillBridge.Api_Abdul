using Microsoft.EntityFrameworkCore;
using SkillBridge.Api.Entities;

public class SkillBridgeDbContext : DbContext
{
    public SkillBridgeDbContext(DbContextOptions<SkillBridgeDbContext> options) : base(options)
    {
    }

    public DbSet<User> Users { get; set; }
    public DbSet<Job> Jobs { get; set; }
    public DbSet<JobApplication> JobApplications { get; set; }
    public DbSet<CandidateProfile> CandidateProfiles { get; set; }

    // Backward compatibility alias
    public DbSet<CandidateProfile> Userprofiles => CandidateProfiles;

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // User → ignore computed properties (aliases)
        modelBuilder.Entity<User>()
            .Ignore(u => u.Name)
            .Ignore(u => u.Type);

        // Job → User (PostedBy) relationship
        modelBuilder.Entity<Job>()
            .HasOne(j => j.PostedBy)
            .WithMany(u => u.PostedJobs)
            .HasForeignKey(j => j.PostedById)
            .OnDelete(DeleteBehavior.Restrict);

        // JobApplication → Job
        modelBuilder.Entity<JobApplication>()
            .HasOne(a => a.AppliedJob)
            .WithMany(j => j.Applications)
            .HasForeignKey(a => a.AppliedJobId)
            .OnDelete(DeleteBehavior.Restrict);

        // JobApplication → User (Applicant)
        modelBuilder.Entity<JobApplication>()
            .HasOne(a => a.Applicant)
            .WithMany(u => u.Applications)
            .HasForeignKey(a => a.ApplicantId)
            .OnDelete(DeleteBehavior.Restrict);

        // CandidateProfile → User (one-to-one)
        modelBuilder.Entity<CandidateProfile>()
            .HasOne(p => p.User)
            .WithOne(u => u.CandidateProfile)
            .HasForeignKey<CandidateProfile>(p => p.UserId)
            .OnDelete(DeleteBehavior.Cascade);

        // Ignore CoverLetterPath alias
        modelBuilder.Entity<JobApplication>()
            .Ignore(a => a.CoverLetterPath);

        // Map CandidateProfile to 'Userprofiles' table for backward compatibility
        modelBuilder.Entity<CandidateProfile>().ToTable("Userprofiles");
    }
}