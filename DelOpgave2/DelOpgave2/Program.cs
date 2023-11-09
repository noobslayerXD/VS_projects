using System;
using System.Diagnostics;

namespace DelOpgave2
{
    class Program
    {
        static void Main(string[] args)
        {
            //Definerer lige en timer som jeg bruger senere, så jeg kan vise hvor god jeg er
            Stopwatch timer = new Stopwatch();
            //userinput
            int i=Convert.ToInt32(Console.ReadLine());
            //starter timeren
            timer.Start();
            //caller min metode
            PrimeFactor(i);
            //Stopper timeren
            timer.Stop();
            //Skriver hvor lang tid den brugte
            Console.WriteLine(timer.Elapsed);
            //Det var alt:)
            Console.WriteLine("Det var alt:)");

        }
        static void PrimeFactor(int i)
        {
            //en variable til at lave lidt MATH
            int a;
            //Starter med a på 2, altså det laveste primtal, så længe at user inputtet er større end en, så kører den igennem loppen, og får a til at stige med en hver gang
            for (a = 2; i > 1; a++)
            {
                //Hvis man kan dividere UserInputtet med a og det ikke har nogen rest
                if (i % a == 0)
                {
                    //ny variable til at se hvor mange gange man kan bruge denne primtalsfaktor
                    int x = 0;
                    //Så længe at userInputtet kan divideres med a uden rest
                    while (i % a == 0)
                    {
                        //Her dividere man i med a, også bliver i lig med i/a
                        i /= a;
                        //x stiger med en, fordi hvis den kører igennem dette loop må det betyde at den har været en primtalsfaktor en mere gang end før
                        x++;
                    }
                    //Skriver at primtallet a er en primtalsfaktor det antal gange det kørte igennem while loopet
                    Console.WriteLine($"{a} is a prime factor {x} times!");
                }
            }
        }
    }
}
