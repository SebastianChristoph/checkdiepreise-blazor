using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace CheckDiePreise.Data.Models
{
    public class DailyReport
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int Id { get; set; }
        [Required] public string Name { get; set; }
        [Required] public DateTime Date { get; set; }
        [Required] public string Identifier { get; set; }
        [Required] public decimal Price { get; set; }
        [Required] public decimal Baseprice { get; set; }
        [Required] public string BasepriceUnit { get; set; }
        [Required] public string Store { get; set; }
        public string Category { get; set; }
        public string Url { get; set; }
    }
}
