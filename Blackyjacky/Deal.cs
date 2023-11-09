using System;
using System.Collections.Generic;
using System.Text;

namespace BlackJack
{
    public class Deal
    {
        public int card1;
        public int card2;
        public int card3;

        public void DealCards(int cardFace, int cardNumber) 
        {
            switch (cardFace)
            {
                case 0:
                    Console.Write("\u2665");
                    break;

                case 1:
                    Console.Write("\u2660");
                    break;

                case 2:
                    Console.Write("\u2666");
                    break;

                case 3:
                    Console.Write("\u2663");
                    break;
            }


            switch (cardNumber)
            {
                case 0:
                    Console.WriteLine("Ace");
                    break;

                case 1:
                    Console.WriteLine("2");
                    break;

                case 2:
                    Console.WriteLine("3");
                    break;

                case 3:
                    Console.WriteLine("4");
                    break;

                case 4:
                    Console.WriteLine("5");
                    break;

                case 5:
                    Console.WriteLine("6");
                    break;

                case 6:
                    Console.WriteLine("7");
                    break;

                case 7:
                    Console.WriteLine("8");
                    break;

                case 8:
                    Console.WriteLine("9");
                    break;

                case 9:
                    Console.WriteLine("10");
                    break;

                case 10:
                    Console.WriteLine("Knight");
                    break;

                case 11:
                    Console.WriteLine("Queen");
                    break;

                case 12:
                    Console.WriteLine("King");
                    break;
            }
        }


        public int Shufflenumber()
        {
            Random cardNumber = new();

            return Convert.ToInt32(cardNumber.Next(0, 12));
        }
        public int Shuffleface()
        {
            Random cardFace = new();

            return Convert.ToInt32(cardFace.Next(0, 3));
        }
    }
}
