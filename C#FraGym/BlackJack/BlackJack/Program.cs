using System;

namespace BlackJack
{
    class Program
    {
        static void Main(string[] args) 
        {
            Deal d = new Deal();
            Money m = new Money();

            d.card1 = d.Shufflenumber();
            d.card2 = d.Shufflenumber();
            d.card3 = d.Shufflenumber();

            m.start();

            Console.Write("Your first card is:");
            d.DealCards(d.Shuffleface(), d.card1);

            Console.Write("Your Second card is:");
            d.DealCards(d.Shuffleface(), d.card2);

            Console.WriteLine($"You are at:{d.card1+d.card2+2}");


            Console.Write("Dealers first card is:");
            d.DealCards(d.Shuffleface(), d.card3);

            m.HS();
        }
    }
}
