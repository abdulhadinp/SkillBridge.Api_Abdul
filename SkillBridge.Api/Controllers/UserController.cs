using Microsoft.AspNetCore.Authorization;
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
    public async Task<string> CreateUser(CreateUserRequestDto request)
    {
        
        Console.WriteLine($"Received CreateUser request: {System.Text.Json.JsonSerializer.Serialize(request)}");
        var result = await _userRepository.CreateUserAsync(request);
        return result;
    }
    [HttpPost, Route("login")]
    public async Task<IActionResult> Login(LoginRequestDto request)
    {
        var result = await _userRepository.LoginAsync(request);

        if (result == null)
        {
            return Unauthorized("Invalid email or password");
        }

        return Ok(result);
    }
    [Authorize]
    [HttpPost, Route("profile/create")]
    [Consumes("multipart/form-data")]
    public async Task<CreateUserProfileResponseDto> CreateUserProfile([FromForm] CreateUserProfileRequestDto request)
    {
        var user = await _userRepository.CreateUserProfileAsync(request);
        return user;
    }
}