namespace BlackJack
{
    public class Money
    {
        Deal d = new();
        public int card5;
        public int card4;
        public int dealertotal;
        Program p = new();
        public void start()
        {
            Console.WriteLine("Welcome");
            //Console.WriteLine("How much do you want to bet?");
        }
        public void HS()
        {
            Console.WriteLine("Do you hit or stand?");
            string? input = Console.ReadLine();
            if (input == "hit")
            {
                Console.Write("Your third card is:");
                card5 = d.Shufflenumber();
                d.DealCards(d.Shuffleface(), card5);
                
            }
            else if (input == "stand")
            {

            }
            Console.Write("Dealers second card is:");
            card4 = d.Shufflenumber();
            d.DealCards(d.Shuffleface(), card4);
            dealertotal = card4 + d.card3 + 2;
        }
    }
}
