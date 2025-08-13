using System;
using System.Collections.Generic;
using System.Text;

namespace BlackJack
{
    public class Money
    {
        Deal d = new Deal();
        int card5;
        int card4;
        Program p = new Program();
        public void start()
        {
            Console.WriteLine("Welcome");
            Console.WriteLine("How much do you want to bet?");
        }
        public void HS()
        {
            Console.WriteLine("Do you hit or stand?");
            string input = Console.ReadLine();
            if (input == "hit")
            {
                Console.Write("Your 3. card is:");
                card5 = d.Shufflenumber();
                d.DealCards(d.Shuffleface(), card5);
            }
            else if (input == "stand")
            {
                Console.Write("Dealers second card is:");
                card4 = d.Shufflenumber();
                d.DealCards(d.Shuffleface(), card4);
                int dealertotal = card4 + d.card3 + 2;
            }
        }
    }
}
