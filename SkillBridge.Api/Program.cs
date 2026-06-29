using Microsoft.EntityFrameworkCore;
using Scalar.AspNetCore;
using SkillBridge.Api;
using SkillBridge.Api.IRepositories;
using SkillBridge.Api.Repositories;

var builder = WebApplication.CreateBuilder(args);

// ─── Services ─────────────────────────────────────────────────────────────────
builder.Services.AddControllers();
builder.Services.AddOpenApi();

// Repository / Service registrations (Dependency Injection — supports OOP Abstraction)
builder.Services.AddScoped<IJobRepository, JobRepository>();
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IApplicationRepository, ApplicationRepository>();
builder.Services.AddScoped<JwtTokenHelper>();
builder.Services.AddHttpContextAccessor();
builder.Services.AddScoped<ICurrentUserHelper, CurrentUserHelper>();
builder.Services.AddScoped<IFileUploadHelper, FileUploadHelper>();

// Database (Entity Framework Core with SQL Server in Docker)
builder.Services.AddDbContext<SkillBridgeDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// CORS — allow React frontend on localhost:5173
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins("http://localhost:5173", "http://localhost:3000")
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });
});

// JWT Authentication
builder.Services.AddAuthentication("Bearer")
    .AddJwtBearer("Bearer", options =>
    {
        options.TokenValidationParameters = new Microsoft.IdentityModel.Tokens.TokenValidationParameters
        {
            ValidateIssuer = false,
            ValidateAudience = false,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["JwtSettings:Issuer"],
            ValidAudience = builder.Configuration["JwtSettings:Audience"],
            IssuerSigningKey = new Microsoft.IdentityModel.Tokens.SymmetricSecurityKey(
                System.Text.Encoding.UTF8.GetBytes(
                    builder.Configuration["JwtSettings:SecretKey"]
                    ?? throw new InvalidOperationException("JwtSettings:SecretKey is missing."))),
        };
    });

builder.Services.AddAuthorization();

var app = builder.Build();

// ─── Auto-migrate and Seed ────────────────────────────────────────────────────
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<SkillBridgeDbContext>();
    db.Database.Migrate();

    // Seed test data in Development mode only
    if (app.Environment.IsDevelopment())
    {
        await DataSeeder.SeedAsync(db);
    }
}

// ─── Middleware Pipeline ──────────────────────────────────────────────────────
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.MapScalarApiReference();
}

app.UseCors("AllowFrontend");
app.UseAuthentication();
app.UseAuthorization();
app.UseStaticFiles();
app.MapControllers();

app.Run();
