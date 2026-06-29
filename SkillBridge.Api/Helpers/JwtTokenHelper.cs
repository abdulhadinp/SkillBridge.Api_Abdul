using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;

public class JwtTokenHelper
{
    private readonly string _secretKey;
    private readonly int _expireMinutes;
    public JwtTokenHelper(IConfiguration configuration)
    {
        _secretKey = configuration["AppConfig:SecretKey"];
        _expireMinutes = int.Parse(configuration["AppConfig:TokenExpirationMinutes"]);
    }
    public string GenerateToken(int userId, string email, string name, string type)
    {
        int expireMinutes = _expireMinutes;
        string secretKey = _secretKey;
        var tokenHandler = new JwtSecurityTokenHandler();
        var key = Encoding.ASCII.GetBytes(secretKey);
        var tokenDescriptor = new SecurityTokenDescriptor
        {
            Subject = new ClaimsIdentity(new[]
            {
                new Claim(ClaimTypes.NameIdentifier, userId.ToString()),
                new Claim(ClaimTypes.Email, email),
                new Claim(ClaimTypes.Name, name),
                new Claim(ClaimTypes.Role, type)
            }),
            Expires = DateTime.UtcNow.AddMinutes(expireMinutes),
            SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature)
        };
        var token = tokenHandler.CreateToken(tokenDescriptor);
        return tokenHandler.WriteToken(token);
    }
}