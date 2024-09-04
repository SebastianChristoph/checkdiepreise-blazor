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


    //protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    //{
    //    optionsBuilder.UseSqlite(Configuration.GetConnectionString("SQLiteDataDB"));
    //}

    //protected override void OnModelCreating(ModelBuilder modelBuilder)
    //{
    //    var product1 = new Product
    //    {
    //        Id = Guid.NewGuid(),
    //        Name = "Nudeln",
    //    };

    //    var product2 = new Product
    //    {
    //        Id = Guid.NewGuid(),
    //        Name = "Autos",
    //    };

    //    modelBuilder.Entity<Product>().ToTable("Product").HasData(product1, product2);

    //}
    public DbSet<ProductChange> ProductChanges { get; set; }

}

