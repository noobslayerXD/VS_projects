using System;

namespace BlackJack
{
    class Program
    {
        static void Main(string[] args)
        {
            Deal d = new();
            Money m = new();

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
            Console.Write($"Dealers cards are at: {m.card4+d.card3+2}\n");
            Console.Write($"You are at: {d.card1+d.card2+m.card5+2}\n");

            if ((d.card1+d.card2+m.card5+2 > m.card4+d.card3+2) && (d.card1+d.card2+m.card5+2 <= 21))
            {
                Console.Write("You're winner!\n");
            }
            else if (d.card1+d.card2+m.card5+2 == m.card4+d.card3+2)
            {
                Console.Write("Draw!\n");
            }
            else
            {
                Console.Write("You lost!\n");
            }
        }
    }
}
