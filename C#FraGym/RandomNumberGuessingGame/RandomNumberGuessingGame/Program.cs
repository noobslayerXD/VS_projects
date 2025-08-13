using System;

namespace RandomNumberGuessingGame
{
    class Program
    {
        static void Main(string[] args)
        {
            //Laver tilfældigt tal
            Random rand = new Random();
            //gør så man kan gætte
            int guess = 0;
            // skriver en lille velkomst
            string start = "Gæt på et tal mellem 1 og 100";
            //laver et tilfældigt tal mellem 1 og 100
            int num = rand.Next(1, 100);
            //Giver et antal gæt man får
            int antalGæt = 10;

            Console.WriteLine(start);
            //Et loop sådan at man kan gætte mere end en gang
            while (guess!=num)
            {
                //Der er lavet try sådan at programmet ikke dør hvis man skriver noget der ikke er et tal
                try
                {
                    //Fjerner et gæt per forsøg 
                    antalGæt--;
                    if (antalGæt == 0)
                    {
                        Console.WriteLine("Du brugte alle dine gæt, du er en taber!!!");
                        return;
                    }
                    guess = Convert.ToInt32(Console.ReadLine());
                    //Hvis tallet man har gættet på er mindre end tallet
                    if (guess < num)
                    {
                        Console.WriteLine("Det tal jeg tænker på er højere end det");
                    }
                    //Hvis det tal man har gættet på et større end tallet
                    else if (guess > num)
                    {
                        Console.WriteLine("Det tal jeg tænker på er lavere end det");
                    }
                    //Fortæller en hvad tallet var, og hvor mange forsøg man brugte på at finde tallet
                    if (guess == num)
                    {
                        Console.WriteLine("Tallet var " + num + ", og du brugte " + (10 - antalGæt) + " forsøg på at gætte det");
                    }
                }
                //Det her er lavet for at stoppe idioter der ikke fatter at de skal skrive tal
                catch
                {
                    Console.WriteLine("Skriv et tal der er helt din nød");
                }
            }

        }

    }
}
