using System;


namespace Prime_number_factorization
{
    class Program
    {
        static void Main(string[] args)
        {

            int a;
            Console.WriteLine("Skriv lige et positivt heltal: ");
            //Konvertere det brugeren skriver om til et tal
            a = int.Parse(Console.ReadLine());
            //caller min method
            Math(a);
        }
        static void Math(int a)
        {
            int b = 2;

            //Her tester den alle tal for at se om de er lige
            if (a % b == 0)
            {

                int x = 0;
                while (a % b == 0)
                {
                    //Ser hvor mange gange tallet går op i to
                    a /= b;
                    x++;
                }
                Console.WriteLine($"{b} er en primtalsfaktor {x} gange");
            }
            else
            {
                //her gør vi det samme bare for 3
                b++;
                int x = 0;
                while (a % b == 0)
                {

                    a /= b;
                    x++;
                }
                if (x == 0)
                {
                    //Hvis tallet hverken har 2 eller 3 som primtalsfaktor, så må det være et primtal
                    Console.WriteLine($"{a} er et primtal");
                }
                else
                {
                    Console.WriteLine($"{b} er en primtalsfaktor {x} gange");
                }
            }

        }
    }
}
