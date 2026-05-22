using SkillBridge.Api.Entities;

public class UserRepository : IUserRepository
{
    private readonly SkillBridgedbcontext _context;
    public UserRepository(SkillBridgedbcontext context)
    {
        _context = context;
    }
    public Task<string> CreateUserAsync (CreatedUserRequestDto req_user)
    {
        User user1 = new User();
        user1.Name = req_user.Name;
        user1.Email = req_user.Email;
        user1.PasswordHash = BCrypt.Net.BCrypt.HashPassword(req_user.Password);
        user1.Type = req_user.Type;
        user1.CreatedAt = DateTime.UtcNow;
        user1.IsActive = true;

        _context.Users.Add(user1);
        var result = _context.SaveChanges();
        if(result > 0)
        {
            return Task.FromResult("User created sucessfully");
        }
        else
        {
            return Task.FromResult("Failed to create user");
        }
    }
}
