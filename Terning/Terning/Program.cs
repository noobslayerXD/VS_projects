using System;

namespace Terning
{
    class Program
    {

        static void Main(string[] args)
        {
            Die die = new Die();
            DieCup cup = new DieCup();
            die.roll();
            die.getEyes();
            cup.roll();
            cup.getEyes(); 
        }
    }
}
