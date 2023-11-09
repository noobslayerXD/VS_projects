using System;

namespace Quiz
{
    class Program
    {
        static void Main(string[] args)
        {
            //Laver to tal
            Random rand1 = new Random();
            Random rand2 = new Random();

            int guess = 0;
            int points = 0;

            int num1 = rand1.Next(1, 100);
            int num2 = rand2.Next(1, 100);

            Console.WriteLine(num1 + "+" + num2);

            guess = Convert.ToInt32(Console.ReadLine());

            if (guess == num1 + num2)
            {
                points++;
                Console.WriteLine("Det var rigtigt"+", du har "+points+"points");
                
            }

            else
            {
                Console.WriteLine("Du dårlig");
            }

        }
    }
}
