using CheckDiePreise.Data.Models;
using Microsoft.EntityFrameworkCore;

namespace CheckDiePreise.Data;

public class DataContext : DbContext
{
    protected readonly IConfiguration Configuration;

    public DataContext(IConfiguration configuration)
    {
        Configuration = configuration;
    }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlite(Configuration.GetConnectionString("SQLiteDataDB"));
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        var product1 = new Product
        {
            Id = Guid.NewGuid(),
            Name = "Nudeln",
        };

        var product2 = new Product
        {
            Id = Guid.NewGuid(),
            Name = "Autos",
        };

        modelBuilder.Entity<Product>().ToTable("Products").HasData(product1, product2);

    }
    public DbSet<Product> Products { get; set; }



}

