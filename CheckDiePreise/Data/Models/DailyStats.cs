using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace CheckDiePreise.Data.Models
{
    public class DailyStats
    {

        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int Id { get; set; }
        [Required] public DateTime Date { get; set; }
        [Required] public string MaxIdentifier { get; set; }
        [Required] public string MaxName { get; set; }
        [Required] public decimal MaxPrice { get; set; }
        [Required] public decimal MaxPriceBefore { get; set; }
        [Required] public string MaxStore { get; set; }
        public string MaxCategory { get; set; }
        [Required] public string MinIdentifier { get; set; }
        [Required] public string MinName { get; set; }
        [Required] public decimal MinPrice { get; set; }
        [Required] public decimal MinPriceBefore { get; set; }
        [Required] public string MinStore { get; set; }
        public string MinCategory { get; set; }
    }
}
