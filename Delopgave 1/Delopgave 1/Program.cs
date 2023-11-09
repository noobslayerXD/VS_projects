using System;
using System.Collections.Generic;

namespace Delopgave_1
{
        class Program
        {
            
            static void Main(string[] args)
            {
                //Laver en liste    
                List<int> StoredPrimes = new List<int> { 2, 3, 5, 7, 11, 13 };
                //Caller metoden
                PrintList(StoredPrimes);

            }
            static void PrintList(List<int> StoredPrimes)
            {
                //Går igennem hvert tal i StoredPrimes
                foreach (int i in StoredPrimes)
                {
                    //For hver gang den går igennem stored primes, så skriver den det tal den er nået til
                    Console.WriteLine($"{i}");
                }
            }

        }
}





