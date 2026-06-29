using System.Security.Claims;

public interface ICurrentUserHelper
{
    int userID { get; }

    int GetCurrentUserId();
}
public class CurrentUserHelper : ICurrentUserHelper
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public CurrentUserHelper(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public int userID
    {
        get
        {
            var userIdClaim = _httpContextAccessor.HttpContext?.User.Claims.FirstOrDefault(c => c.Type == ClaimTypes.NameIdentifier);
            if (userIdClaim != null && int.TryParse(userIdClaim.Value, out int userId))
            {
                return userId;
            }
            throw new Exception("User ID claim not found or invalid.");
        }
    }

    public int GetCurrentUserId()
    {
        throw new NotImplementedException();
    }

    int ICurrentUserHelper.GetCurrentUserId()
    {
        throw new NotImplementedException();
    }
}