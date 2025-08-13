using System;

namespace ConsoleApp1
{
    class Program
    {
        static void Main(string[] args)
        {
            //loop med det ene tal i som går fra 1 til 12
            for (int i = 1; i <= 12; i++)
            {
                //loop med det andet tal fra 1 til 12
                for (int j = 1; j <= 12; j++)
                {
                    //ganger de to tal sammen og laver et mellem rum til næste tal
                    Console.Write(i * j + "\t");
                }
                //starter en ny linie når den har ganget, altså en ny række i tabellen
                Console.Write("\n");
            }

            Console.ReadLine();
        }
    }

}  
