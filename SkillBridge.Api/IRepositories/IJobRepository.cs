public interface IJobRepository
{
    Task<IEnumerable<JobDto>> GetJobListAsync();
}