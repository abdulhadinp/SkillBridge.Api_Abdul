using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class UserController : ControllerBase
{
    private readonly IUserRepository _userRepository;
    public UserController(IUserRepository userRepository)
    {
        _userRepository = userRepository;
    }
    [HttpPost, Route("create")]
    public async Task<string> CreateUser(CreatedUserRequestDto request)
    {
        var result = await _userRepository.CreateUserAsync(request);
        return result;        
    }
}