using System.Threading.Tasks;

public interface IUserRepository
{
    Task<string> CreateUserAsync(CreatedUserRequestDto user);
}