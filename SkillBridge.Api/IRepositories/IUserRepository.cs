public interface IUserRepository
{
    public Task<string> CreateUserAsync(CreateUserRequestDto user);
    public Task<LoginResponseDto?> LoginAsync(LoginRequestDto request);
    public Task<CreateUserProfileResponseDto> CreateUserProfileAsync(CreateUserProfileRequestDto request);
}