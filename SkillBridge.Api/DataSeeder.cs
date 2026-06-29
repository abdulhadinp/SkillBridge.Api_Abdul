using SkillBridge.Api.Entities;

namespace SkillBridge.Api
{
    /// <summary>
    /// DataSeeder — populates the database with test data in Development mode.
    /// Creates 1 Admin, 5 Candidates, 12 Jobs, 8 Applications.
    /// Only runs if the database is empty to avoid duplicate data on restart.
    /// </summary>
    public static class DataSeeder
    {
        public static async Task SeedAsync(SkillBridgeDbContext context)
        {
            // Only seed if no users exist
            if (context.Users.Any()) return;

            Console.WriteLine("[DataSeeder] Seeding development data...");

            // ─── 1. Admin User ────────────────────────────────────────────────────
            var admin = new User
            {
                FullName = "Admin User",
                Email = "admin@skillbridge.np",
                PasswordHash = BCrypt.Net.BCrypt.HashPassword("Admin@123"),
                Role = "Admin",
                IsActive = true,
                CreatedAt = DateTime.UtcNow
            };
            context.Users.Add(admin);

            // ─── 2. Candidate Users ───────────────────────────────────────────────
            var candidates = new List<User>
            {
                new User { FullName = "Rajan Shrestha", Email = "rajan@example.com", PasswordHash = BCrypt.Net.BCrypt.HashPassword("Test@123"), Role = "Candidate", IsActive = true, CreatedAt = DateTime.UtcNow },
                new User { FullName = "Sunita Tamang", Email = "sunita@example.com", PasswordHash = BCrypt.Net.BCrypt.HashPassword("Test@123"), Role = "Candidate", IsActive = true, CreatedAt = DateTime.UtcNow },
                new User { FullName = "Bikash Gurung", Email = "bikash@example.com", PasswordHash = BCrypt.Net.BCrypt.HashPassword("Test@123"), Role = "Candidate", IsActive = true, CreatedAt = DateTime.UtcNow },
                new User { FullName = "Anisha Rai", Email = "anisha@example.com", PasswordHash = BCrypt.Net.BCrypt.HashPassword("Test@123"), Role = "Candidate", IsActive = true, CreatedAt = DateTime.UtcNow },
                new User { FullName = "Dipesh Karki", Email = "dipesh@example.com", PasswordHash = BCrypt.Net.BCrypt.HashPassword("Test@123"), Role = "Candidate", IsActive = true, CreatedAt = DateTime.UtcNow }
            };

            // Also add candidate1@example.com for screenshot scripts
            var candidate1 = new User { FullName = "Priya Adhikari", Email = "candidate1@example.com", PasswordHash = BCrypt.Net.BCrypt.HashPassword("Test@123"), Role = "Candidate", IsActive = true, CreatedAt = DateTime.UtcNow };
            candidates.Add(candidate1);

            context.Users.AddRange(candidates);
            await context.SaveChangesAsync();

            // ─── 3. Candidate Profiles ────────────────────────────────────────────
            var profiles = new List<CandidateProfile>
            {
                new CandidateProfile { UserId = candidates[0].Id, FullName = "Rajan Shrestha", Email = "rajan@example.com", Skills = "C#, ASP.NET Core, SQL Server, Docker", Experience = "3 years of backend development with .NET technologies.", Education = "BSc Computer Science, Tribhuvan University", Summary = "Experienced .NET developer specialising in web APIs." },
                new CandidateProfile { UserId = candidates[1].Id, FullName = "Sunita Tamang", Email = "sunita@example.com", Skills = "Accounting, Tally ERP, Excel, Financial Analysis", Experience = "2 years as a junior accountant at a Kathmandu-based firm.", Education = "BBS Accounting, Pokhara University", Summary = "Detail-oriented accountant with expertise in Tally ERP." },
                new CandidateProfile { UserId = candidates[2].Id, FullName = "Bikash Gurung", Email = "bikash@example.com", Skills = "React, TypeScript, JavaScript, HTML, CSS", Experience = "2 years of frontend development with React and TypeScript.", Education = "BSc IT, ISMT College", Summary = "Frontend developer passionate about modern UI/UX." },
                new CandidateProfile { UserId = candidates[3].Id, FullName = "Anisha Rai", Email = "anisha@example.com", Skills = "Teaching, Mathematics, Education, Curriculum Design", Experience = "4 years teaching mathematics at secondary school level.", Education = "BEd Mathematics, TU", Summary = "Dedicated mathematics teacher with curriculum design expertise." },
                new CandidateProfile { UserId = candidates[4].Id, FullName = "Dipesh Karki", Email = "dipesh@example.com", Skills = "Management, Project Management, Leadership, MS Office", Experience = "5 years in project management and team leadership.", Education = "BBA Management, Kathmandu University", Summary = "Experienced manager with proven leadership skills." },
                new CandidateProfile { UserId = candidates[5].Id, FullName = "Priya Adhikari", Email = "candidate1@example.com", Skills = "Python, Machine Learning, Data Analysis, SQL", Experience = "1 year internship in data science at tech startup.", Education = "BSc Computer Science, ISMT College", Summary = "Aspiring data scientist with a passion for machine learning." }
            };
            context.CandidateProfiles.AddRange(profiles);

            // ─── 4. Job Listings ──────────────────────────────────────────────────
            var jobs = new List<Job>
            {
                // IT Jobs
                new Job { Title = "Senior .NET Developer", Description = "We are looking for an experienced .NET developer to join our backend team. You will design and develop RESTful APIs using ASP.NET Core 8, work with SQL Server, and deploy applications using Docker.", Company = "Tech Innovations Pvt. Ltd.", Location = "Kathmandu", JobType = "IT", MinSalary = 60000, MaxSalary = 90000, PostedDate = DateTime.UtcNow.AddDays(-10), DeadLineDate = DateTime.UtcNow.AddDays(30), IsActive = true, PostedById = admin.Id, CreatedAt = DateTime.UtcNow.AddDays(-10) },
                new Job { Title = "React Frontend Developer", Description = "Seeking a skilled React developer with TypeScript experience. Responsibilities include building responsive UIs, integrating REST APIs, and collaborating with the design team.", Company = "Digital Solutions Nepal", Location = "Lalitpur", JobType = "IT", MinSalary = 45000, MaxSalary = 70000, PostedDate = DateTime.UtcNow.AddDays(-8), DeadLineDate = DateTime.UtcNow.AddDays(22), IsActive = true, PostedById = admin.Id, CreatedAt = DateTime.UtcNow.AddDays(-8) },
                new Job { Title = "Python Data Analyst", Description = "Join our data team to analyse large datasets, build dashboards, and develop machine learning models. Proficiency in Python, Pandas, and SQL required.", Company = "DataBridge Analytics", Location = "Kathmandu", JobType = "IT", MinSalary = 50000, MaxSalary = 80000, PostedDate = DateTime.UtcNow.AddDays(-5), DeadLineDate = DateTime.UtcNow.AddDays(25), IsActive = true, PostedById = admin.Id, CreatedAt = DateTime.UtcNow.AddDays(-5) },
                new Job { Title = "DevOps Engineer", Description = "We need a DevOps engineer experienced with Docker, Kubernetes, CI/CD pipelines (GitHub Actions / Azure DevOps), and Linux server administration.", Company = "CloudNepal Tech", Location = "Kathmandu", JobType = "IT", MinSalary = 70000, MaxSalary = 100000, PostedDate = DateTime.UtcNow.AddDays(-3), DeadLineDate = DateTime.UtcNow.AddDays(27), IsActive = true, PostedById = admin.Id, CreatedAt = DateTime.UtcNow.AddDays(-3) },
                // Accounting Jobs
                new Job { Title = "Junior Accountant", Description = "Looking for a junior accountant to handle day-to-day bookkeeping, VAT filing, and financial reporting using Tally ERP and Excel.", Company = "Himalayan Finance Group", Location = "Kathmandu", JobType = "Accounting", MinSalary = 25000, MaxSalary = 40000, PostedDate = DateTime.UtcNow.AddDays(-12), DeadLineDate = DateTime.UtcNow.AddDays(18), IsActive = true, PostedById = admin.Id, CreatedAt = DateTime.UtcNow.AddDays(-12) },
                new Job { Title = "Senior Financial Analyst", Description = "Senior role requiring expertise in financial modelling, budgeting, forecasting, and reporting to senior management. CPA qualification preferred.", Company = "Summit Capital Nepal", Location = "Pokhara", JobType = "Accounting", MinSalary = 55000, MaxSalary = 85000, PostedDate = DateTime.UtcNow.AddDays(-6), DeadLineDate = DateTime.UtcNow.AddDays(24), IsActive = true, PostedById = admin.Id, CreatedAt = DateTime.UtcNow.AddDays(-6) },
                // Teaching Jobs
                new Job { Title = "Mathematics Teacher (Grade 8–12)", Description = "We are seeking a qualified Mathematics teacher for grades 8 to 12 in our CBSE curriculum school. Minimum 2 years of teaching experience required.", Company = "Everest International School", Location = "Bhaktapur", JobType = "Teaching", MinSalary = 30000, MaxSalary = 50000, PostedDate = DateTime.UtcNow.AddDays(-15), DeadLineDate = DateTime.UtcNow.AddDays(15), IsActive = true, PostedById = admin.Id, CreatedAt = DateTime.UtcNow.AddDays(-15) },
                new Job { Title = "English Language Instructor", Description = "Looking for an energetic English instructor for both spoken and written English courses. TEFL/TESOL certification is a strong advantage.", Company = "Kathmandu Language Academy", Location = "Kathmandu", JobType = "Teaching", MinSalary = 28000, MaxSalary = 45000, PostedDate = DateTime.UtcNow.AddDays(-4), DeadLineDate = DateTime.UtcNow.AddDays(26), IsActive = true, PostedById = admin.Id, CreatedAt = DateTime.UtcNow.AddDays(-4) },
                // Management Jobs
                new Job { Title = "Project Manager — IT Projects", Description = "Experienced project manager required to lead cross-functional IT teams. PMP certification preferred. Responsible for project planning, execution, and stakeholder communication.", Company = "MountainTech Solutions", Location = "Kathmandu", JobType = "Management", MinSalary = 65000, MaxSalary = 95000, PostedDate = DateTime.UtcNow.AddDays(-9), DeadLineDate = DateTime.UtcNow.AddDays(21), IsActive = true, PostedById = admin.Id, CreatedAt = DateTime.UtcNow.AddDays(-9) },
                new Job { Title = "HR Manager", Description = "We are hiring an HR Manager to oversee recruitment, performance management, employee relations, and HR policy development.", Company = "Namaskar Hospitality Group", Location = "Pokhara", JobType = "Management", MinSalary = 45000, MaxSalary = 70000, PostedDate = DateTime.UtcNow.AddDays(-7), DeadLineDate = DateTime.UtcNow.AddDays(23), IsActive = true, PostedById = admin.Id, CreatedAt = DateTime.UtcNow.AddDays(-7) },
                new Job { Title = "Operations Manager", Description = "Responsible for overseeing daily operations, supply chain, vendor management, and process optimisation across multiple business units.", Company = "Sagarmatha Enterprises", Location = "Chitwan", JobType = "Management", MinSalary = 55000, MaxSalary = 80000, PostedDate = DateTime.UtcNow.AddDays(-2), DeadLineDate = DateTime.UtcNow.AddDays(28), IsActive = true, PostedById = admin.Id, CreatedAt = DateTime.UtcNow.AddDays(-2) },
                new Job { Title = "Business Development Executive", Description = "Drive business growth by identifying new market opportunities, building client relationships, and developing strategic partnerships. Strong communication skills essential.", Company = "Yeti Business Consultants", Location = "Kathmandu", JobType = "Management", MinSalary = 35000, MaxSalary = 60000, PostedDate = DateTime.UtcNow.AddDays(-1), DeadLineDate = DateTime.UtcNow.AddDays(29), IsActive = true, PostedById = admin.Id, CreatedAt = DateTime.UtcNow.AddDays(-1) }
            };
            context.Jobs.AddRange(jobs);
            await context.SaveChangesAsync();

            // ─── 5. Applications ──────────────────────────────────────────────────
            var applications = new List<JobApplication>
            {
                new JobApplication { AppliedJobId = jobs[0].Id, ApplicantId = candidates[0].Id, Status = "Shortlisted", CoverLetter = "I am excited to apply for the Senior .NET Developer position. With 3 years of hands-on experience in ASP.NET Core and SQL Server, I am confident in my ability to contribute to your team.", AppliedAt = DateTime.UtcNow.AddDays(-9), IsActive = true, CreatedAt = DateTime.UtcNow.AddDays(-9) },
                new JobApplication { AppliedJobId = jobs[1].Id, ApplicantId = candidates[2].Id, Status = "Interview", CoverLetter = "As a React and TypeScript developer, I would love to join Digital Solutions Nepal. My portfolio includes several responsive web applications built with React.", AppliedAt = DateTime.UtcNow.AddDays(-7), IsActive = true, CreatedAt = DateTime.UtcNow.AddDays(-7) },
                new JobApplication { AppliedJobId = jobs[2].Id, ApplicantId = candidates[5].Id, Status = "Applied", CoverLetter = "I am a data science enthusiast with hands-on Python and SQL experience. I would welcome the opportunity to contribute to your analytics team.", AppliedAt = DateTime.UtcNow.AddDays(-4), IsActive = true, CreatedAt = DateTime.UtcNow.AddDays(-4) },
                new JobApplication { AppliedJobId = jobs[4].Id, ApplicantId = candidates[1].Id, Status = "Hired", CoverLetter = "With 2 years of accounting experience using Tally ERP and Excel, I am well prepared to handle bookkeeping and VAT filing responsibilities at Himalayan Finance Group.", AppliedAt = DateTime.UtcNow.AddDays(-11), IsActive = true, CreatedAt = DateTime.UtcNow.AddDays(-11) },
                new JobApplication { AppliedJobId = jobs[6].Id, ApplicantId = candidates[3].Id, Status = "Under Review", CoverLetter = "As a qualified Mathematics teacher with 4 years of experience at secondary level, I am enthusiastic about joining Everest International School.", AppliedAt = DateTime.UtcNow.AddDays(-14), IsActive = true, CreatedAt = DateTime.UtcNow.AddDays(-14) },
                new JobApplication { AppliedJobId = jobs[8].Id, ApplicantId = candidates[4].Id, Status = "Rejected", CoverLetter = "I have 5 years of project management experience and hold a PMP certification. I am confident I can lead your IT project teams effectively.", AppliedAt = DateTime.UtcNow.AddDays(-8), IsActive = true, CreatedAt = DateTime.UtcNow.AddDays(-8) },
                new JobApplication { AppliedJobId = jobs[0].Id, ApplicantId = candidates[2].Id, Status = "Applied", CoverLetter = "I am a full-stack developer expanding into .NET. I am eager to learn and bring my React expertise to a senior .NET role.", AppliedAt = DateTime.UtcNow.AddDays(-3), IsActive = true, CreatedAt = DateTime.UtcNow.AddDays(-3) },
                new JobApplication { AppliedJobId = jobs[9].Id, ApplicantId = candidates[4].Id, Status = "Shortlisted", CoverLetter = "With extensive HR management experience, I am committed to fostering a positive workplace culture at Namaskar Hospitality Group.", AppliedAt = DateTime.UtcNow.AddDays(-6), IsActive = true, CreatedAt = DateTime.UtcNow.AddDays(-6) }
            };
            context.JobApplications.AddRange(applications);
            await context.SaveChangesAsync();

            Console.WriteLine("[DataSeeder] ✅ Seeding complete: 1 Admin, 6 Candidates, 12 Jobs, 8 Applications.");
        }
    }
}
