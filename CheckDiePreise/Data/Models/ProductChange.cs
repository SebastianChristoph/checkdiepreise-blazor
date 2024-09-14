using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace CheckDiePreise.Data.Models
{
    public class ProductChange
    {

        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int Id { get; set; }
        [Required] public string Name { get; set; }
        [Required] public DateTime Date { get; set; }
        [Required] public string Identifier { get; set; }
        [Required] public float PriceUnit { get; set; }
        [Required] public string UnitName { get; set; }
        [Required] public float Baseprice { get; set; }
        [Required] public string BasepriceName { get; set; }
        [Required] public string Store { get; set; }
        public string Category { get; set; }
        [Required] public string Trend { get; set; }
        public string Url { get; set; }
    }

}
