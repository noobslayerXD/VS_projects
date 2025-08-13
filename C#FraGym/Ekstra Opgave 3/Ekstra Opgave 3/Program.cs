using System;

namespace Ekstra_Opgave_3
{
    class Program
    {
        static void Main(string[] args)
        {
            //loop for tallene mellem 1 og en mil
            for (int i= 1; i <= 1000000; i++)
            {

                double j = Math.Pow(-1, i + 1) / 2 * i - 1;
                for (j = Math.Pow(-1, i + 1) / 2 * i - 1;j<1000000;)
                {
                    Console.WriteLine(j);
                }
            }
            
        }
    }
}
