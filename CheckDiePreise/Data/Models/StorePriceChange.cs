﻿using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace CheckDiePreise.Data.Models
{
    public class StorePriceChange
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int Id { get; set; }
        [Required] public string StoreName { get; set; }
        [Required] public DateTime Date { get; set; }
        [Required] public decimal Price { get; set; }
        [Required] public decimal Baseprice { get; set; }
        [Required]  public string Category { get; set; }
    }
}
