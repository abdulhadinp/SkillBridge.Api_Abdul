using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using System;
using System.IO;
using System.Threading.Tasks;

public interface IFileUploadHelper
{
    Task<string> UploadFileAsync(IFormFile file);
}

public class FileUploadHelper : IFileUploadHelper
{
    private readonly IWebHostEnvironment _environment;

    public FileUploadHelper(IWebHostEnvironment environment)
    {
        _environment = environment;
    }

    public async Task<string> UploadFileAsync(IFormFile file)
    {
        if (file == null || file.Length == 0)
        {
            throw new ArgumentException("No file provided.");
        }

        // FIX: WebRootPath is null if the 'wwwroot' folder doesn't exist yet.
        // This fallback prevents the ArgumentNullException crash.
        var webRootPath = _environment.WebRootPath;
        if (string.IsNullOrEmpty(webRootPath))
        {
            webRootPath = Path.Combine(_environment.ContentRootPath, "wwwroot");
        }

        var uploadsFolder = Path.Combine(webRootPath, "uploads");
        
        // This will automatically create the 'wwwroot/uploads' folder if it doesn't exist
        if (!Directory.Exists(uploadsFolder))
        {
            Directory.CreateDirectory(uploadsFolder);
        }

        var uniqueFileName = $"{Guid.NewGuid()}_{file.FileName}";
        var filePath = Path.Combine(uploadsFolder, uniqueFileName);

        using (var stream = new FileStream(filePath, FileMode.Create))
        {
            await file.CopyToAsync(stream);
        }

        // Returns the relative URL path to the uploaded file
        return $"/uploads/{uniqueFileName}";
    }
}