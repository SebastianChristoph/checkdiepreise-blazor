using CheckDiePreise.Data.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;

namespace CheckDiePreise.Data;

public class DataContext : DbContext
{
    protected readonly IConfiguration Configuration;

    //public DataContext(IConfiguration configuration)
    //{
    //    Configuration = configuration;
    //}

    public DataContext(DbContextOptions<DataContext> options, IConfiguration configuration)
        : base(options)
    {
        Configuration = configuration;
    }
    public DbSet<ProductChange> ProductChanges { get; set; }
    public DbSet<DailyStats> DailyStats { get; set; }

}

