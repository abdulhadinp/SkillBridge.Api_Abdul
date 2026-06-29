using SkillBridge.Api.Entities;
using Microsoft.EntityFrameworkCore;

public class UserRepository : IUserRepository
{
    private readonly SkillBridgeDbContext _context;
    private readonly JwtTokenHelper _jwtTokenHelper;
    private readonly ICurrentUserHelper _currentUserHelper;
    private readonly IFileUploadHelper _fileUploadHelper;

    public UserRepository(
        SkillBridgeDbContext context,
        JwtTokenHelper jwtTokenHelper,
        ICurrentUserHelper currentUserHelper,
        IFileUploadHelper fileUploadHelper)
    {
        _context = context;
        _jwtTokenHelper = jwtTokenHelper;
        _currentUserHelper = currentUserHelper;
        _fileUploadHelper = fileUploadHelper;
    }

    public Task<string> CreateUserAsync(CreateUserRequestDto req_user)
    {
        User user1 = new User
        {
            FullName = req_user.Name,
            Email = req_user.Email,
            PasswordHash = BCrypt.Net.BCrypt.HashPassword(req_user.Password),
            Role = req_user.Type,
            CreatedAt = DateTime.UtcNow,
            IsActive = true
        };

        _context.Users.Add(user1);
        var result = _context.SaveChanges();
        return result > 0
            ? Task.FromResult("User created successfully!")
            : Task.FromResult("Failed to create user.");
    }

    public async Task<LoginResponseDto?> LoginAsync(LoginRequestDto request)
    {
        var user = await _context.Users
            .FirstOrDefaultAsync(u => u.Email == request.Email);

        if (user == null) return null;

        if (string.IsNullOrEmpty(user.PasswordHash) || !user.PasswordHash.StartsWith("$2"))
            return null;

        bool isPasswordValid = BCrypt.Net.BCrypt.Verify(request.Password, user.PasswordHash);
        if (!isPasswordValid) return null;

        var token = _jwtTokenHelper.GenerateToken(
            user.Id,
            user.Email ?? "",
            user.FullName ?? "",
            user.Role ?? "Candidate");

        return new LoginResponseDto
        {
            Token = token,
            UserId = user.Id.ToString(),
            Name = user.FullName,
            Email = user.Email,
            Type = user.Role
        };
    }

    public async Task<CreateUserProfileResponseDto> CreateUserProfileAsync(CreateUserProfileRequestDto request)
    {
        var userId = _currentUserHelper.userID;
        var user = await _context.Users.FindAsync(userId);

        string? resumeUrl = null;
        if (request.Resume != null && request.Resume.Length > 0)
        {
            resumeUrl = await _fileUploadHelper.UploadFileAsync(request.Resume);
        }

        // Check if profile exists; update if so, create if not
        var existing = await _context.CandidateProfiles.FirstOrDefaultAsync(p => p.UserId == userId);
        if (existing != null)
        {
            existing.FullName = request.FullName;
            existing.Email = request.Email;
            existing.PhoneNumber = request.PhoneNumber;
            existing.Education = request.Education;
            existing.LinkedInProfile = request.LinkedInProfile;
            existing.GitHubProfile = request.GitHubProfile;
            existing.Summary = request.Summary;
            if (resumeUrl != null) existing.ResumePath = resumeUrl;
        }
        else
        {
            var profile = new CandidateProfile
            {
                UserId = userId,
                User = user,
                FullName = request.FullName,
                Email = request.Email,
                PhoneNumber = request.PhoneNumber,
                Education = request.Education,
                LinkedInProfile = request.LinkedInProfile,
                GitHubProfile = request.GitHubProfile,
                Summary = request.Summary,
                ResumePath = resumeUrl
            };
            _context.CandidateProfiles.Add(profile);
        }

        var result = await _context.SaveChangesAsync();
        return new CreateUserProfileResponseDto
        {
            Success = result > 0,
            ProfileId = existing?.Id ?? 0
        };
    }
}