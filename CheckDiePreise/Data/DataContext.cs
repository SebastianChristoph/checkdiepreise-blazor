﻿using CheckDiePreise.Data.Models;
using Microsoft.EntityFrameworkCore;

namespace CheckDiePreise.Data;

public class DataContext : DbContext
{
     //protected readonly IConfiguration Configuration;

    public DataContext(DbContextOptions<DataContext> options, IConfiguration configuration)
        : base(options)
    {
        //Configuration = configuration;
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

    }
    public DbSet<ProductChange> ProductChanges { get; set; }
    public DbSet<StorePriceChange> StorePriceChanges { get; set; }
    public DbSet<DailyReport> DailyReports { get; set; }

}

