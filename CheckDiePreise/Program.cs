using CheckDiePreise.Components;
using CheckDiePreise.Data;
using CheckDiePreise.Data.Services;
using Microsoft.EntityFrameworkCore;
using System;

var builder = WebApplication.CreateBuilder(args);
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

//var connectionString = Environment.GetEnvironmentVariable("AZURE_SQL_CONNECTIONSTRING") ?? builder.Configuration.GetConnectionString("DefaultConnection");


//if (Environment.IsDevelopment())
//{
//    builder.Services.AddDbContext<DataContext>(options =>
//        options.UseSqlite("Data Source=localdatabase.db"));
//}
//else
//{
//    builder.Services.AddDbContext<DataContext>(options =>
//        options.UseSqlServer(connectionString));
//}


// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();
//builder.Services.AddDbContextFactory<DataContext>(options => options.UseSqlite(connectionString));
builder.Services.AddDbContext<DataContext>(options => options.UseSqlServer(connectionString));
builder.Services.AddScoped<ProductService>();
builder.Services.AddSingleton<IConfiguration>(builder.Configuration);

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseStaticFiles();
app.UseAntiforgery();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

app.Run();
